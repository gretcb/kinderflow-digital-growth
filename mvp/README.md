# KinderFlow Create a Sign MVP

This local MVP turns a validated adult reference sign video into isolated MediaPipe landmarks, body-relative motion diagnostics and a reviewable movement preview. It reuses the Round 1 POC code; it does not duplicate the Computer Vision method.

## Requirements

- Python 3.11 or 3.12;
- MediaPipe legacy Solutions API (MediaPipe 0.10);
- ffmpeg with an H.264 encoder available on PATH;
- an MP4 reference video; and
- the existing local demo file at *poc/input/sign_reference.mp4* for the demo-reference path.

Create and activate a virtual environment, then install:

~~~bash
python -m pip install -r mvp/requirements.txt
~~~

## Start

From the repository root:

~~~bash
python mvp/app.py
~~~

Open [http://127.0.0.1:8000/create-sign.html](http://127.0.0.1:8000/create-sign.html).

The service also serves the existing prototype routes, including the Flashcard Builder.

## Demonstration paths

- **Demo reference:** choose **Use demo reference video**, then run the movement check. This processes the existing private local reference through the real pipeline.
- **Custom reference:** select another MP4 validated reference. Metrics and artifacts are calculated for that upload.

MP4 is the supported MVP format. Uploads are limited to 100 MB, remain local and are stored under a generated *mvp/runs/run_...* directory. Run artifacts are ignored by Git. The canonical Round 1 files in *poc/output* are not overwritten.

MediaPipe/OpenCV first writes the real landmark overlay as an intermediate MPEG-4 Part 2 file. The MVP then uses ffmpeg to create a browser-facing H.264 MP4 with yuv420p pixel format and fast-start metadata. MediaPipe is not rerun. If ffmpeg or H.264 encoding is unavailable, the run stops with a controlled preview error rather than presenting an unplayable video.

## Operator-facing status rules

- **Pass:** extraction is EXTRACTION_PASS and all five automated POC quality dimensions are PASS.
- **Review needed:** extraction produced usable movement data and no automated dimension failed, but at least one dimension is PARTIAL.
- **Fail:** extraction is EXTRACTION_FAIL, motion status is MOTION_REPRESENTATION_FAIL, or any automated quality dimension is FAIL.

The POC's raw statuses remain available under technical details. Proceed with conditions is not shown as the main operator status.

Actions are deliberately bounded:

- Pass → **Approve**;
- Review needed → **Approve anyway** or **Use another reference video**;
- Fail → **Use another reference video** only.

Approval publishes only in the current local browser session and unlocks the downstream Flashcard link.

For live presentations, keep a short screen recording of the completed demo flow as a fallback. The recording should show the input, stage progression, visual comparison, metrics and review boundary without including private filesystem paths.

The current local sample is technical fallback evidence, not a production library asset. Confirm its source rights, intended sign identity and presentation permission before showing the reference or overlay externally; otherwise replace it with an owned or appropriately licensed validated adult reference.

## Tests

~~~bash
python -m unittest discover -s mvp/tests -v
python -m unittest discover -s poc/tests -v
~~~

The real demo-reference integration test is opt-in because it runs MediaPipe:

~~~bash
KINDERFLOW_RUN_INTEGRATION=1 python -m unittest mvp.tests.test_mvp.DemoIntegrationTest -v
~~~

## Boundaries

The technical result answers whether the captured movement produced usable structured evidence for review. It does not certify linguistic sign correctness. Human review remains the publication gate. Publication controls are local demo state only; no authentication, audit log, database, cloud storage, external API, automatic publication, production avatar or child-video processing is implemented.
