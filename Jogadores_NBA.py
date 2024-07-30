import openpyxl.workbook
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import openpyxl
from bs4 import BeautifulSoup
import pandas as pd
import string
import numpy as np
import time
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows

Options = Options()
# Options.add_argument('window-size=400,800')
# Options.add_argument('--headless')
# produto1 = input('Qual produto deseja?: ')
navegador = webdriver.Chrome()

navegador.get('https://www.espn.com.br/nba/times')
link_dos_times = []
Link_times = navegador.find_elements(
    By.XPATH, "//div/div/div/section/a")  # procura o link dos times
for link in Link_times:
    link = link.get_attribute('href')
    link_dos_times.append(link)
for i in link_dos_times:
    navegador.get(i)  # entra no link do time
    # sleep(1)
    # procura o botao "ELENCO"
    elenco = navegador.find_element(
        By.XPATH, "//nav/ul/li[5]/a").get_attribute('href')
    # print(elenco)
    navegador.get(elenco)  # entra no link do ELENCO
    sleep(2)
    jogadores = navegador.find_elements(By.XPATH, "//tbody/tr/td/div/a")
    lista_link_jogador = []
    for jogador in jogadores:
        jogador = jogador.get_attribute('href')
        lista_link_jogador.append(jogador)
    lista_sem_duplicatas = list(dict.fromkeys(lista_link_jogador))
    lista_nomes = []
    for nome in lista_sem_duplicatas:
        separa = nome.split("/")
        lista_nomes.append(separa[8])
    print(lista_nomes)
    # Imprime a lista sem duplicatas
    lista_data = []
    for i in lista_sem_duplicatas:
        navegador.get(i)
        imagem = navegador.find_element(By.XPATH, "//div/figure[2]/div/img").get_attribute('src')
        
        ver = navegador.find_element(
            By.XPATH, "//div/section[2]/header/div[2]/a").get_attribute('href')
        navegador.get(ver)
        sleep(1)
        tabelas1 = navegador.find_elements(
            By.XPATH, "//tr[@class='Table__TR Table__TR--sm Table__even']")
        tabelas2 = navegador.find_elements(
            By.XPATH, "//tr[@class='filled Table__TR Table__TR--sm Table__even']")
        nome1 = navegador.find_element(By.XPATH, "//div/div[2]/h1/span").text
        nome2 = navegador.find_element(
            By.XPATH, "//div/div[2]/h1/span[2]").text
        clube = navegador.find_element(By.XPATH, "//div/div[2]/div/ul/li").text
        lista_info = []
        for tabela1, tabela2 in zip(tabelas1, tabelas2):
            tabela1 = tabela1.text
            tabela1 = tabela1.split()
            tabela2 = tabela2.text.split()
            lista_info.append(tabela1)
            lista_info.append(tabela2)
            # Escrevendo os dados do DataFrame na nova planilha
        # print(lista_info)
        print("pegando informaçoes do jogador:"+nome1+" "+nome2)
        print(imagem)
        minha_lista = ['Dia', 'Data', 'EM', 'LOCAL', 'V-D', 'PLACAR', 'MIN', 'FG', 'FG%',
                       '3PT', '3PTS%', 'FT', 'FT%', 'REB', 'V', 'BLK', 'STL', 'PF', 'TO', 'PTS']
        nova_lista = [[valor for valor in sublista if valor != 'TE']
                      # Remove somente a palavra "TE"
                      for sublista in lista_info]
        nova_lista = [[valor for valor in sublista if valor != '2TE']
                      # Remove somente a palavra "2TE"
                      for sublista in nova_lista]

        # Criando uma nova lista sem os elementos que contêm 'TE'
        # Remove a lista inteira que tem a palavra "Medias"
        nova_lista = [
            sublista for sublista in nova_lista if 'Médias' not in sublista]
        # Remove a lista inteira que tem a palavra "Totais"
        nova_lista = [
            sublista for sublista in nova_lista if 'Totais' not in sublista]

        # Exibindo a nova lista
        # print(nova_lista)

        df = pd.DataFrame(nova_lista, columns=minha_lista)
        arquivo = nome1+'.xlsx'
        df.to_excel(arquivo, index=False)
        print("Planilha criada com sucesso")