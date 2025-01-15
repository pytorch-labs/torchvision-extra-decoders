// Copyright (c) Meta Platforms, Inc. and affiliates.

// This software may be used and distributed according to the terms of the
// GNU Lesser General Public License version 2.

#include "decode_avif.h"
#include "decode_heic.h"
#include <ATen/core/op_registration/op_registration.h>

// TODO: Uncomment when/if we suppot windows
// // If we are in a Windows environment, we need to define
// // initialization functions for the _custom_ops extension
// #ifdef _WIN32
// void* PyInit_extra_decoders(void) {
//   return nullptr;
// }
// #endif

namespace extra_decoders_ns {

static auto registry = torch::RegisterOperators()
                           .op("extra_decoders_ns::decode_heic(Tensor "
                               "encoded_data, int mode) -> Tensor",
                               &decode_heic)
                           .op("extra_decoders_ns::decode_avif(Tensor "
                               "encoded_data, int mode) -> Tensor",
                               &decode_avif);

} // namespace extra_decoders_ns
