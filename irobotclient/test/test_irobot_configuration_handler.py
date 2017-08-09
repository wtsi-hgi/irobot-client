import unittest
from unittest.mock import MagicMock

import errno
import argparse
import os

from irobotclient import configuration_handler
from irobotclient.custom_exceptions import IrobotClientException

class TestConfigurationSetup(unittest.TestCase):

    def setUp(self):
        self._parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        self._parser.add_argument("input_file", default="input")
        self._parser.add_argument("output_dir", default="output")
        self._parser.add_argument("-u", "--url")
        self._parser.add_argument("-t", "--token")
        self._parser.add_argument("-f", "--force", default=False, action="store_true")
        self._parser.add_argument("--no_index", default=False, action="store_true")

        self._old_listdir = os.listdir
        os.listdir = MagicMock(spec=os.listdir)

    def tearDown(self):
        os.listdir = self._old_listdir

    def test_config_run(self):
        """
        This test a complete run-through of configuration_handler.run() through getting args and validating them to
        return the correctly formatted details.

        :return:
        """
        old_parse_args = argparse.ArgumentParser.parse_args
        argparse.ArgumentParser.parse_args = MagicMock(spec=argparse.ArgumentParser.parse_args)
        argparse.ArgumentParser.parse_args.return_value = argparse.Namespace(input_file="/input",
                                                                             output_dir="output",
                                                                             url="http://irobot/address",
                                                                             token="abc123",
                                                                             force=True,
                                                                             no_index=True)

        os.listdir.return_value = ["hello", "input"]

        self.assertEqual(configuration_handler.run(),
                         argparse.Namespace(input_file="input",            # leading '/' removed
                                            output_dir="output/",          # trailing '/' added
                                            url="http://irobot/address/",  # trailing '/' added
                                            token="abc123",
                                            force=True,                    # overwrite "input" in output_dir
                                            no_index=True))                # don't download index files

        argparse.ArgumentParser.parse_args = old_parse_args

    # The following test assess more granular details of the configuration handler.
    def test_input_file_slash_removal(self):
        args = self._parser.parse_args(["/some/place/on/irods/input.cram", None])
        configuration_handler._check_input_file_argument(args)
        self.assertFalse(args.input_file.startswith('/'))

    def test_input_file_directory_exception(self):
        args = self._parser.parse_args(["/some/place/on/irods/input/", None])
        self.assertRaisesRegex(IrobotClientException, f'{errno.ECONNABORTED}',
                               configuration_handler._check_input_file_argument, args)

    def test_output_directory_formatting(self):
        os.listdir.return_value = []

        args = self._parser.parse_args(["", "~/some/output/dir"])
        configuration_handler._check_output_directory_argument(args)
        self.assertTrue(os.path.isabs(args.output_dir))
        self.assertTrue(args.output_dir.endswith('/'))

    def test_output_directory_not_exist(self):
        # Need the os.listdir to function as normal for this test to work so removing mock reference.
        os.listdir = self._old_listdir

        args = self._parser.parse_args(["", "~/some/output/dir"])
        self.assertRaisesRegex(OSError, "directory",
                               configuration_handler._check_output_directory_argument, args)

    def test_file_exist_in_output_dir_with_extension_and_no_overwrite(self):
        os.listdir.return_value = {"hello.cram", "test.cram", "file.cram", "one.cram"}

        args = self._parser.parse_args(["file.cram", "~/some/output/dir"])
        self.assertRaisesRegex(IrobotClientException, f"{errno.EEXIST}",
                               configuration_handler._check_output_directory_argument, args)


    def test_file_overwrite_in_output_dir_with_extension(self):
        os.listdir.return_value = {"hello.cram", "test.cram", "file.cram", "one.cram"}

        args = self._parser.parse_args(["file.cram", "~/some/output/dir", "-f"])
        configuration_handler._check_output_directory_argument(args)
        self.assertTrue(args.output_dir.endswith('/'))

    def test_file_exist_in_output_directory_with_no_extensions_and_no_overwrite(self):
        os.listdir.return_value = {"hello", "test", "file", "one"}

        args = self._parser.parse_args(["file", "~/some/output/dir"])
        self.assertRaisesRegex(IrobotClientException, f"{errno.EEXIST}",
                               configuration_handler._check_output_directory_argument, args)

    def test_url_as_none(self):
        args = self._parser.parse_args(["", "", "-u", None])

        self.assertRaisesRegex(IrobotClientException, f"{errno.ENOKEY}",
                               configuration_handler._check_url_argument, args)

    def test_url_set_as_argument(self):
        args = self._parser.parse_args(["", "", "-u", "https//irobot/address/"])

        configuration_handler._check_url_argument(args)
        self.assertEqual(args.url, "https//irobot/address/")

    def test_url_set_as_environ(self):
        args = self._parser.parse_args(["", "", "-u", None])
        os.environ['IROBOTURL'] = "http://irobot/address/"

        configuration_handler._check_url_argument(args)
        self.assertEqual(args.url, "http://irobot/address/")

    def test_url_formatting(self):
        args = self._parser.parse_args(["", "", "-u", "https//irobot"])

        configuration_handler._check_url_argument(args)
        self.assertTrue(args.url.endswith('/'))

    def test_auth_token_set_as_none(self):
        """
        Note: this shouldn't fail because the authorisation method could be Basic type and this will be
        handled at runtime.

        :return:
        """
        args = self._parser.parse_args(["", "", "-t", None])

        configuration_handler._check_authorisation_token(args)
        self.assertTrue(args.token, None)

    def test_arvados_token_set_as_argument(self):
        args = self._parser.parse_args(["", "", "-t", "abc123"])

        configuration_handler._check_authorisation_token(args)
        self.assertTrue(args.token, "abc123")

    def test_arvados_token_set_as_environ(self):
        args = self._parser.parse_args(["", "", "-t", None])
        os.environ['ARVADOSTOKEN'] = "abc123"

        configuration_handler._check_authorisation_token(args)
        self.assertTrue(args.token, "abc123")


if __name__ == '__main__':
    unittest.main()
