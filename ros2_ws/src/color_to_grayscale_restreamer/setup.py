from setuptools import find_packages, setup
import os
from glob import glob
package_name = 'color_to_grayscale_restreamer'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
         glob(os.path.join('launch', '*.launch.py'))),
    ],
    install_requires=['setuptools',
                      'numpy',],
    zip_safe=True,
    maintainer='anto',
    maintainer_email='antoronson590@gmail.com',
    description='Node that transforms color image to grayscale',
    license='Apache_2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'pub_grayscale = color_to_grayscale_restreamer.py_color2grayscale:main',
        ],
    },
)
