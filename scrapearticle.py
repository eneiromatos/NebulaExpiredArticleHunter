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

import os
import re
from newspaper import Article
from newspaper import Config
import config


class ScrapeArticle:
    def __init__(self, url: str, url_dir: str):
        self.url = url
        self.__title = str()
        self.__domain_dir = url_dir
        self.__wburl = 'https://web.archive.org/web/19900101/' + url
        self.__word_count = int()

    def __scrape_article(self) -> str:
        wburl = self.__wburl

        # Configuration for Newspaper.Article instance
        conf = Config()
        conf.fetch_images = False
        conf.browser_user_agent = config.user_agent
        conf.request_timeout = config.request_time_out

        article = Article(wburl, config=conf)
        article.download()
        article.parse()
        self.__word_count = len(f'{article.text} {article.title}'.strip().split(' '))
        if self.__word_count < config.min_word_len or self.__word_count > config.max_word_len:
            return None
        self.__title = article.title
        return article.title + '\n' + article.text

    def create_article_file(self):
        article = self.__scrape_article()
        if article is None:
            return None
        projects_dir = 'projects'
        domain_dir = self.__domain_dir.replace('/', '').replace(':', '_').replace('\n', '')
        current_dir = projects_dir + '/' + domain_dir
        filename = f'{self.__title} {self.__word_count} words'
        #replace any special character with space
        filename = re.sub(r"\W+|_", " ", filename).removesuffix(' ').removeprefix(' ') + '.txt'
        save_patch = f'{current_dir}/{filename}'

        if not os.path.exists(projects_dir):
            os.mkdir(projects_dir)

        if not os.path.exists(projects_dir + '/' + domain_dir):
            os.mkdir(projects_dir + '/' + domain_dir)

        with open(save_patch, mode='w', encoding='utf-8') as txt:
            txt.write(article)
