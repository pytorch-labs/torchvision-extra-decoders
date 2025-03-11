#!/bin/bash

set -ex

ls dist
wheel_path=`find dist -type f -name "*.whl"`

echo Found $wheel_path


# Put all the .so files we want to ship with the wheels within the lib_to_bundle
# dir. Maybe it's enough to LD_LIBRARY_PATH $CONDA_PREFIX/lib but I fear this
# might include some un-desired libc or libcxx so files?
mkdir libs_to_bundle
for f in `find $CONDA_PREFIX/lib | grep -e libavif.so -e libdav1d.so -e librav1e.so -e libSvtAv1Enc.so -e libaom.so -e libheif.so -e libx265.so -e libde265.so`; do cp $f libs_to_bundle; done
echo `ls libs_to_bundle`
export LD_LIBRARY_PATH="$PWD/libs_to_bundle:$LD_LIBRARY_PATH"

# This is the oldest we can do based on the existing dependencies.
wheel_platform="manylinux_2_39_x86_64"

${CONDA_RUN} auditwheel -v repair --plat $wheel_platform $wheel_path  --exclude libtorch_python.so --exclude libc10.so --exclude libtorch.so --exclude libtorch_cpu.so --wheel-dir dist

# mv original wheel to a different dir, the 'repaired' wheel outputed by
# auditwheel is still in dist/
mkdir original_wheel
mv $wheel_path original_wheel/


# This is absolutely disgusting, we're effectively pretending that the wheel is
# compatible with older platforms than it actually does.
new_wheel_platform="manylinux_2_17_x86_64.manylinux2014_x86_64"
echo "Replacing ${wheel_platform} with ${new_wheel_platform} in wheel name"
mv dist/*${wheel_platform}*.whl $(echo dist/*${wheel_platform}*.whl | sed "s/${wheel_platform}/${new_wheel_platform}/")
