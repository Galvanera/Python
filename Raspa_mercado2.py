import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from time import sleep

# Inicializar o driver do Selenium (certifique-se de ter o ChromeDriver instalado)

Options = Options()
Options.add_argument('window-size=1400,1800')
driver = webdriver.Chrome(options=Options)
# Abrir a página
url = "https://tauste.com.br/bauru/"
driver.get(url)
time.sleep(1.5)
cep = driver.find_element(By.XPATH, '//*[@id="zipcode"]')
cep.click()
cep.send_keys("17066050")
continuar = driver.find_element(
    By.XPATH, '//*[@id="form-validate-zipcode"]/div[2]/div/button')
continuar.click()
sleep(1)
menu = driver.find_element(
    By.XPATH, '//*[@id="html-body"]/div[3]/header/div[2]/span')
menu.click()
time.sleep(1)
tabela_cate = driver.find_element(By.XPATH, '//*[@id="ui-id-1"]')
lista_categoria = []
try:
    # Encontra todas as tags <a> com o atributo href
    tags_a = tabela_cate.find_elements(By.TAG_NAME, "a")

    # Imprime os valores dos atributos href
    for tag in tags_a:
        href_value = tag.get_attribute("href")
        # print(f"Valor do atributo href: {href_value}")
        if href_value and href_value.count("/") == 4:
            lista_categoria.append(href_value)

    print("Tags <a> encontradas e valores impressos com sucesso!")

except Exception as e:
    print(f"Erro ao encontrar ou interagir com as tags <a>: {e}")
precos_filtrados = []
lista_prod = []
lista_preco = []
lista_cat = []
lista_imagem = []
# Percorrer a lista a partir do segundo elemento

try:
    for i in lista_categoria:
        driver.get(i)
        time.sleep(0.5)
        while True:
            try:
                proxima_pagina = driver.find_element(
                    By.CLASS_NAME, "next").get_attribute('href')
                print(proxima_pagina)
                sleep(1)
                precos = driver.find_elements(
                    By.XPATH, '//div/div[2]/div[1]/span/span/span')
                for preco in precos:
                # product_price = preco.text.strip()
                    lista_preco.append(
                        preco.text.strip()
                    )
                products = driver.find_elements(
                    By.CLASS_NAME, "product-item-name")
                # Encontrar a categoria
                cat = driver.find_element(
                    By.XPATH, '//*[@id="page-title-heading"]/span')
                imagens = driver.find_elements(
                    By.CLASS_NAME, "product-image-photo")
                # Extrair informações (nome e preço) de cada produto
                for product in products:
                    # product_name = product.text.strip()
                    lista_prod.append(
                        product.text.strip()
                    )
                    # print(product.text)
                    lista_cat.append(cat.text)
                #  print(cat.text)
                
                    # print(preco.text)
                for imagem in imagens:
                    lista_imagem.append(imagem.get_attribute("src"))
                    #print(imagem.get_attribute('src'))
                driver.get(proxima_pagina)
            except:
                break  # Sai do loop se não houver mais páginas
except Exception as e:
    print(f"Erro ao percorrer as páginas: {e}")
i=0
while i < len(lista_preco):
    if lista_preco[i] == 'De:':
        # Ignora o próximo elemento após "De:"
        i += 1
    elif lista_preco[i] == 'Por:':
        # Ignora o "Por:"
        i += 0
    else:
        # Adiciona o preço à lista filtrada
        precos_filtrados.append(lista_preco[i])
    i += 1

df = pd.DataFrame({
    "Produto": lista_prod,
    "Preço": precos_filtrados,
    "Categoria": lista_cat,
    "Imagem": lista_imagem,
})

nome_arquivo = "Dados_Tauste.xlsx"
df.to_excel(nome_arquivo, index=False)
print(f"Os dados foram salvos no arquivo {nome_arquivo}")
