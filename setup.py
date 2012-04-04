from distutils.core import setup
from flying_robots.metadata import (
        short_name,
        version,
        author,
        homepage_url,
        description,
        download_url,
        license
        )

setup(
        name=short_name,
        version=version,
        author=author,
        packages=['', 'flying_robots'],
        scripts=['flybots'],
        url=homepage_url,
        description=description,
        download_url=download_url,
        platforms=['unix', 'posix', 'linux', 'bsd'],
        license=license
        )
