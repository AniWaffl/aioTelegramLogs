from setuptools import setup


setup(
    name='aioTelegramLogs',
    version='0.01',
    author='Daniel Leroy',
    description='library for logging to telegrams',
    url='https://github.com/AniWaffl/aioTelegramLogs',
    install_requires=[
        "aiohttp>=3.7.3"
    ],
    packages=['aioTelegramLogs'],
    python_requires=">=3.5"
) 