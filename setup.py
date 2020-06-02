from setuptools import setup, find_packages,find_namespace_packages

setup(
    name='utils',
    version='0.0.3',
    url='',
    packages=find_namespace_packages(),


    install_requires=["azure-storage-blob==1.5.0","kubernetes","requests"],
    license='',
    author='shubham mishra',
    author_email='shubhammishra920816@gmail.com',
    description='This package contains common utilities used across all the repos'
)

