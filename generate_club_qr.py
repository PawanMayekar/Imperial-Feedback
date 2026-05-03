#!/usr/bin/env python3
"""Generate a PNG QR code for the Club feedback form URL.

On Windows, run with the project venv so `qrcode` resolves (do not use `py`
without the venv—it uses a different Python):

    feedvenv\\Scripts\\python.exe generate_club_qr.py
"""

from __future__ import annotations

import argparse
from pathlib import Path

import qrcode
from qrcode.constants import ERROR_CORRECT_M

DEFAULT_URL = "https://clubfeedback.sdcorp.in//forms/restaurant/"
DEFAULT_OUT = Path(__file__).resolve().parent / "club_feedback_qr.png"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a QR code PNG for the form URL.")
    parser.add_argument("--url", default=DEFAULT_URL, help="URL to encode")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUT,
        help="Output PNG path",
    )
    args = parser.parse_args()

    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_M,
        box_size=12,
        border=4,
    )
    qr.add_data(str(args.url))
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    out = args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    print(f"Wrote {out.resolve()}")


if __name__ == "__main__":
    main()
