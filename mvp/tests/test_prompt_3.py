from __future__ import annotations

import io
import ipaddress
import json
import socket
import sys
import tempfile
import time
import unittest
from email.message import Message
from http.client import IncompleteRead
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from urllib.error import HTTPError

import cv2
import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[2]
MVP_ROOT = REPO_ROOT / "mvp"
sys.path.insert(0, str(MVP_ROOT))

import pipeline  # noqa: E402
from app import (  # noqa: E402
    KinderFlowHandler,
    illustrative_video_catalog,
    registered_illustrative_video,
)


def public_resolver(hostname, port, **_kwargs):
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", port))]


def private_resolver(hostname, port, **_kwargs):
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("127.0.0.1", port))]


class FakeResponse:
    def __init__(self, payload: bytes, content_type: str = "video/mp4", url=None, content_length=True):
        self.payload = io.BytesIO(payload)
        self.headers = Message()
        self.headers["Content-Type"] = content_type
        if content_length:
            self.headers["Content-Length"] = str(len(payload))
        self.status = 200
        self.url = url

    def read(self, size=-1):
        return self.payload.read(size)

    def geturl(self):
        return self.url

    def getcode(self):
        return self.status

    def close(self):
        self.payload.close()

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        self.close()


class TimeoutResponse(FakeResponse):
    def read(self, size=-1):
        raise socket.timeout("test timeout")


class IncompleteResponse(FakeResponse):
    def read(self, size=-1):
        raise IncompleteRead(b"partial", 200)


class ManualClock:
    def __init__(self):
        self.value = 0.0

    def __call__(self):
        return self.value


class LateEofResponse(FakeResponse):
    def __init__(self, clock):
        super().__init__(b"", content_length=False)
        self.clock = clock

    def read(self, size=-1):
        self.clock.value = pipeline.REMOTE_VIDEO_TIMEOUT_SECONDS + 1
        return b""


class FakeOpener:
    def __init__(self, *actions):
        self.actions = list(actions)
        self.requests = []

    def open(self, request, timeout):
        self.requests.append((request, timeout))
        action = self.actions.pop(0)
        if isinstance(action, Exception):
            raise action
        return action


def redirect(url: str, location: str, code: int = 302) -> HTTPError:
    headers = Message()
    headers["Location"] = location
    return HTTPError(url, code, "redirect", headers, io.BytesIO())


def tiny_mp4_bytes() -> bytes:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "source.mp4"
        writer = cv2.VideoWriter(
            str(path),
            cv2.VideoWriter_fourcc(*"mp4v"),
            10,
            (64, 64),
        )
        if not writer.isOpened():
            raise unittest.SkipTest("OpenCV MP4 writer is unavailable")
        for index in range(4):
            writer.write(np.full((64, 64, 3), 30 + index * 20, dtype=np.uint8))
        writer.release()
        return path.read_bytes()


