'''
Nebula Expired Article Hunter: article scraper for the wayback machine.
Copyright (C) 2021  Eneiro A. Matos B.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

from configparser import ConfigParser

config_file = ConfigParser()
config_file.read('config.ini', encoding='utf-8')

min_word_len = int(config_file.get('Word Limits', 'min_word_count'))
max_word_len = int(config_file.get('Word Limits', 'max_word_count'))

user_agent = config_file.get('Network and Connection', 'user_agent')
request_time_out = int(config_file.get('Network and Connection', 'request_time_out'))

domain_list = config_file.get('Files and Directories', 'domain_list')
log = config_file.get('Files and Directories', 'log')
projects_folder = config_file.get('Files and Directories', 'projects_folder')
