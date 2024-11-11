# Copyright (c) Meta Platforms, Inc. and affiliates.

# This software may be used and distributed according to the terms of the
# GNU Lesser General Public License version 2.

from pathlib import Path

import torch

try:
    from .version import __version__  # noqa: F401
except ImportError:
    pass


def expose_extra_decoders():
    suffix = ".so"  # TODO: make this cross-platform
    torch.ops.load_library(Path(__file__).parent / f"extra_decoders_lib{suffix}")
