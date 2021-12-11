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

import sys
import time
import waybackurls
import scrapearticle
import os
import config

if not os.path.exists(config.domain_list):
    with open(config.domain_list, mode='w') as working_file:
        print(f'File {config.domain_list} has been created, put you expired domains there.')
        input('Press any key to exit.')
    sys.exit()

with open(config.domain_list, mode='r') as domains:
    domains.seek(0)
    domains = domains.readlines()
    print(f'{len(domains)} domains will be processed, this may take some time, please be patient.')
    input('Press any key to continue.')
    for domain in domains:
        if domain in ('', ' ', '/n', None):
            continue
        domain = domain.casefold().strip('\n').strip()
        try:
            urls = waybackurls.WaybackmachineUrls(domain)
            urls_to_scrape = urls.get_url_list()
        except Exception as err:
            with open(config.log, mode='a') as log:
                log.write(f'{domain} - {time.ctime()}:\nError: {err}\n\n')
            continue
        print(f'\nExploring {len(urls_to_scrape)} URLS in {domain}')
        for num, url in enumerate(urls_to_scrape):
            print(f'{num+1}: Exploring {url}')
            try:
                article = scrapearticle.ScrapeArticle(url, domain)
                article.create_article_file()
            except Exception as err:
                with open(config.log, mode='a') as log:
                    log.write(f'{domain} - {time.ctime()}:\nError: {err}\n\n')

    input('\nThe process has finished, press any key to exit.')
