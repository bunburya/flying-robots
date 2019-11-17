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

if os_name == 'nt':
    scriptname = join('scripts', 'flying-robots.pyw')
else:
    scriptname = join('scripts', 'flying-robots')

setup(
        name=app_name,
        version=version,
        author=author,
        packages=['flying_robots', 'flying_robots.ui'],
        package_data={'flying_robots.ui': ['gfx/*.gif']},
        scripts=[scriptname],
        url=homepage_url,
        description=description,
        download_url=download_url,
        license=license_name
        )
