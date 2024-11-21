#!/bin/bash

set -ex

old="linux_x86_64"
new="manylinux_2_17_x86_64.manylinux2014_x86_64"
echo "Replacing ${old} with ${new} in wheel name"
mv dist/*${old}*.whl $(echo dist/*${old}*.whl | sed "s/${old}/${new}/")
