#!/bin/bash

set -ex

ls dist
wheel_path=`find dist -type f -name "*.whl"`

echo Found $wheel_path

# auditwheel -v repair --plat manylinux_2_38_x86_64  $wheel_path  --exclude libtorch_python.so --exclude libc10.so --exclude libtorch.so --exclude libtorch_cpu.so --wheel-dir dist

# old="linux_x86_64"
# new="manylinux_2_17_x86_64.manylinux2014_x86_64"
# echo "Replacing ${old} with ${new} in wheel name"
# mv dist/*${old}*.whl $(echo dist/*${old}*.whl | sed "s/${old}/${new}/")
