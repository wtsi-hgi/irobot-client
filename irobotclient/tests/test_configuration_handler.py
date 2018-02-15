import unittest
from unittest.mock import MagicMock

import errno
import argparse
import os

from irobotclient import configuration_handler
from irobotclient.custom_exceptions import IrobotClientException


class TestConfigurationSetup(unittest.TestCase):
    """
    Assessing if the configuration and setup of the program in undertaken correctly.
    """
    def setUp(self):
        # A default argparse object to pass to the private functions.
        self._args = argparse.Namespace(input_file=None,
                                        output_dir=None,
                                        url=None,
                                        arvados_token=None,
                                        basic_username=None,
                                        basic_password=None,
                                        force=False,
                                        no_index=False,
                                        override_url=False)

        self._old_listdir = os.listdir
        os.listdir = MagicMock(spec=os.listdir)

        self._old_getenv = os.getenv
        os.getenv = MagicMock(spec=os.getenv)

    def tearDown(self):
        os.listdir = self._old_listdir
        os.getenv = self._old_getenv

    def test_config_run_with_all_args_set(self):
        """
        This test a complete run-through of configuration_handler.run(args) through getting args and validating them to
        return the correctly formatted details.

        :return:
        """

        os.listdir.return_value = ["hello", "input"]
        os.getenv.return_value = "test_url"

        args = ['/input', 'output', '-u', 'http://irobot/address', '--arvados_token', 'abc123',
                '--basic_username', 'tester', '--basic_password', 'test', '-f', '--no_index', '-o']

        self.assertEqual(configuration_handler.run(args),
                         argparse.Namespace(input_file="input",            # leading '/' removed
                                            output_dir="output/",          # trailing '/' added
                                            url="http://irobot/address/",  # trailing '/' added
                                            arvados_token="abc123",
                                            basic_username='tester',
                                            basic_password='test',
                                            force=True,                    # overwrite "input" in output_dir
                                            no_index=True,                 # don't download index files
                                            override_url=True))            # override the environment var url

    def test_config_run_with_env_vars_set_but_no_optional_args_set(self):
        """
        This test will check that the environment variables populate the argparse object.

        :return:
        """

        os.getenv.side_effect = ["test_url/", "test_token", "test_user", "test_password"]

        args = ['input', 'output/']

        self.assertEqual(configuration_handler.run(args),
                         argparse.Namespace(input_file="input",
                                            output_dir="output/",
                                            url="test_url/",                   # set via getenv
                                            arvados_token="test_token",        # set via getenv
                                            basic_username='test_user',        # set via getenv
                                            basic_password='test_password',    # set via getenv
                                            force=False,                       # default value
                                            no_index=False,                    # default value
                                            override_url=False))               # default value

    def test_config_run_with_override_url_set(self):
        """
        Test that the -o flag overrides the URL environment variable value

        :return:
        """
        os.getenv.side_effect = ["test_url/", "test_token", "test_user", "test_password", "test_url/"]

        args = ['input', 'output/', '-o']

        self.assertEqual(configuration_handler.run(args),
                         argparse.Namespace(input_file="input",
                                            output_dir="output/",
                                            url=None,                        # Environment var overrode by -o flag
                                            arvados_token="test_token",      # set via getenv
                                            basic_username='test_user',      # set via getenv
                                            basic_password='test_password',  # set via getenv
                                            force=False,                     # default value
                                            no_index=False,                  # default value
                                            override_url=True))              # Override the environment variable URL

    # The following tests assess exception handling.
    def test_input_file_is_directory_exception(self):
        self._args.input_file = "/input/"
        self.assertRaisesRegex(IrobotClientException, f'{errno.ECONNABORTED}',
                               configuration_handler._check_input_file_argument, self._args)

    def test_output_directory_not_exist_exception(self):
        # Need the os.listdir to function as normal so removing mock reference.
        os.listdir = self._old_listdir

        self._args.output_dir = "non_existant"
        self.assertRaisesRegex(OSError, "directory",
                               configuration_handler._check_output_directory_argument, self._args)

    def test_file_exist_in_output_dir_but_no_force_set_exception(self):
        os.listdir.return_value = {"hello.cram", "test.cram"}

        self._args.input_file = "test.cram"
        self._args.output_dir = "/test_dir/"
        self._args.force = False
        self.assertRaisesRegex(IrobotClientException, f"{errno.EEXIST}",
                               configuration_handler._check_output_directory_argument, self._args)

    def test_credentials_not_set_exception(self):
        self.assertRaisesRegex(IrobotClientException, f"{errno.EACCES}",
                               configuration_handler._check_authorisation_credentials, self._args)


if __name__ == '__main__':
    unittest.main()
