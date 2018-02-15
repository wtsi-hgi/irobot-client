from setuptools import setup, find_packages

try:
    from pypandoc import convert
    def read_markdown(file: str) -> str:
        return convert(file, "rst")
except ImportError:
    def read_markdown(file: str) -> str:
        return open(file, "r").read()


setup(name="irobotclient",
      version="1.0.0",
      description="Client for the iRobot HTTP API",
      url="https://github.com/wtsi-hgi/irobot-client",
      author="Elizabeth Weatherill",
      author_email="elizabeth.weatherill@sanger.ac.uk",
      license="GNU General Public License",
      packages=find_packages(exclude=["test"]),
      install_requires=open("requirements.txt", "r").readlines(),
      entry_points={
          "console_scripts": [
              "irobotclient=irobotclient.entrypoint:main"
          ]
      },
      zip_safe=True)
