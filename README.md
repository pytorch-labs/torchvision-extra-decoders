An extension of [TorchVision](https://github.com/pytorch/vision) for decoding
AVIF and HEIC images.

## Usage

Assuming torchvision is already installed:

```bash
$ pip install torchvision-extra-decoders
```

Then, you can use the HEIC and AVIF decoders from torchvision like the other
decoders ([docs](https://pytorch.org/vision/stable/io.html)):

```py
from torchvision.io import decode_image, decode_heic, decode_avif

img = decode_image("image.heic")
img = decode_image("image.avif")

img = decode_heic("image.heic")
img = decode_avif("image.avif")
```

## LICENSE

This project is released under the [LGPL 2.1 License](./LICENSE).
