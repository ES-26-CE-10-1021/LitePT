import os
import torch
from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension

# Get the path to the torch/lib directory where libc10.so lives
# This ensures we can bake the RPATH into the binary
lib_dir = os.path.join(os.path.dirname(torch.__file__), "lib")

setup(
    name='pointrope',
    ext_modules=[
        CUDAExtension(
            name='pointrope',
            sources=[
                "pointrope.cpp",
                "kernels.cu",
            ],
            # We omit all_cuda_archs here. 
            # CUDAExtension automatically respects the TORCH_CUDA_ARCH_LIST 
            # environment variable if it is set in your shell.
            extra_compile_args={
                'nvcc': ['-O3', '--ptxas-options=-v', '--use_fast_math'],
                'cxx': ['-O3']
            },
            # This embeds the path to PyTorch libraries so the OS can find libc10.so
            extra_link_args=[f'-Wl,-rpath,{lib_dir}'],
            runtime_library_dirs=[lib_dir]
        )
    ],
    cmdclass={
        'build_ext': BuildExtension
    }
)
