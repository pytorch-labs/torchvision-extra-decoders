Disclaimer: this is still WIP!!


An extension of `torchvision` for decoding AVIF and HEIC images.

Usage:

```bash
$ pip install torchvision-extra-decoders
```

Then

```py
from torchvision.io import decode_image, decode_heic, decode_avif

img = decode_image("image.heic")
img = decode_image("image.avif")

img = decode_heic("image.heic")
img = decode_avif("image.avif")
```
