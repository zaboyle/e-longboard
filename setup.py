"""
e-longboard python package configuration.

Zach Boyle <zboyle@umich.edu>
"""

from setuptools import setup

setup(
	name='e-longboard',
    version='0.1.0',
	description='BMS and Blynk functionality for Raspberry Pi controlled e-longboard',
	author='Zach Boyle',
	author_email='zboyle@umich.edu',
	license='GPL-3.0',
	url='https://github.com/zaboyle/e-longboard',
    packages=[
		'src',
	],
    include_package_data=True,
    install_requires=[
		'adafruit-mcp3008',
        'blynklib==0.2.6',
		'PyYAML==5.3.1',
		'psutil==5.7.0',
		'pytest==4.6.9',
		'pytest-xdist==1.31.0',
    ],
)
