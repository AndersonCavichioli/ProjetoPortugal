import requests
from bs4 import BeautifulSoup
import pandas as pd
import math

url = 'https://www.imovirtual.com/arrendar/apartamento/'

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"}

site = requests.get(url, headers=headers)
soup = BeautifulSoup(site.content, 'html.parser')
qtd_item = soup.find('div', class_='offers-index pull-left text-nowrap').get_text().strip()

qtd = int(qtd_item[74:75] + qtd_item[76:])
ultima_pagina = math.ceil(qtd / 24)

dic_aptos = {'descricao': [], 'quartos': [], 'area': [], 'valor': []}

for i in range(1, ultima_pagina + 1):
    url_pag = f'https://www.imovirtual.com/arrendar/apartamento/?page={i}'
    site = requests.get(url_pag, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    desc = soup.find_all('div', class_='offer-item-details')

    for a in desc:
        descricao = a.find('span', class_='offer-item-title')
        quartos = a.find('li', class_='offer-item-rooms hidden-xs').getText().strip()
        area = a.find('li', class_='hidden-xs offer-item-area').getText().strip()
        valor = a.find('li', class_='offer-item-price').getText().strip()

        print(descricao, quartos, area, valor)

        dic_aptos['descricao'].append(descricao)
        dic_aptos['quartos'].append(quartos)
        dic_aptos['area'].append(area)
        dic_aptos['valor'].append(valor)

    print(url_pag)

df = pd.DataFrame(dic_aptos)

df.to_csv('E:/Dados/apartamentos.csv')
