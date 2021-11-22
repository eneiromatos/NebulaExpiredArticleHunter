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

import re
import requests
import config


class WaybackmachineUrls:
    def __init__(self, domain: str):
        self.domain = domain.casefold().removesuffix('\n')

    def get_url_list(self) -> tuple[str]:
        exeption_rules = ['.jpg', '.txt', '.js', '.css', '.png', '.gif', '.xml', '.cgi', '.ico',
                          '.php', '/wp-', '/comments', '/feed', '/cat', '/page', '/tag',
                          '/author', '/trackback', '/contact', '/aviso-', '/politica-', 'comment-page', '/privacy',
                          '=', '/amp', '/js', '//', '?', '/media', '.svg', '/fonts', '/theme', '/template', '/search',
                          '/buscar', '/busqueda', '/nosotros', '/cgi', '/cdn', '/img', '.asp', '.jsp', '/photos/',
                          '/images/', '/sample-page', '/cookies-policy', '/user/', '/users/', '/fotos/', '/images/',
                          '/products/', '/product/', '/producto/', '/productos/', '/shop/', '/tienda/', '/usuario/',
                          '/user/', '/usuarios/', '/users/', '/catalogo/', '/admin/']
        clean_url_list = list()
        header = {'user-agent': config.user_agent}
        wburl = f'https://web.archive.org/cdx/search/cdx?url={self.domain}*' \
                f'&statuscode=200&filter=mimetype:text/html&fl=original&output=txt'
        req = requests.get(wburl, headers=header)
        urllist = [url.replace(':80', '').removeprefix('http://').removeprefix('https://').removesuffix('/').casefold()
                   for url in req.text.split('\n')]
        urllist = set(urllist)

        for url in urllist:
            is_good_url = True
            for rule in exeption_rules:
                if url.find(rule) > -1 or url == '' or re.search(r'[^a-zA-Z0-9/:.-]', url) is not None:
                    is_good_url = False
                    break
            if is_good_url:
                clean_url_list.append(url)

        clean_url_list.sort()
        return tuple(clean_url_list)
