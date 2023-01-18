from setuptools import setup

setup(
    name='branchcommons',
    version='1.0',
    package_dir={'': 'src'},
    py_modules=["leafpkg", "packagebuild"],
    include_package_data=True,
    install_requires=[],
    author='zimsneexh',
    author_email='z@zsxh.eu',
    description='Common shared branch components'
)

