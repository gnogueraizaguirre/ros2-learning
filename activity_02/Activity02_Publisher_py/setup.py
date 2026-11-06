from setuptools import find_packages, setup

package_name = 'Activity02_Publisher_py'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    package_data={'': ['py.typed']},
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='gus',
    maintainer_email='g.nogueraizaguirre@gmail.com',
    description='This will publish a bunch of numbers for a cpp to count, add and publish in another topic',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'number_publisher = Activity02_Publisher_py.publisher:main'
        ],
    },
)
