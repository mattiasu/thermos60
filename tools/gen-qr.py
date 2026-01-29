#!/usr/bin/env python3
import qrcode
from qrcode.image.svg import SvgPathImage

URL = "https://thermos60.pages.dev/"
OUT = "thermos-addy-se.svg"

img = qrcode.make(
    URL,
    image_factory=SvgPathImage,
    box_size=10
)

img.save(OUT)
print(f"Saved {OUT}")
