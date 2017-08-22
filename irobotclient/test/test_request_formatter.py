import unittest

from requests.auth import HTTPBasicAuth

from irobotclient import request_formatter


class TestRequestFormatter(unittest.TestCase):
    """
    Test case to check if the requests are formatted and built correctly.
    """
    def test_get_authorisation_strings(self):
        auth_token = "abc123"
        username = "tester"
        password = "password"

        auth_strings = request_formatter._get_authentication_strings(arvados_token=auth_token,
                                                                     basic_username=username,
                                                                     basic_password=password)

        basic_auth = HTTPBasicAuth(username, password)
        self.assertEqual(auth_strings, {'Arvados': f"Arvados {auth_token}",
                                        'Basic': f"Basic {basic_auth}"})

    def test_get_url_request_path(self):
        irobot_url = "http://test/address/"
        input_file = "some/address/in/irods/file.txt"

        url = request_formatter.get_url_request_path(irobot_url, input_file)
        self.assertEqual(url, "http://test/address/some/address/in/irods/file") # Note the missing extension.

    def test_get_file_list_with_index_for_cram(self):
        input_file = "/some/address/in/irods/file.cram"

        file_list = request_formatter.get_file_list(input_file, False)

        self.assertEqual(file_list, ["/some/address/in/irods/file.cram", "/some/address/in/irods/file.crai"])

    def test_get_file_list_with_index_for_bam(self):
        input_file = "/some/address/in/irods/file.bam"

        file_list = request_formatter.get_file_list(input_file, False)

        self.assertEqual(file_list, ["/some/address/in/irods/file.bam",
                                     "/some/address/in/irods/file.bai",
                                     "/some/address/in/irods/file.pbi"])

    def test_get_file_list_without_index_for_bam(self):
        input_file = "/some/address/in/irods/file.bam"

        file_list = request_formatter.get_file_list(input_file, True)

        self.assertEqual(file_list, [input_file])

    def test_get_file_list_without_input_extension(self):
        input_file = "/some/address/in/irods/file"

        file_list = request_formatter.get_file_list(input_file, False)

        self.assertEqual(file_list, [input_file])

    def test_get_file_list_with_common_extension(self):
        input_file = "/some/address/in/irods/file.txt"

        file_list = request_formatter.get_file_list(input_file, False)

        self.assertEqual(file_list, [input_file])


if __name__ == '__main__':
    unittest.main()
