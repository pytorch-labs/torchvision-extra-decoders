#!/bin/bash

set -ex

ls dist
wheel_path=`find dist -type f -name "*.whl"`

echo Found $wheel_path


# Put all the .so files we want to ship with the wheels within the lib_to_bundle
# dir. Maybe it's enough to LD_LIBRARY_PATH $CONDA_PREFIX/lib but I fear this
# might include some un-desired libc or libcxx so files?
mkdir libs_to_bundle
for f in `find $CONDA_PREFIX/lib | grep -e libavif.so -e libdav1d.so -e librav1e.so  -e libaom.so -e libheif.so -e libx265.so -e libde265.so`; do cp $f libs_to_bundle; done
echo `ls libs_to_bundle`
export LD_LIBRARY_PATH="$PWD/libs_to_bundle:$LD_LIBRARY_PATH"

${CONDA_RUN} auditwheel -v repair --plat manylinux_2_38_x86_64  $wheel_path  --exclude libtorch_python.so --exclude libc10.so --exclude libtorch.so --exclude libtorch_cpu.so --wheel-dir dist

# mv original wheel to a different dir, the 'repaired' wheel outputed by auditwheel should still be in `dist` and treated and *the* wheel
mkdir original_wheel
mv $wheel_path original_wheel/

# old="linux_x86_64"
# new="manylinux_2_17_x86_64.manylinux2014_x86_64"
# echo "Replacing ${old} with ${new} in wheel name"
# mv dist/*${old}*.whl $(echo dist/*${old}*.whl | sed "s/${old}/${new}/")
