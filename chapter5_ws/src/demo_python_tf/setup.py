from setuptools import find_packages, setup

package_name = 'demo_python_tf'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jason',
    maintainer_email='quietjosen@example.com',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'static_tf2_broadcaster = demo_python_tf.static_tf2_broadcaster:main',
            'dynamic_tf2_broadcaster = demo_python_tf.dynamic_tf2_broadcaster:main',
            'tf2_listener = demo_python_tf.tf2_listener:main',
        ],
    },
)
