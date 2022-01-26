from setuptools import setup, find_packages

with open('README.md', 'r') as stream:
    long_description = stream.read()

setup(
    name='ed-amino',
<<<<<<< HEAD
    version='0.7.1.6',
=======
    version='0.7.1.4',
>>>>>>> a62cef8317410d60b6e04c2746252c7c5576ab39
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
        'pydantic'
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    packages=find_packages()
)
