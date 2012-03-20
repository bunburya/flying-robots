from distutils.core import setup

with open('USAGE', 'r') as f:
    long_desc = f.read()

setup(
        name='flybots',
        version='0.1.0',
        author='Alan Bunbury',
        packages=['', 'flying_robots'],
        scripts=['flybots'],
        url='https://github.com/bunburya/FlyingRobots',
        description='A 3D clone of the classic bsd-robots game.',
        long_description=long_desc,
        download_url='https://github.com/bunburya/FlyingRobots',
        platforms=['unix', 'posix', 'linux', 'bsd'],
        license='MIT License'
        )
