# iRobot Client

Basic [iRobot](https://github.com/wtsi-hgi/irobot) client to interact with the iRobot HTTP API.  The client is wrapped in [Common Workflow Language](http://www.commonwl.org/v1.0/) for integration with Arvados and other applications.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

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

Alternatively in a Docker container nut *without* test resources:
```
docker run -it mercury/irobot-client
```

Check that the iRobot-Client works:
```
irobotclient test_text.txt <output_directory_name> -u https://github.com/wtsi-hgi/irobot-client/tree/develop/ --arvados_token abc123 -f
```

### Usage
- [ ] Describe CLI usage
- [ ] Describe CWL usage

## Running the tests
- [ ] Update unittests
- [ ] Create automated test script for cwl?
- [ ] Explain how to run the automated tests for this system

### And coding style tests

- [ ] This project follows the unittest and PEP8 coding style.


## Deployment

- [ ] Add additional notes about how to deploy this on a live system


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

