# iRobot Client

Basic [iRobot](https://github.com/wtsi-hgi/irobot) client to interact with the iRobot HTTP API.  The client has a [Common Workflow Language](http://www.commonwl.org/v1.0/) wrapper for integration with Arvados and other applications if needed.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine or in a Docker container for development and testing purposes.

### Prerequisites

What things you need to install the software: 
- python 3.6 


### Installing

From GitHub:
```
git clone https://github.com/wtsi-hgi/irobot-client.git
cd irobot-client
python setup.py install
```

Alternatively in a Docker container but *without* test resources (CANNOT run the cwl inside the irobot-client container):
```
docker run -it mercury/irobot-client
```

Check that the iRobot-Client works:
```
irobotclient test_text.txt <output_directory_name> -u https://github.com/wtsi-hgi/irobot-client --arvados_token abc123 -f
```
The above command should give a warning about not validating the Checksum; checksum validation is a feature supported when using the client against the iRobot server.'

### Usage
####Command line interface
```
usage: irobotclient [options] INPUT_FILE OUTPUT_DIR

Command line interface for iRobot HTTP requests

positional arguments:
  input_file            path and name of input file
  output_dir            path of output directory

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     Use this tag if no irobot URL is set as an environment variable {IROBOT_URL}. URL scheme, domain and port for irobot. EXAMPLE: http://irobot:5000/
  --arvados_token ARVADOS_TOKEN
                        Arvados authentication token; if not supplied here it will be sourced from the environment {ARVADOS_TOKEN} or default to an
  --basic_username BASIC_USERNAME
                        Basic authentication username; if not supplied here it will be sourced from the environment {BASIC_USERNAME} then, failing that, current system user
  --basic_password BASIC_PASSWORD
                        Basic authentication password; if not supplied here it will be sourced from the environment {BASIC_PASSWORD}
  -f, --force           force overwrite output file if it already exists
  --no_index            Do not download index files for CRAM/BAM files

```
####Common Workflow Language (CWL)
 
The below commands run the cwl wrapper passing in the example YAML file defining program argument values.
```
cd cwl
pip install -r cwl_requirements.txt
cwl-runner cwl_wrapper.cwl config_example.yml
```
The above command should return a test_text.txt file to your working directory.  To specify a different output directory use the cwl-runner `--outdir OUTDIR` option.

## Deployment

Values required for the client can be passed in as arguments on the command line, a YAML file when using CWL, or the following can be set as environment variables:
```
IROBOT_URL      -   URL scheme, domain and port for irobot. EXAMPLE: http://irobot:5000/
ARVADOS_TOKEN   -   Arvados authentication token
BASIC_USERNAME  -   Basic authentication username
BASIC_PASSWORD  -   Basic authentication password
```

## Running the tests
- [ ] TODO: Update unittests
- [ ] TODO: Create automated test script for cwl
- [ ] TODO: Explain how to run the automated tests for this system

### And coding style tests

- [ ] TODO: This project follows the unittest and PEP8 coding style.


## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/wtsi-hgi/irobot-client/releases). 

## Authors

* [Elizabeth Weatherill](https://github.com/EWeatherill)

See also the list of [contributors](https://github.com/wtsi-hgi/irobot-client/graphs/contributors) who participated in this project.

## License

This project is licensed under the GNU General Public License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* [Chris Harrison](https://github.com/Xophmeister) - iRobot developer
* [Colin Nolan](https://github.com/colin-nolan) - Code reviewer
* [Josh Randall](https://github.com/jrandall) - Team lead
* [Billie Thompson](https://github.com/PurpleBooth) - [README template](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* Stack Overflow

