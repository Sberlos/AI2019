from distutils.core import setup
from Cython.Build import cythonize

sourcefiles = ["run.pyx", "src/*.pyx"]
setup(ext_modules = cythonize(sourcefiles,
    compiler_directives={'language_level': 3}),)
