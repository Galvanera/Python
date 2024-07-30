import requests
from bs4 import BeautifulSoup
import pandas as pd

lista_noticias = []

response = requests.get('https://g1.globo.com/')
content = response.content

site = BeautifulSoup(content, 'html.parser')

#HTML da noticia
posts = site.findAll('div', attrs={'class': '_evt'})

#titulo da noticia
for post in posts:
    titulo_noticia = post.find('a', attrs={'class':'feed-post-link'})
    #print(titulo_noticia.text) # titulo da noticia
    #print(titulo_noticia['href']) # link da noticia

    lista_noticias.append([titulo_noticia.text, titulo_noticia['href']])    
    

news = pd.DataFrame(lista_noticias, columns=['Titulo da Noticia', 'Link da Noticia'])
news.to_excel('NoticiasG1.xlsx', index=False)
print (news)