class DirectVideoUrlSafetyTests(unittest.TestCase):
    def test_url_requires_http_public_host_without_credentials_or_fragment(self) -> None:
        valid = "https://example.com/reference.mp4?token=temporary"
        self.assertEqual(
            pipeline.validate_direct_video_url(valid, resolver=public_resolver),
            valid,
        )
        for value, message in (
            ("file:///tmp/reference.mp4", "complete http"),
            ("javascript:alert(1)", "complete http"),
            ("https://user:secret@example.com/reference.mp4", "username or password"),
            ("https://example.com/reference.mp4#part", "fragment"),
            ("https://example.com:8443/reference.mp4", "network port"),
        ):
            with self.subTest(value=value):
                with self.assertRaisesRegex(pipeline.InputError, message):
                    pipeline.validate_direct_video_url(value, resolver=public_resolver)
        with self.assertRaisesRegex(pipeline.InputError, "cannot be used"):
            pipeline.validate_direct_video_url(
                "http://127.0.0.1/reference.mp4",
                resolver=private_resolver,
            )

        def slow_resolver(*_args, **_kwargs):
            time.sleep(0.2)
            return public_resolver("example.com", 443)

        with self.assertRaisesRegex(pipeline.InputError, "too long"):
            pipeline.validate_direct_video_url(
                "https://example.com/reference.mp4",
                timeout_seconds=0.01,
                resolver=slow_resolver,
            )

    def test_remote_url_manifest_keeps_sign_and_redacts_query_tokens(self) -> None:
        with tempfile.TemporaryDirectory() as directory, patch.object(
            pipeline, "RUNS_ROOT", Path(directory)
        ):
            _run_dir, manifest = pipeline.prepare_run(
                "WATER",
                "Drink break",
                "Validated reference",
                "direct-video.mp4",
                "direct_video_url",
                "https://cdn.example.com/water.mp4?token=secret",
            )
        self.assertEqual(manifest["sign"]["sign_id"], "water")
        self.assertEqual(manifest["source"]["kind"], "direct_video_url")
        self.assertEqual(manifest["source"]["reference_id"], "direct_video_reference")
        self.assertEqual(manifest["source"]["display_filename"], "Direct video URL")
        self.assertEqual(
            manifest["source"]["reference_source_url"],
            "https://cdn.example.com/water.mp4",
        )
        self.assertNotIn("secret", json.dumps(manifest))

    def test_invalid_direct_url_is_rejected_before_run_directory_is_created(self) -> None:
        with tempfile.TemporaryDirectory() as directory, patch.object(
            pipeline, "RUNS_ROOT", Path(directory)
        ):
            with self.assertRaisesRegex(pipeline.InputError, "username or password"):
                pipeline.prepare_run(
                    "HELP",
                    "Playtime",
                    "Validated reference",
                    "direct-video.mp4",
                    "direct_video_url",
                    "https://user:secret@example.com/help.mp4",
                )
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_valid_remote_mp4_uses_server_name_and_cleans_staging_file(self) -> None:
        payload = tiny_mp4_bytes()
        response = FakeResponse(payload, content_length=False)
        with tempfile.TemporaryDirectory() as directory:
            run_dir = Path(directory) / "run_test"
            opener = FakeOpener(response)
            result = pipeline.store_direct_video_url(
                run_dir,
                "https://example.com/not-trusted-name.bin",
                opener=opener,
                resolver=public_resolver,
            )
            self.assertEqual(result, run_dir / "input/reference.mp4")
            self.assertEqual(result.read_bytes(), payload)
            self.assertEqual(list((run_dir / "input").glob("incoming-*.mp4")), [])
            request, timeout = opener.requests[0]
            self.assertEqual(request.get_header("Accept"), "video/mp4")
            self.assertEqual(request.get_header("Accept-encoding"), "identity")
            self.assertLessEqual(timeout, pipeline.REMOTE_VIDEO_TIMEOUT_SECONDS)

    def test_webpage_and_non_video_response_fail_with_upload_recovery(self) -> None:
        for content_type in ("text/html; charset=utf-8", "application/octet-stream"):
            with self.subTest(content_type=content_type), tempfile.TemporaryDirectory() as directory:
                run_dir = Path(directory) / "run_test"
                opener = FakeOpener(FakeResponse(b"not video", content_type=content_type))
                with self.assertRaisesRegex(
                    pipeline.InputError,
                    "This page cannot be used as a reference video.*upload the video file",
                ):
                    pipeline.store_direct_video_url(
                        run_dir,
                        "https://example.com/page",
                        opener=opener,
                        resolver=public_resolver,
                    )
                self.assertEqual(list((run_dir / "input").glob("*")), [])

    def test_declared_and_streamed_oversize_responses_fail_closed(self) -> None:
        declared = FakeResponse(b"short")
        declared.headers.replace_header(
            "Content-Length", str(pipeline.MAX_UPLOAD_BYTES + 1)
        )
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(pipeline.InputError, "larger than the 100 MB"):
                pipeline.store_direct_video_url(
                    Path(directory) / "declared",
                    "https://example.com/reference.mp4",
                    opener=FakeOpener(declared),
                    resolver=public_resolver,
                )

        with tempfile.TemporaryDirectory() as directory, patch.object(
            pipeline, "MAX_UPLOAD_BYTES", 8
        ):
            run_dir = Path(directory) / "streamed"
            with self.assertRaisesRegex(pipeline.InputError, "larger than the 100 MB"):
                pipeline.store_direct_video_url(
                    run_dir,
                    "https://example.com/reference.mp4",
                    opener=FakeOpener(FakeResponse(b"123456789", content_length=False)),
                    resolver=public_resolver,
                )
            self.assertEqual(list((run_dir / "input").glob("*")), [])

    def test_timeout_removes_partial_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            run_dir = Path(directory) / "run_test"
            with self.assertRaisesRegex(pipeline.InputError, "too long"):
                pipeline.store_direct_video_url(
                    run_dir,
                    "https://example.com/reference.mp4",
                    opener=FakeOpener(TimeoutResponse(b"video")),
                    resolver=public_resolver,
                )
            self.assertEqual(list((run_dir / "input").glob("*")), [])

    def test_truncated_response_and_late_eof_fail_with_unconditional_cleanup(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            run_dir = Path(directory) / "truncated"
            with self.assertRaisesRegex(pipeline.InputError, "ended unexpectedly"):
                pipeline.store_direct_video_url(
                    run_dir,
                    "https://example.com/reference.mp4",
                    opener=FakeOpener(IncompleteResponse(b"video")),
                    resolver=public_resolver,
                )
            self.assertEqual(list((run_dir / "input").glob("*")), [])

        payload = tiny_mp4_bytes()
        mismatched_length = FakeResponse(payload)
        mismatched_length.headers.replace_header(
            "Content-Length",
            str(len(payload) + 100),
        )
        with tempfile.TemporaryDirectory() as directory:
            run_dir = Path(directory) / "short-body"
            with self.assertRaisesRegex(pipeline.InputError, "ended unexpectedly"):
                pipeline.store_direct_video_url(
                    run_dir,
                    "https://example.com/reference.mp4",
                    opener=FakeOpener(mismatched_length),
                    resolver=public_resolver,
                )
            self.assertEqual(list((run_dir / "input").glob("*")), [])

        clock = ManualClock()
        with tempfile.TemporaryDirectory() as directory:
            run_dir = Path(directory) / "late-eof"
            with self.assertRaisesRegex(pipeline.InputError, "too long"):
                pipeline.store_direct_video_url(
                    run_dir,
                    "https://example.com/reference.mp4",
                    opener=FakeOpener(LateEofResponse(clock)),
                    resolver=public_resolver,
                    clock=clock,
                )
            self.assertEqual(list((run_dir / "input").glob("*")), [])

    def test_connection_uses_validated_address_without_second_dns_lookup(self) -> None:
        connections = []

        class FakeSocket:
            def settimeout(self, value):
                self.timeout = value

            def connect(self, destination):
                connections.append(destination)

            def setsockopt(self, *_args):
                pass

            def close(self):
                pass

        with patch.object(pipeline.socket, "socket", return_value=FakeSocket()):
            connection = pipeline.PinnedHTTPConnection(
                "attacker-controlled.example",
                pinned_addresses=[ipaddress.ip_address("93.184.216.34")],
                timeout=2,
            )
            connection.connect()
        self.assertEqual(connections, [("93.184.216.34", 80)])

    def test_redirects_are_bounded_and_revalidated(self) -> None:
        payload = tiny_mp4_bytes()
        safe_redirect = redirect(
            "https://example.com/reference.mp4",
            "https://media.example.com/reference.mp4",
        )
        with tempfile.TemporaryDirectory() as directory:
            result = pipeline.store_direct_video_url(
                Path(directory) / "safe",
                "https://example.com/reference.mp4",
                opener=FakeOpener(safe_redirect, FakeResponse(payload, url="https://media.example.com/reference.mp4")),
                resolver=public_resolver,
            )
            self.assertTrue(result.is_file())

        def mixed_resolver(hostname, port, **_kwargs):
            return private_resolver(hostname, port) if hostname == "127.0.0.1" else public_resolver(hostname, port)

        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(pipeline.InputError, "cannot be used"):
                pipeline.store_direct_video_url(
                    Path(directory) / "private",
                    "https://example.com/reference.mp4",
                    opener=FakeOpener(redirect("https://example.com/reference.mp4", "https://127.0.0.1/reference.mp4")),
                    resolver=mixed_resolver,
                )

        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(pipeline.InputError, "unsafe destination"):
                pipeline.store_direct_video_url(
                    Path(directory) / "downgrade",
                    "https://example.com/reference.mp4",
                    opener=FakeOpener(redirect("https://example.com/reference.mp4", "http://media.example.com/reference.mp4")),
                    resolver=public_resolver,
                )

        redirects = [
            redirect("https://example.com/reference.mp4", f"https://example.com/{index}.mp4")
            for index in range(pipeline.REMOTE_VIDEO_REDIRECT_LIMIT + 1)
        ]
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(pipeline.InputError, "too many times"):
                pipeline.store_direct_video_url(
                    Path(directory) / "loop",
                    "https://example.com/reference.mp4",
                    opener=FakeOpener(*redirects),
                    resolver=public_resolver,
                )


class IllustrativeVideoRegistryTests(unittest.TestCase):
    def test_catalog_exposes_only_registered_outputs_without_paths(self) -> None:
        catalog = illustrative_video_catalog()
        signs = catalog["signs"]
        expected = {
            "more": "mas.mp4",
            "help": "ayuda.mp4",
            "milk": "leche.mp4",
        }
        for sign_id, filename in expected.items():
            with self.subTest(sign_id=sign_id):
                self.assertTrue(signs[sign_id]["available"])
                self.assertEqual(signs[sign_id]["url"], f"/api/illustrative-videos/{sign_id}")
                self.assertEqual(signs[sign_id]["provider"], "Google Labs FX / Gemini FX")
                self.assertEqual(registered_illustrative_video(sign_id)["path"].name, filename)
                self.assertEqual(
                    signs[sign_id]["usage_status"],
                    "GOOGLE_LABS_FX_OUTPUT_USAGE_CONFIRMATION_NEEDED",
                )
        for sign_id in ("eat", "sleep", "water"):
            with self.subTest(sign_id=sign_id):
                self.assertFalse(signs[sign_id]["available"])
                self.assertIsNone(signs[sign_id]["url"])
        self.assertIsNone(registered_illustrative_video("unsupported"))
        serialized = json.dumps(catalog)
        self.assertNotIn("../resources", serialized)
        self.assertNotIn("/Users/", serialized)

    def test_registry_tampering_and_explicit_display_denial_fail_closed(self) -> None:
        registry = json.loads(
            (REPO_ROOT / "assets/registry/sign_asset_registry.json").read_text(encoding="utf-8")
        )
        cases = []
        denied = json.loads(json.dumps(registry))
        denied["assets"]["demo_more"]["demo_display_allowed"] = False
        cases.append(denied)
        missing_display_field = json.loads(json.dumps(registry))
        missing_display_field["assets"]["demo_more"].pop("demo_display_allowed")
        cases.append(missing_display_field)
        wrong_status = json.loads(json.dumps(registry))
        next(item for item in wrong_status["signs"] if item["sign_id"] == "more")["gemini_demo_status"] = "NOT_AVAILABLE_STATIC_FLOW_ALLOWED"
        cases.append(wrong_status)
        wrong_provider = json.loads(json.dumps(registry))
        next(item for item in wrong_provider["signs"] if item["sign_id"] == "more")["gemini_demo_provider"] = "Unknown provider"
        cases.append(wrong_provider)
        wrong_licence = json.loads(json.dumps(registry))
        wrong_licence["assets"]["demo_more"]["licence_or_provenance_status"] = "UNVERIFIED"
        cases.append(wrong_licence)
        escaped_path = json.loads(json.dumps(registry))
        escaped_path["assets"]["demo_more"]["path"] = "../resources/video_input/more.mp4"
        cases.append(escaped_path)
        bad_hash = json.loads(json.dumps(registry))
        bad_hash["assets"]["demo_more"]["sha256"] = "0" * 64
        cases.append(bad_hash)
        for index, candidate in enumerate(cases):
            with self.subTest(case=index):
                self.assertIsNone(registered_illustrative_video("more", candidate))
        self.assertIsNone(registered_illustrative_video("more", {}))

    def test_expected_output_hashes_and_directory_contents_are_exact(self) -> None:
        expected = {
            "more": ("mas.mp4", "adec2ddda3b6cd8ce0a10e9eaa8a5eaf02f826147c0ea33fcc3be403ee48f6a4"),
            "help": ("ayuda.mp4", "529b3bea31746d8a1ce305828244badfa9db543ae1960312ad7c6665b838db02"),
            "milk": ("leche.mp4", "55d106d20318c9c9be430f523a71e4b85d5a7656c90c4fdbdf32a58d1efa95c2"),
        }
        for sign_id, (filename, digest) in expected.items():
            verified = registered_illustrative_video(sign_id)
            self.assertEqual(verified["path"].name, filename)
            self.assertEqual(verified["asset"]["sha256"], digest)
        output_root = REPO_ROOT.parent / "resources/video_output"
        self.assertEqual(
            {path.name for path in output_root.iterdir() if path.is_file()},
            {"mas.mp4", "ayuda.mp4", "leche.mp4"},
        )

    def test_demo_output_is_never_a_reference_input(self) -> None:
        registry = json.loads(
            (REPO_ROOT / "assets/registry/sign_asset_registry.json").read_text(encoding="utf-8")
        )
        assets = registry["assets"]
        input_hashes = {
            assets[sign["reference_video_input"]]["sha256"] for sign in registry["signs"]
        }
        output_hashes = {
            registered_illustrative_video(sign_id)["asset"]["sha256"]
            for sign_id in ("more", "help", "milk")
        }
        self.assertEqual(len(output_hashes), 3)
        self.assertTrue(output_hashes.isdisjoint(input_hashes))


class JsonRequestBoundaryTests(unittest.TestCase):
    @staticmethod
    def request(payload: bytes, **headers):
        base_headers = {
            "Content-Type": "application/json",
            "Content-Length": str(len(payload)),
            "Host": "127.0.0.1:8000",
        }
        base_headers.update(headers)
        return SimpleNamespace(headers=base_headers, rfile=io.BytesIO(payload))

    def test_json_reader_accepts_same_origin_object(self) -> None:
        request = self.request(
            b'{"sign_name":"MORE"}',
            Origin="http://127.0.0.1:8000",
        )
        self.assertEqual(
            KinderFlowHandler.read_json(request),
            {"sign_name": "MORE"},
        )

    def test_json_reader_rejects_simple_cross_origin_and_non_object_requests(self) -> None:
        cases = (
            (self.request(b"{}", **{"Content-Type": "text/plain"}), "application/json"),
            (self.request(b"{}", Origin="https://evil.example"), "Cross-origin"),
            (self.request(b"{}", Origin="https://127.0.0.1:8000"), "Cross-origin"),
            (self.request(b"{}", Origin="http://127.0.0.1:8000/path"), "Cross-origin"),
            (self.request(b"[]"), "JSON object"),
            (self.request(b"{}", **{"Content-Length": "-1"}), "length is invalid"),
        )
        for request, message in cases:
            with self.subTest(message=message):
                with self.assertRaisesRegex(pipeline.InputError, message):
                    KinderFlowHandler.read_json(request)


if __name__ == "__main__":
    unittest.main()
