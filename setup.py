from os import name as os_name
from distutils.core import setup
from flying_robots.metadata import (
        short_name,
        version,
        author,
        homepage_url,
        description,
        download_url,
        license_name
        )

if os_name == 'nt':
    scriptname = 'flybots.pyw'
else:
    scriptname = 'flybots'

setup(
        name=short_name,
        version=version,
        author=author,
        packages=['', 'flying_robots', 'flying_robots.ui'],
        package_data={'flying_robots.ui': ['gfx/*.gif']},
        scripts=[scriptname],
        url=homepage_url,
        description=description,
        download_url=download_url,
        license=license_name
        )
