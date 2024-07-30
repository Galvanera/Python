import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
from time import sleep

# Inicializar o driver do Selenium (certifique-se de ter o ChromeDriver instalado)

Options = Options()
Options.add_argument('window-size=1400,1800')
driver = webdriver.Chrome(options=Options)
# Abrir a página
url = "https://www.confianca.com.br/"
driver.get(url)
time.sleep(1.5)
bauru = driver.find_element(By.XPATH, "//div[@class='box__button']")
bauru.click()
time.sleep(1)
menu = driver.find_element(By.XPATH, "//section/div/div/div/div/button")
menu.click()
sleep(1)
lista_categoria = []
# colocar a tag no final /a que contem o href
categorias = driver.find_elements(
    By.XPATH, "//div[@class='side-nav__menu-item']/a")

for categoria in categorias:
    lista_categoria.append(
        categoria.get_attribute('href'))
# print(lista_categoria)
lista_prod = []
lista_preco = []
lista_cat = []
lista_imagem = []
# Percorrer a lista a partir do segundo elemento
for i in range(1, len(lista_categoria)):
    driver.get(lista_categoria[i])
    time.sleep(0.5)

    # Tempo total para rolar a página (1 minuto = 60 segundos)
    tempo_total = 60
    # Intervalo de rolagem (ajuste conforme necessário)
    intervalo = 2  # Rolar a cada x segundos
    # Calcula quantas vezes precisamos rolar
    num_rolagens = tempo_total // intervalo

    # Rolar a página continuamente

    for _ in range(num_rolagens):
        # Rolar até o final da página
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(intervalo)
    # Encontrar todos os produtos
    products = driver.find_elements(By.CLASS_NAME, "product-shelf__name")
    precos = driver.find_elements(
        By.CLASS_NAME, "product-shelf__price-current")
    # Encontrar a categoria
    cat = driver.find_element(By.XPATH, "//div[2]/div/h2")
    imagens = driver.find_elements(
        By.XPATH, "//section[2]/div/a/div/div/button/img")

    # Extrair informações (nome e preço) de cada produto
    for product in products:
        # product_name = product.text.strip()
        lista_prod.append(
            product.text.strip()
        )
        lista_cat.append(cat.text)
    for preco in precos:
        # product_price = preco.text.strip()
        lista_preco.append(
            preco.text.strip()
        )
    for imagem in imagens:
        lista_imagem.append(imagem.get_attribute("src"))
df = pd.DataFrame({
    "Produto": lista_prod,
    "Preço": lista_preco,
    "Categoria": lista_cat,
    "Imagem": lista_imagem
})

nome_arquivo = "Dados_mercado.xlsx"
df.to_excel(nome_arquivo, index=False)
print(f"Os dados foram salvos no arquivo {nome_arquivo}")
