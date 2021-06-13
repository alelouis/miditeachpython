from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='miditeach',
    version='0.5',
    description='miditeach',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/alelouis/midiTeach',
    author='Alexis LOUIS',
    author_email='alelouis.dev@gmail.com',
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['miditeach=miditeach.miditeach:main'],
    },
    install_requires=[
        'arcade',
        'python-rtmidi',
        'mido'
    ],
    include_package_data=True,
    zip_safe=False)