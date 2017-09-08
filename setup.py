from setuptools import setup, find_packages

setup(name='irobotclient',
      version='0.1',
      description='Client for the iRobot HTTP API',
      url='https://github.com/wtsi-hgi/irobot-client',
      author='Elizabeth Weatherill',
      author_email='elizabeth.weatherill@sanger.ac.uk',
      license='GNU General Public License',
      packages=find_packages(exclude=["test"]),
      entry_points={
          'console_scripts': [
              'irobotclient=irobotclient.entrypoint:main']},
      zip_safe=False)
