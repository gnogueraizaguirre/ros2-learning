from setuptools import find_packages, setup

package_name = 'my_robot_controller'

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
    description='Package for turtlesim robot control',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'my_first_node = my_robot_controller.my_first_node:main',
            'draw_circle = my_robot_controller.draw_circle:main',
            'pose_subscriber = my_robot_controller.pose_subscriber:main',
            'turtle_controller = my_robot_controller.turtle_controller:main',
            'turtle_controller_spiral = my_robot_controller.turtle_controller_spiral:main',
        ],
    },
)
