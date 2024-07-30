import streamlit as st
import pandas as pd
import altair as alt

# Carregando os dados do arquivo .xlsx (substitua pelo caminho do seu arquivo)
file_path = 'NBA.xlsx'
df = pd.read_excel(file_path)

# Filtro pelo campo "Time"
selected_team = st.sidebar.selectbox('Selecione um time:', df['Time'].unique())
filtered_df = df[df['Time'] == selected_team]

# Exibindo a tabela filtrada
st.dataframe(filtered_df, height=400)

# Seleção múltipla de jogadores
selected_players = st.multiselect("Selecione os Jogadores", filtered_df["Nome Jogador"])

# Filtrar os dados pelos jogadores selecionados
filtered_df_players = filtered_df[filtered_df["Nome Jogador"].isin(selected_players)]

# Gráfico de barras para 'PTS', 'REB' e 'AST'
bar_chart_pts = alt.Chart(filtered_df_players).mark_bar().encode(
    x='PTS:Q',
    y='Nome Jogador:N',
    color=alt.value('blue'),
    tooltip=['Nome Jogador', 'PTS']
).properties(width=400, height=200)

bar_chart_reb = alt.Chart(filtered_df_players).mark_bar().encode(
    x='REB:Q',
    y='Nome Jogador:N',
    color=alt.value('green'),
    tooltip=['Nome Jogador', 'REB']
).properties(width=400, height=200)

bar_chart_ast = alt.Chart(filtered_df_players).mark_bar().encode(
    x='AST:Q',
    y='Nome Jogador:N',
    color=alt.value('orange'),
    tooltip=['Nome Jogador', 'AST']
).properties(width=400, height=200)

# Gráfico de barras unificado para 'PTS', 'REB' e 'AST'



# Exibindo os gráficos um abaixo do outro
st.altair_chart(bar_chart_pts, use_container_width=True)
st.altair_chart(bar_chart_reb, use_container_width=True) 
st.altair_chart(bar_chart_ast, use_container_width=True)

# Exibir os valores dos atributos
st.write("Valores dos Atributos:")
for player in selected_players:
    player_data = filtered_df_players[filtered_df_players["Nome Jogador"] == player]
    st.write(f"{player}: PTS={player_data['PTS'].values[0]}, REB={player_data['REB'].values[0]}, AST={player_data['AST'].values[0]}")