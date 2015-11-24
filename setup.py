from setuptools import setup, find_packages

name = 'two1tools'
version = '0.0.1'

setup(
    name=name,
    version=version,
    packages=find_packages(),
    description='Tools for the 21 Bitcoin Computer',
    author='Ian Chen',
    author_email='bitcoinfees@gmail.com',
    license='MIT',
    url='https://github.com/bitcoinfees/two1tools',
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'sendsats = two1tools.bittransfer:send_bittransfer_cli'
        ]
    },
)
