from setuptools import find_packages, setup

package_name = 'turtle_catch_them_all'

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
    description='Aplicaction for controlling a turtle dynamically. This package spawns 5 or so turtles randomly in turtlesim and the main turtle has to path towards them and despawn them',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'turtle_spawner = turtle_catch_them_all.turtle_spawner:main',
            'turtle_controller = turtle_catch_them_all.my_turtle_controller:main'
        ],
    },
)
