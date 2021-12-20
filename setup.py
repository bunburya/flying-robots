from os import name as os_name
from os.path import join
from setuptools import setup
from flying_robots.metadata import (
        app_name,
        version,
        author,
        homepage_url,
        description,
        download_url,
        license_name
)

scripts = [join('scripts', 'flying-robots')]
if os_name == 'nt':
    scripts.append(join('scripts', 'flying-robots.bat'))

setup(
        name=app_name,
        version=version,
        author=author,
        packages=['flying_robots', 'flying_robots.ui'],
        package_data={'flying_robots.ui': ['gfx/*.gif']},
        scripts=scripts,
        url=homepage_url,
        description=description,
        download_url=download_url,
        license=license_name
)
