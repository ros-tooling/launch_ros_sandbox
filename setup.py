# Copyright FIXME

""" 
"""

from setuptools import find_packages
from setuptools import setup

setup(
    name = 'launch_ros_sandbox',
    version = '0.1.0',
    packages = find_packages(exclude=['test']),
    install_requires = [
        'setuptools',
        'launch',
    ],
    zip_safe = True,
    description = 'Extension for Launch for delegating ROS 2 Launches into a sandboxed environment',
    license = 'Apache License, Version 2.0',
    tests_require = [
        'pytest',
    ],
)