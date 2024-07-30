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


Options = Options()
# Options.add_argument('window-size=400,800')
# Options.add_argument('--headless')
# produto1 = input('Qual produto deseja?: ')
navegador = webdriver.Chrome()

navegador.get(
    'https://www.espn.com.br/nba/estatisticas/jogador/_/temporada/2024/tipodetemporada/2')
# Clicar no botão "Mostrar mais" até que não esteja mais disponível

while True:
    try:
        show_more_button = navegador.find_element(
            By.CLASS_NAME, "loadMore__link")
        show_more_button.click()
        time.sleep(1)  # Aguardar um segundo para o conteúdo ser carregado
    except:
        break  # O botão não está mais disponível

lista_jogadores = []
lista_id = []
lista_time = []
l_posicao = []
lista_jogos_disputados = []
l_minutos = []
l_pontos = []
l_ma_convertidos = []
l_mt_arremessos = []
l_porcentagem_ar_certos = []
l_media_3 = []
l_media_tent_3 = []
l_media_porc = []
l_media_ll = []
l_media_ten_ll = []
l_aprov_ll = []
l_reb = []
l_ass = []
l_roubos = []
l_bloqueio = []
l_to = []
l_dd2 = []
l_dd3 = []

# jogos = navegador.find_elements(By.XPATH, "//td[@class='Table__TD']")
tabela_jogadores = navegador.find_element(
    By.XPATH, "//tbody[@class='Table__TBODY']")
tabela_atributos = navegador.find_element(
    By.XPATH, '//*[@id="fittPageContainer"]/div[3]/div/div/section/div/div[3]/div[1]/div/div/div[2]/table/tbody')
tabela_jogadores = tabela_jogadores.text
tabela_jogadores = list(tabela_jogadores.split("\n"))
tabela_atributos = tabela_atributos.text
tabela_atributos = list(tabela_atributos.split())
# print(len(tabela_atributos))

id = list(range(0, len(tabela_jogadores), 3))
jogador = list(range(1, len(tabela_jogadores), 3))
time = list(range(2, len(tabela_jogadores), 3))
posicao = list(range(0, len(tabela_atributos), 20))
jogos_disputados = list(range(1, len(tabela_atributos), 20))
minutos = list(range(2, len(tabela_atributos), 20))
pontos = list(range(3, len(tabela_atributos), 20))
ma_convertidos = list(range(4, len(tabela_atributos), 20))
mt_arremessos = list(range(5, len(tabela_atributos), 20))
porcentagem_ar_certos = list(range(6, len(tabela_atributos), 20))
media_3 = list(range(7, len(tabela_atributos), 20))
media_tent_3 = list(range(8, len(tabela_atributos), 20))
media_porc = list(range(9, len(tabela_atributos), 20))
media_ll = list(range(10, len(tabela_atributos), 20))
media_ten_ll = list(range(11, len(tabela_atributos), 20))
aprov_ll = list(range(12, len(tabela_atributos), 20))
reb = list(range(13, len(tabela_atributos), 20))
ass = list(range(14, len(tabela_atributos), 20))
roubos = list(range(15, len(tabela_atributos), 20))
bloqueio = list(range(16, len(tabela_atributos), 20))
to = list(range(17, len(tabela_atributos), 20))
dd2 = list(range(18, len(tabela_atributos), 20))
dd3 = list(range(19, len(tabela_atributos), 20))

for i in id:
    # print(tabela_jogadores[i])
    lista_id.append(tabela_jogadores[i])
# print(lista_id)
for j in jogador:
    # print(tabela_jogadores[j])
    lista_jogadores.append(tabela_jogadores[j])
# print(lista_jogadores)
for k in time:
    lista_time.append(tabela_jogadores[k])
# print(lista_time) ----------------------------------------------
for v in posicao:
    l_posicao.append(tabela_atributos[v])
for a in jogos_disputados:
    lista_jogos_disputados.append(float(tabela_atributos[a]))
for b in minutos:
    l_minutos.append(float(tabela_atributos[b]))
for c in pontos:
    l_pontos.append(float(tabela_atributos[c]))
for d in ma_convertidos:
    l_ma_convertidos.append(float(tabela_atributos[d]))
for e in mt_arremessos:
    l_mt_arremessos.append(float(tabela_atributos[e]))
for f in porcentagem_ar_certos:
    l_porcentagem_ar_certos.append(float(tabela_atributos[f]))
for g in media_3:
    l_media_3.append(float(tabela_atributos[g]))
for h in media_tent_3:
    l_media_tent_3.append(float(tabela_atributos[h]))
for r in media_porc:
    l_media_porc.append(float(tabela_atributos[r]))
for l in media_ll:
    l_media_ll.append(float(tabela_atributos[l]))
for m in media_ten_ll:
    l_media_ten_ll.append(float(tabela_atributos[m]))
for n in aprov_ll:
    l_aprov_ll.append(float(tabela_atributos[n]))
for o in reb:
    l_reb.append(float(tabela_atributos[o]))
for p in ass:
    l_ass.append(float(tabela_atributos[p]))
for p in roubos:
    l_roubos.append(float(tabela_atributos[p]))
for q in bloqueio:
    l_bloqueio.append(float(tabela_atributos[q]))
for s in to:
    l_to.append(float(tabela_atributos[s]))
for t in dd2:
    l_dd2.append(float(tabela_atributos[t]))
for u in dd3:
    l_dd3.append(float(tabela_atributos[u]))

# tabela_geral = list(zip(lista_id, lista_jogadores, lista_time, lista_jogos_disputados, l_minutos, l_pontos, l_ma_convertidos, l_mt_arremessos, l_porcentagem_ar_certos,
#                        l_media_3, l_media_tent_3, l_media_ll, l_media_ten_ll, l_aprov_ll, l_reb, l_ass, l_roubos, l_bloqueio, l_toco, l_to, l_dd2, l_dd3))
# print(tabela_geral)
valores = pd.DataFrame(list(zip(lista_id, lista_jogadores, lista_time, l_posicao, lista_jogos_disputados, l_minutos, l_pontos, l_ma_convertidos, l_mt_arremessos, l_porcentagem_ar_certos,
                                l_media_3, l_media_tent_3, l_media_porc, l_media_ll, l_media_ten_ll, l_aprov_ll, l_reb, l_ass, l_roubos, l_bloqueio, l_to, l_dd2, l_dd3)), columns=['ID', 'Nome Jogador', 'Time', 'Posição', 'Jgs Disp', 'MIN', 'PTS',	'M.Arr', 'M.Ten.Arr',
                                                                                                                                                                                    'Arr.Cert%', 'Med.3PTS', 'Med.Tent3',	'Arr3P%', 'Med.LL', 'Med.Tent.LL',
                                                                                                                                                                                    'Aprov.LL%', 'REB', 'AST', 'Roub', 'BLK', 'TO',	'DD2',	'DD3'])
valores.to_excel('NBA.xlsx', index=False)

print("planilha criada com sucesso!")
