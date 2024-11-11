# Copyright (c) Meta Platforms, Inc. and affiliates.

# This software may be used and distributed according to the terms of the
# GNU Lesser General Public License version 2.

import os
import subprocess
import sys
from pathlib import Path

from setuptools import find_packages, setup

from torch.utils.cpp_extension import BuildExtension, CppExtension

ROOT_DIR = Path(__file__).absolute().parent


# Same version logic as in torchvision
def get_and_write_version():
    with open(ROOT_DIR / "version.txt") as f:
        version = f.readline().strip()
    sha = "Unknown"

    try:
        sha = (
            subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(ROOT_DIR))
            .decode("ascii")
            .strip()
        )
    except Exception:
        pass

    if os.getenv("BUILD_VERSION"):
        version = os.getenv("BUILD_VERSION")
    elif sha != "Unknown":
        version += "+" + sha[:7]

    with open(ROOT_DIR / "torchvision_extra_decoders/version.py", "w") as f:
        f.write(f"__version__ = '{version}'\n")
        f.write(f"git_version = {repr(sha)}\n")

    return version


def find_library(header):
    # returns (found, include dir, library dir)
    # if include dir or library dir is None, it means that the library is in
    # standard paths and don't need to be added to compiler / linker search
    # paths

    searching_for = f"Searching for {header}"

    # Try conda-related prefixes. If BUILD_PREFIX is set it means conda-build is
    # being run. If CONDA_PREFIX is set then we're in a conda environment.
    for prefix_env_var in ("BUILD_PREFIX", "CONDA_PREFIX"):
        if (prefix := os.environ.get(prefix_env_var)) is not None:
            prefix = Path(prefix)
            if sys.platform == "win32":
                prefix = prefix / "Library"
            include_dir = prefix / "include"
            library_dir = prefix / "lib"
            if (include_dir / header).exists():
                print(f"{searching_for}. Found in {prefix_env_var}.")
                return True, str(include_dir), str(library_dir)
        print(f"{searching_for}. Didn't find in {prefix_env_var}.")

    if sys.platform == "linux":
        for prefix in (Path("/usr/include"), Path("/usr/local/include")):
            if (prefix / header).exists():
                print(f"{searching_for}. Found in {prefix}.")
                return True, None, None
            print(f"{searching_for}. Didn't find in {prefix}")

    return False, None, None


def make_extension():

    heic_found, heic_include_dir, heic_library_dir = find_library(
        header="libheif/heif_cxx.h"
    )
    if not heic_found:
        raise RuntimeError("Couldn't find libheic!")

    print(f"{heic_include_dir = }")
    print(f"{heic_library_dir = }")

    avif_found, avif_include_dir, avif_library_dir = find_library(header="avif/avif.h")
    if not avif_found:
        raise RuntimeError("Couldn't find libavif!")

    print(f"{heic_include_dir = }")
    print(f"{heic_library_dir = }")

    sources = list(Path("torchvision_extra_decoders/csrc/").glob("*.cpp"))
    print(f"{sources = }")

    return CppExtension(
        name="torchvision_extra_decoders.extra_decoders_lib",
        sources=sorted(str(s) for s in sources),
        include_dirs=[heic_include_dir, avif_include_dir],
        library_dirs=[heic_library_dir, avif_library_dir],
        libraries=["heif", "avif"],
        extra_compile_args={"cxx": ["-g0"]},
    )


def get_requirements():
    pytorch_dep = os.getenv("TORCH_PACKAGE_NAME", "torch")
    if os.getenv("PYTORCH_VERSION"):
        pytorch_dep += "==" + os.getenv("PYTORCH_VERSION")

    return [pytorch_dep]


if __name__ == "__main__":

    with open("README.md") as f:
        readme = f.read()

    PACKAGE_NAME = "torchvision-extra-decoders"

    setup(
        name=PACKAGE_NAME,
        version=get_and_write_version(),
        author="PyTorch Team",
        author_email="packages@pytorch.org",
        url="TODO",
        description="TODO",
        long_description=readme,
        long_description_content_type="text/markdown",
        license="LGPLv2.1",
        packages=find_packages(exclude=("test",)),
        package_data={PACKAGE_NAME: ["*.dll", "*.dylib", "*.so"]},
        zip_safe=False,
        install_requires=get_requirements(),
        python_requires=">=3.9",
        ext_modules=[make_extension()],
        cmdclass={
            "build_ext": BuildExtension.with_options(no_python_abi_suffix=True),
        },
    )
