from configparser import ConfigParser

config_file = ConfigParser()
config_file.read('config.ini', encoding='utf-8')

min_word_len = int(config_file.get('Word Limits', 'min_word_count'))
max_word_len = int(config_file.get('Word Limits', 'max_word_count'))

user_agent = config_file.get('Network and Connection', 'user_agent')
request_time_out = int(config_file.get('Network and Connection', 'request_time_out'))
