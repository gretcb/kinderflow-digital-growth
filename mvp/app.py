"""Local HTTP service for the KinderFlow Create a Sign MVP."""

from __future__ import annotations

import argparse
import json
import mimetypes
import re
import threading
from email import policy
from email.parser import BytesParser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

from pipeline import (
    InputError,
    MAX_UPLOAD_BYTES,
    REPO_ROOT,
    RUNS_ROOT,
    load_public_run,
    prepare_run,
    public_run,
    run_pipeline,
    store_demo,
    store_upload,
    validate_extension,
    write_manifest,
)


PROTOTYPE_ROOT = REPO_ROOT / "prototype"
PROCESSING_LOCK = threading.Lock()


def response_schema_ok(payload: dict) -> bool:
    required = {
        "schema_version",
        "run_id",
        "created_at",
        "state",
        "sign",
        "source",
        "stages",
        "technical_status",
        "content_status",
        "metrics",
        "warnings",
        "technical_details",
        "error",
        "artifacts",
        "processing",
    }
    return required.issubset(payload) and isinstance(payload.get("stages"), list)


class KinderFlowHandler(BaseHTTPRequestHandler):
    server_version = "KinderFlowMVP/1.0"

    def send_json(self, payload: dict, status: int = HTTPStatus.OK) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def send_file(self, path: Path) -> None:
        if not path.is_file():
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        file_size = path.stat().st_size
        start = 0
        end = file_size - 1
        status = HTTPStatus.OK
        range_header = self.headers.get("Range")
        if range_header:
            match = re.fullmatch(r"bytes=(\d*)-(\d*)", range_header.strip())
            if not match:
                self.send_error(HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE)
                return
            start_text, end_text = match.groups()
            if start_text:
                start = int(start_text)
                end = int(end_text) if end_text else end
            elif end_text:
                suffix_length = int(end_text)
                start = max(file_size - suffix_length, 0)
            if start >= file_size or start > end:
                self.send_response(HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE)
                self.send_header("Content-Range", f"bytes */{file_size}")
                self.end_headers()
                return
            end = min(end, file_size - 1)
            status = HTTPStatus.PARTIAL_CONTENT
        length = end - start + 1
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(length))
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        if status == HTTPStatus.PARTIAL_CONTENT:
            self.send_header("Content-Range", f"bytes {start}-{end}/{file_size}")
        self.end_headers()
        with path.open("rb") as source:
            source.seek(start)
            remaining = length
            while remaining and (chunk := source.read(min(64 * 1024, remaining))):
                self.wfile.write(chunk)
                remaining -= len(chunk)

    def do_GET(self) -> None:  # noqa: N802
        route = unquote(urlparse(self.path).path)
        if route == "/api/health":
            self.send_json({"status": "ok", "service": "kinderflow-create-sign"})
            return
        if route.startswith("/api/runs/"):
            try:
                self.send_json(load_public_run(route.rsplit("/", 1)[-1]))
            except InputError as error:
                self.send_json({"error": str(error)}, HTTPStatus.NOT_FOUND)
            return
        if route.startswith("/runs/"):
            relative = Path(route.removeprefix("/runs/"))
            candidate = (RUNS_ROOT / relative).resolve()
            if RUNS_ROOT.resolve() not in candidate.parents:
                self.send_error(HTTPStatus.NOT_FOUND)
                return
            self.send_file(candidate)
            return
        relative = "create-sign.html" if route == "/" else route.lstrip("/")
        candidate = (PROTOTYPE_ROOT / relative).resolve()
        if candidate != PROTOTYPE_ROOT and PROTOTYPE_ROOT.resolve() not in candidate.parents:
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        self.send_file(candidate)

    def do_POST(self) -> None:  # noqa: N802
        route = urlparse(self.path).path
        try:
            if route == "/api/runs/demo":
                payload = self.read_json()
                run_dir, manifest = prepare_run(
                    payload.get("sign_name", ""),
                    payload.get("routine_context", ""),
                    payload.get("reference_status", ""),
                    "sign_reference.mp4",
                    "demo_reference",
                )
                video_path = store_demo(run_dir)
            elif route == "/api/runs/upload":
                fields, filename, video_bytes = self.read_multipart()
                validate_extension(filename)
                run_dir, manifest = prepare_run(
                    fields.get("sign_name", ""),
                    fields.get("routine_context", ""),
                    fields.get("reference_status", ""),
                    filename,
                    "operator_upload",
                )
                video_path = store_upload(run_dir, filename, video_bytes)
            else:
                self.send_error(HTTPStatus.NOT_FOUND)
                return
            manifest["source"]["size_bytes"] = video_path.stat().st_size
            manifest["state"] = "queued"
            write_manifest(run_dir, manifest)
            worker = threading.Thread(
                target=self.process_safely,
                args=(run_dir, manifest),
                daemon=True,
            )
            worker.start()
            self.send_json(public_run(manifest), HTTPStatus.ACCEPTED)
        except InputError as error:
            self.send_json({"error": str(error)}, HTTPStatus.BAD_REQUEST)
        except (ValueError, TypeError):
            self.send_json(
                {"error": "The movement check could not be started."},
                HTTPStatus.BAD_REQUEST,
            )

    def process_safely(self, run_dir: Path, manifest: dict) -> None:
        with PROCESSING_LOCK:
            run_pipeline(run_dir, manifest)

    def read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length > 64 * 1024:
            raise InputError("Request is too large.")
        try:
            return json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError as error:
            raise InputError("Request must contain valid JSON.") from error

    def read_multipart(self) -> tuple:
        content_length = int(self.headers.get("Content-Length", "0"))
        if content_length <= 0 or content_length > MAX_UPLOAD_BYTES + 64 * 1024:
            raise InputError("The selected video exceeds the 100 MB demo limit.")
        content_type = self.headers.get("Content-Type", "")
        if not content_type.startswith("multipart/form-data"):
            raise InputError("Upload must use multipart form data.")
        body = self.rfile.read(content_length)
        message = BytesParser(policy=policy.default).parsebytes(
            (
                f"Content-Type: {content_type}\r\n"
                "MIME-Version: 1.0\r\n\r\n"
            ).encode("utf-8")
            + body
        )
        fields = {}
        filename = None
        video_bytes = None
        for part in message.iter_parts():
            name = part.get_param("name", header="content-disposition")
            if name == "reference_video":
                filename = part.get_filename()
                video_bytes = part.get_payload(decode=True)
            elif name in ("sign_name", "routine_context", "reference_status"):
                fields[name] = part.get_content()
        if not filename or video_bytes is None:
            raise InputError("Select an MP4 reference video.")
        return fields, filename, video_bytes

    def log_message(self, format: str, *args: object) -> None:
        print(f"[mvp] {self.address_string()} {format % args}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the KinderFlow Create a Sign MVP")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    RUNS_ROOT.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer((args.host, args.port), KinderFlowHandler)
    print(f"KinderFlow Create a Sign MVP: http://{args.host}:{args.port}/create-sign.html")
    print("Processing remains local. Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
