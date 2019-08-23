# Copyright FIXME

"""Package setup for launch_ros_sandbox."""

from setuptools import find_packages
from setuptools import setup

setup(
    name='launch_ros_sandbox',
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    install_requires=[
        'setuptools',
        'launch',
    ],
    zip_safe=True,
    description='Sandbox extension to ROS 2 Launch.',
    license='Apache License, Version 2.0',
    tests_require=[
        'pytest',
    ],
)
