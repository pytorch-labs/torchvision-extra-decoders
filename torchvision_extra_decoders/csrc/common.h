// Copyright (c) Meta Platforms, Inc. and affiliates.

// This software may be used and distributed according to the terms of the
// GNU Lesser General Public License version 2.

#pragma once

#include <stdint.h>
#include <torch/torch.h>

namespace extra_decoders_ns {

/* Should be kept in-sync with Python ImageReadMode enum */
using ImageReadMode = int64_t;
const ImageReadMode IMAGE_READ_MODE_UNCHANGED = 0;
const ImageReadMode IMAGE_READ_MODE_GRAY = 1;
const ImageReadMode IMAGE_READ_MODE_GRAY_ALPHA = 2;
const ImageReadMode IMAGE_READ_MODE_RGB = 3;
const ImageReadMode IMAGE_READ_MODE_RGB_ALPHA = 4;

void validate_encoded_data(const torch::Tensor &encoded_data);

bool should_this_return_rgb_or_rgba(ImageReadMode mode, bool has_alpha);

} // namespace extra_decoders_ns
