import unittest

from irobotclient import request_formatter


class TestRequestFormatter(unittest.TestCase):

    def test_get_authorisation_header_with_arvados(self):
        auth_token = "abc123"

        headers = request_formatter.get_header(auth_token=auth_token)
        self.assertEqual(headers["authorization"], "Arvados abc123")

    def test_get_url_request_path(self):
        irobot_url = "http://test/address/"
        input_file = "some/address/in/irods/file.txt"

        url = request_formatter.get_url_request_path(irobot_url, input_file)
        self.assertEqual(url, "http://test/address/some/address/in/irods/file") # Note the missing extension.

    def test_get_file_extensions_with_index_for_cram(self):
        input_file = "/some/address/in/irods/file.cram"

        extensions = request_formatter.get_file_extensions(input_file, False)

        self.assertEqual(extensions, [".cram", ".crai"])

    def test_get_file_extensions_with_index_for_bam(self):
        input_file = "/some/address/in/irods/file.bam"

        extensions = request_formatter.get_file_extensions(input_file, False)

        self.assertEqual(extensions, [".bam", ".bai", ".pbi"])

    def test_get_file_extensions_without_index_for_bam(self):
        input_file = "/some/address/in/irods/file.bam"

        extensions = request_formatter.get_file_extensions(input_file, True)

        self.assertEqual(extensions, [".bam"])

    def test_get_file_extension_without_input_extension(self):
        input_file = "/some/address/in/irods/file"

        extensions = request_formatter.get_file_extensions(input_file, False)

        self.assertEqual(extensions, [])

    def test_get_file_extension_with_common_extension(self):
        input_file = "/some/address/in/irods/file.txt"

        extensions = request_formatter.get_file_extensions(input_file, False)

        self.assertEqual(extensions, [".txt"])


if __name__ == '__main__':
    unittest.main()
