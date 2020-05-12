from setuptools import setup
from setuptools import find_packages

setup(
    name='QtGrab',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    url='https://github.com/AlexanderBerx/QtGrab',
    license='MIT',
    author='Alexander Berx',
    author_email='alexanderberx@hotmail.com',
    description='Screen grab widget for PySide2',
    install_requires=['PySide2'],
    entry_points={'console_scripts': ['qtgrab=qtgrab.sample:main']}
)
