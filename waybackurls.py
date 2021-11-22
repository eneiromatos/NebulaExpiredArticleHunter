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
