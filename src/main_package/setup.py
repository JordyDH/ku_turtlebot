import os
from glob import glob
from setuptools import setup


package_name = 'main_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
	(os.path.join('share', package_name), glob('launch/*launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jordy',
    maintainer_email='jordy.dehoon@student.kuleuven.be',
    description='THIS IS THE MAIN PACKAGE FOR THE TURTLEBOT PROJECT',
    license='THE BEER-WARE license',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
		"talker = main_package.demo_pub:main",
		"listener = main_package.demo_sub:main",
        ],
    },
)
