import sys
import time
import waybackurls
import scrapearticle
import os

if not os.path.exists('domains_list.txt'):
    with open('domains_list.txt', mode='w') as working_file:
        print('Se ha creado el archivo domains_list.txt debe poblarlo con sus dominios'
              ' y ejecutar nuevamente el programa')
        input('Presione una tecla para salir')
    sys.exit()

with open('domains_list.txt', mode='r') as domains:
    for domain in domains:
        if domain == '\n':
            continue
        try:
            urls = waybackurls.WaybackmachineUrls(domain)
            urls_to_scrape = urls.get_url_list()
        except Exception as err:
            with open('error_log.txt', mode='a') as log:
                log.write(domain + '\n' + time.ctime() + str(err) + '\n'*2)
            continue
        print(f'Explorando {len(urls_to_scrape)} URLS en {domain}')
        for num, url in enumerate(urls_to_scrape):
            print(f'{num+1}: Explorando {url}')
            try:
                article = scrapearticle.ScrapeArticle(url, domain)
                article.create_article_file()
            except Exception as err:
                with open('error_log.txt', mode='a') as log:
                    log.write(f'{time.ctime()}\n'
                              f'Error in: {url}\n'
                              f'Error: {str(err)}\n\n')

    input('Presione una tecla para salir')
