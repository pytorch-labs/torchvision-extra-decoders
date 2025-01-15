// Copyright (c) Meta Platforms, Inc. and affiliates.

// This software may be used and distributed according to the terms of the
// GNU Lesser General Public License version 2.

#pragma once

#include "common.h"
#include <torch/torch.h>

namespace extra_decoders_ns {

C10_EXPORT torch::Tensor decode_heic(const torch::Tensor &encoded_data,
                                     ImageReadMode mode);

} // namespace extra_decoders_ns
