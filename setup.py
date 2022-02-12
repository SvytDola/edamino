from setuptools import setup, find_packages
from re import search

with open(f'edamino/__init__.py') as f:
    __version__ = search(r'.[0-9].[0-9].[0-9].[0-9]', f.read()).group()[1:]

with open('README.md', 'r') as stream:
    long_description = stream.read()

setup(
    name='ed-amino',
    version=__version__,
    url='https://github.com/SvytDola/edamino',
    license='MIT',
    author='SvytDola',
    description='Async library for amino.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=[
        'edamino'
    ],
    install_requires=[
        'aiohttp',
        'ujson',
        'python-dotenv',
        'pydantic',
        'aiofile'
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    packages=find_packages()
)
