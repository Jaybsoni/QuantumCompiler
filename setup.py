# Setup file for Quantum Compiler
from setuptools import setup

setup(name='qcompile',
      version='0.1',
      description='A simple quantum compiler',
      author='Jay Soni',
      packages=['qcompile'],
      license='MIT', install_requires=['numpy', 'qiskit']
      )
