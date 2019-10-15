from collections import namedtuple
from bs4 import BeautifulSoup as bs
from requests import get


ATRIBUTOS = {
    "url_toll": "http://www.antt.gov.br/rodovias/Pedagio.html",
    "base_url": "http://www.antt.gov.br"
}

# definindo uma namedtuple
site = namedtuple('Antt', 'site')

class Tolls:

    def format_strs(self, string: str) -> str:
        """
        :param string: string referente a determinados atributos
        :return: string sem espaços.
        """
        # remove o ':' e também os espaçoes, a partir do indice 1
        # return string.split(':')[1].strip()
        return string.strip()

    def gen_antt_concession(self, url: str) -> str:
        """
        :param url: url contendo determinada lista de pedagios
        :return: generator contendo determinada lista de concessão
        """
        page = get(url)
        bs_page = bs(page.text, 'html.parser')
        boxes = bs_page.find_all('div', {'class': 'row no-margin'})
        for box in boxes:
            try:
                titles = box.find('ul').text
                yield titles
            except Exception as err:
                print(err)
                pass

    def gen_links_for_concession(self, url: str) -> str:
        """
        :param url: pagina inicial do site antt
        :return:lista contendo determinado links
        """
        page = get(url)
        bs_page = bs(page.text, 'html.parser')
        boxe = bs_page.find_all('div', {'class': 'row no-margin'})
        tag = [link.find_all('a') for link in boxe][0]
        yield [a.get('href') for a in tag]

    def get_tam_and_links(self, url: str) -> tuple:
        """
        :param url: pagina inicial do site antt
        :return: tamanho atual/paginação e tambem uma lista contendo esses elementos;
        """
        page = get(url)
        bs_page = bs(page.text, 'html.parser')
        boxe = bs_page.find_all('div', {'class': 'row no-margin'})
        tag = [link.find_all('a') for link in boxe][0]
        tam = len([a.get('href') for a in tag])
        links = [a.get('href') for a in tag]
        return tam, links

tam, links = Tolls().get_tam_and_links(ATRIBUTOS.get('url_toll'))

for link in links:
    print(site('{}{}'.format(ATRIBUTOS.get('base_url'), Tolls().format_strs(link))))



#for box  in gen_antt_concession(ATRIBUTOS.get('url_toll')):
    #    print(box)
