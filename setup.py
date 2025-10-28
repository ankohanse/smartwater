import unasyncd
import setuptools

setuptools.setup(
    cmdclass={'build_py': unasyncd.cmdclass_build_py()},
)