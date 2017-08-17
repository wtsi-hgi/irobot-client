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
        # A default argparse object to pass to the tested functions.
        self._args = argparse.Namespace(input_file="file.cram",
                                        output_dir="~/some/output/dir",
                                        url="http://irobot/address/",
                                        token="abc123",
                                        force=True,
                                        no_index=True)

        self._old_listdir = os.listdir
        os.listdir = MagicMock(spec=os.listdir)

    def tearDown(self):
        os.listdir = self._old_listdir

    def test_config_run(self):
        """
        This test a complete run-through of configuration_handler.run(args) through getting args and validating them to
        return the correctly formatted details.

        :return:
        """

        os.listdir.return_value = ["hello", "input"]

        args = ['/input', 'output/', '-u', 'http://irobot/address', '-t', 'abc123', '-f', '--no_index']

        self.assertEqual(configuration_handler.run(args),
                         argparse.Namespace(input_file="input",            # leading '/' removed
                                            output_dir="output/",          # trailing '/' added
                                            url="http://irobot/address/",  # trailing '/' added
                                            token="abc123",
                                            force=True,                    # overwrite "input" in output_dir
                                            no_index=True))                # don't download index files

    # The following test assess more granular details of the configuration handler.
    def test_input_file_slash_removal(self):
        self._args.input_file = '/input.cram'
        configuration_handler._check_input_file_argument(self._args)
        self.assertFalse(self._args.input_file.startswith('/'))

    def test_input_file_directory_exception(self):
        self._args.input_file = "/input/"
        self.assertRaisesRegex(IrobotClientException, f'{errno.ECONNABORTED}',
                               configuration_handler._check_input_file_argument, self._args)

    def test_output_directory_formatting(self):
        os.listdir.return_value = []

        configuration_handler._check_output_directory_argument(self._args)
        self.assertTrue(os.path.isabs(self._args.output_dir))
        self.assertTrue(self._args.output_dir.endswith('/'))

    def test_output_directory_not_exist(self):
        # Need the os.listdir to function as normal for this test to work so removing mock reference.
        os.listdir = self._old_listdir

        self.assertRaisesRegex(OSError, "directory",
                               configuration_handler._check_output_directory_argument, self._args)

    def test_file_exist_in_output_dir_with_extension_and_no_overwrite(self):
        os.listdir.return_value = {"hello.cram", "test.cram", "file.cram", "one.cram"}

        self._args.force = False
        self.assertRaisesRegex(IrobotClientException, f"{errno.EEXIST}",
                               configuration_handler._check_output_directory_argument, self._args)

    def test_file_overwrite_in_output_dir_with_extension(self):
        os.listdir.return_value = {"hello.cram", "test.cram", "file.cram", "one.cram"}

        self._args.force = True
        configuration_handler._check_output_directory_argument(self._args)
        self.assertTrue(self._args.output_dir.endswith('/')) # TODO - I think this test could be tighter or have explaination

    def test_file_exist_in_output_directory_with_no_extensions_and_no_overwrite(self):
        os.listdir.return_value = {"hello", "test", "file", "one"}

        self._args.input_file = "file"
        self._args.force = False
        self.assertRaisesRegex(IrobotClientException, f"{errno.EEXIST}",
                               configuration_handler._check_output_directory_argument, self._args)

    def test_url_as_none(self):
        self._args.url = None

        self.assertRaisesRegex(IrobotClientException, f"{errno.ENOKEY}",
                               configuration_handler._check_url_argument, self._args)

    def test_url_set_as_argument(self):
        self._args.url = "https//irobot/address/"

        configuration_handler._check_url_argument(self._args)
        self.assertEqual(self._args.url, "https//irobot/address/")

    def test_url_set_as_environ(self):
        self._args.url = None
        os.environ['IROBOT_URL'] = "http://irobot/address/"

        configuration_handler._check_url_argument(self._args)
        self.assertEqual(self._args.url, "http://irobot/address/")

    def test_url_formatting(self):
        self._args.url = "https//irobot"

        configuration_handler._check_url_argument(self._args)
        self.assertTrue(self._args.url.endswith('/'))

    def test_auth_token_set_as_none(self):
        """
        Note: this shouldn't fail because the authorisation method could be Basic type and this will be
        handled at runtime.

        :return:
        """
        self._args.token = None

        configuration_handler._check_authorisation_token(self._args)
        self.assertTrue(self._args.token, None)

    def test_arvados_token_set_as_argument(self):
        self._args.token = "abc123"

        configuration_handler._check_authorisation_token(self._args)
        self.assertTrue(self._args.token, "abc123")

    def test_arvados_token_set_as_environ(self):
        self._args.token = None
        os.environ['ARVADOS_TOKEN'] = "abc123"

        configuration_handler._check_authorisation_token(self._args)
        self.assertTrue(self._args.token, "abc123")


if __name__ == '__main__':
    unittest.main()
