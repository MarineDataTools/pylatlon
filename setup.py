from setuptools import setup
import os

ROOT_DIR='pylatlon'
with open(os.path.join(ROOT_DIR, 'VERSION')) as version_file:
    version = version_file.read().strip()

setup(name='pylatlon',
      version=version,
      description='Tools to handle geographic positions (parsing, gui input)',
      url='https://github.com/MarineDataTools/pylatlon',
      author='Peter Holtermann',
      author_email='peter.holtermann@io-warnemuende.de',
      license='GPLv03',
      packages=['pylatlon'],
      scripts = [],
      entry_points={},
      package_data = {'':['VERSION']},
      zip_safe=False)


# TODO Depends on pyproj
