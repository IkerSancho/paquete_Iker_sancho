from setuptools import setup

setup(
   name='paquete_Iker_Sancho',
   version='0.0.1',
   author='Iker Sancho',
   author_email='isancho007@ehu.eus',
   packages=['paquete_Iker_Sancho'],
   url='Indicar una URL para el paquete...',
   license='LICENSE.txt',
   description='This package includes some basic functions to work with datasets',
   long_description=open('README.txt').read(),
   install_requires=[
      "seaborn >= 0.13.2",
      "pandas >= 1.5.3",
      "matplotlib >= 3.6.3",
      "numpy >=1.23.3"
   ],
)