"""
Copyright (c) 2017 Genome Research Ltd.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
Public License for more details.

You should have received a copy of the GNU General Public License along
with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import os
import json


class ConfigurationData:

    def __init__(self):

        _system_conf = '/etc/irobot.conf'
        _user_conf = '~/.irobot.conf'

        try:
            if os.path.exists(_system_conf):
                config_file = open(_system_conf, mode='r')
            elif os.path.exists(_user_conf):
                config_file = open(_user_conf, mode='r')

            config_data = json.load(config_file)
            config_file.close()
        except:
            print("ERROR: No .irobot.conf file found.  Please create one with vi ~/.irobot.conf\n"
                  "For more details on the config file please see:\n"
                  "https://github.com/wtsi-hgi/irobot-client")
            exit()

        self._arvados_token = config_data["arvados_token"]
        self._irobot_url = config_data["irobot_address"]
        self._input_file_extensions = config_data["file_extensions"]

    @property
    def irobot_url(self):
        return self._irobot_url

    @property
    def arvados_token(self):
        return self._arvados_token

    @property
    def input_file_extensions(self):
        return self._input_file_extensions

