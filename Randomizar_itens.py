import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import xlsxwriter
import openpyxl

# Função para gerar datas aleatórias no intervalo desejado


def generate_random_date():
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 5, 31)

    # Gera uma lista de todas as datas no intervalo
    date_list = [start_date + timedelta(days=x)
                 for x in range((end_date - start_date).days + 1)]

    # Filtra a lista para incluir apenas sábados e domingos
    weekend_dates = [date for date in date_list if date.weekday() in (5, 6)]

    # Adiciona mais peso aos fins de semana
    # Ajuste o multiplicador conforme necessário
    weighted_dates = (date_list + weekend_dates) * 2

    # Escolhe uma data aleatória da lista ponderada
    random_date = random.choice(weighted_dates)

    return random_date.strftime("%d/%m/%Y")


def generate_random_time():
    if random.random() < 0.7:
        # 50% chance de gerar um horário entre 16:00 e 21:00
        hour = random.randint(16, 21)
    else:
        # 30% chance de gerar um horário fora de 16:00 e 21:00
        hour = random.choice(list(range(0, 16)) + list(range(21, 23)))
    minute = random.randint(0, 59)
    return f"{hour:02d}:{minute:02d}"


def generate_random_year():
    if random.random() < 0.7:
        # 70% de chance de gerar um ano entre 26 e 65
        return random.randint(26, 65)
    else:
        # 30% de chance de gerar um ano entre 18 e 92
        return random.randint(18, 92)


# Ler a tabela "dados_mercado"
nome_arquivo = 'dados_mercado.xlsx'
df_mercado = pd.read_excel(nome_arquivo)

# Remover o símbolo "R$" e converter para float
df_mercado['Preço'] = df_mercado['Preço'].apply(lambda x: float(
    x.replace('R$', '').replace('.', '').replace(',', '.')))
# Gerar 200 nomes fictícios (permitindo repetições)
fake = Faker("pt_BR")
nomes_clientes = [fake.name() for _ in range(500)]
# Criar um dicionário para associar nomes a idades
idades_clientes = {}
for nome in nomes_clientes:
    idade = generate_random_year()  # Use a função generate_random_year()
    idades_clientes[nome] = idade

# Criar listas para armazenar os dados das compras
dados_compras = []

# Simular 1000 compras
for id_compra in range(1, 3001):
    cliente = random.choice(nomes_clientes)
    quantidade_produtos = random.randint(1, 100)
    produtos_selecionados = df_mercado.sample(n=quantidade_produtos)
    forma_pagamento = random.choices(["Cartão de crédito", "Cartão Débito", "Dinheiro", "Alimentação", "PIX"], weights=[0.22, 0.30, 0.28, 0.03, 0.17]
                                     )[0]
    idade = idades_clientes[cliente]  # Obter a idade do cliente
    data = generate_random_date()
    horario = generate_random_time()

    # Gerar um faturamento aleatório para cada produto
    for _, produto in produtos_selecionados.iterrows():
        valor_total_produto = produto['Preço']
        faturamento_produto = random.uniform(0.05, 0.75)
        if valor_total_produto < 10:
            quantidade_itens = random.randint(1, 15)
        elif 10 < valor_total_produto < 50:
            quantidade_itens = random.randint(1, 5)
        else:
            quantidade_itens = random.randint(1, 2)
        # Verificar a categoria do produto
        if produto['Categoria'] == 'Açougue':
            # Gerar um valor aleatório em gramas entre 500 e 4000
            quantidade_gramas = random.randint(500, 4000)
            quantidade_itens = quantidade_gramas

        dados_compras.append({
            "ID_compra": id_compra,
            "Forma de pagamento": forma_pagamento,
            "Data": data,
            "Horário": horario,
            "Nome do cliente": cliente,
            "Idade": idade,
            "Produto": produto['Produto'],
            "Qnt": quantidade_itens,
            "Preço": valor_total_produto,
            "Categoria": produto['Categoria'],
            "Imagem": '"' + str(produto['Imagem']) + '"',
            "Faturamento": faturamento_produto
        })

# Criar DataFrame para a tabela "Dados_compras"
df_compras = pd.DataFrame(dados_compras)

# Salvar em um arquivo .xlsx
nome_arquivo_compras = "Dados_compras2.xlsx"
df_compras.to_excel(nome_arquivo_compras, index=False, engine='xlsxwriter')
print(f"Os dados das compras foram salvos no arquivo {nome_arquivo_compras}")
