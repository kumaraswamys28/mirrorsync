from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='mirrorsync',
    version='1.0.0',
    description='A command-line tool to sync files between devices on a network.',
    packages=find_packages(),
    install_requires=required,
    entry_points={
        'console_scripts': [
            'sync-server = mirrorsync_pkg.server:main',
            'sync-client = mirrorsync_pkg.client:main',
        ],
    },
)
