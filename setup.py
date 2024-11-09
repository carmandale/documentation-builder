from setuptools import setup, find_packages

setup(
    name="documentation_builder",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'aiohttp',
        'beautifulsoup4',
        'playwright',
        'rich',
        'pytest'
    ]
) 