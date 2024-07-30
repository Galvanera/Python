import pandas as pd

tabela = pd.read_excel("produtos.xlsx")

# atualizar multiplicador
# tabela.loc[linha, coluna] = 1.5
tabela.loc[tabela["Tipo"] == "Serviço", "Multiplicador imposto"] = 1.5
tabela.loc[tabela["Tipo"] == "Produto", "Multiplicador imposto"] = 1.3
tabela.loc[tabela["Produtos"] == "SPA", "Multiplicador imposto"] = 50


# fazer a conta de multiplicação
tabela["Preço real"] = tabela["Multiplicador imposto"] * \
    tabela["Preço base original"]

# salvar as mudanças em excel
tabela.to_excel("Produtos(2).xlsx", index=False)

print(tabela.loc[tabela["Tipo"] == "Serviço"])
print(tabela.loc[tabela["Tipo"] == "Produto"])
print(tabela.loc[tabela["Preço real"] > 1000])
print(tabela.loc[tabela["Preço real"] < 1000]) 
