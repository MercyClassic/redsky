from setuptools import find_packages, setup

VERSION = '1.0.0'


setup(
    name='RedSky',
    version=VERSION,
    packages=find_packages(),
    package_dir={'redsky': 'redsky'},
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/MercyClassic/redsky',
    author='MercyClassic',
    requires=[],
)
