from setuptools import setup, find_packages
from envycontrol import envs
setup(
    name = 'EnvyControl',
    version = envs.VERSION,
    description = 'Enable or disable your Nvidia dGPU',
    url = 'https://github.com/geminis3/EnvyControl',
    author = 'Victor Bayas',
    author_email = 'victorsbayas@gmail.com',
    license = 'MIT',
    packages = find_packages(),
    entry_points = {
        'console_scripts': [
            'envycontrol = envycontrol.__main__:main'
        ]
    })
