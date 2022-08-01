from setuptools import setup, find_packages

setup(
    name='pizzabox',
    packages=find_packages(),
    install_requires=[
        'click==8.1.3',
        'importlib-metadata==4.12.0',
        'lxml==4.9.1',
        'typing-extensions==4.3.0',
        'zipp==3.8.1'
    ],
    version='0.1.0',
    entry_points={
        'console_scripts': [
            'pizzabox = package.main:main'
        ]
    },
)