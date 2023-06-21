from setuptools import setup, find_packages

setup(
    name='F-SEA',
    version='1.0',
    description='A description of your project',
    author='Zaria Burton',
    packages=find_packages(),
    install_requires=[
        'PyQt6',
        'pycryptodomex',
        'nltk',
    ],
    package_data={
        'F-SEA': ['src/assets/*.png'],
    },
    entry_points={
        'console_scripts': [
            'f-sea = main:main',
        ],
    },
)
