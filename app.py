# Importando biblioteca
import pandas as pd
import plotly.express as px
import streamlit as st

# Lendo a base de dados
df = pd.read_parquet("vacinados_2023.parquet")


# apagando a linha que contém data na coluna grupo
df = df.drop(df[df["grupo"] == "2022-10-01 00:00:00.0"].index)

# Corrigindo datas
# Substitua o valor inválido "2022-2022" por "2022" na coluna "data_vacinacao"
df['data_vacinacao'] = df['data_vacinacao'].str.replace('2022-2022', '2022')
df['data_vacinacao'] = df['data_vacinacao'].str.replace('2022-022022', '2022')
df['data_vacinacao'] = df['data_vacinacao'].str.replace('2022-02-262022', '2022')

df["data_vacinacao"] = pd.to_datetime(df["data_vacinacao"])

# Corrigindo Faixa Etária
df["faixa_etaria"] = df["faixa_etaria"].replace("70 a 74 Conecta Recife", "70 a 74 anos")
df["faixa_etaria"] = df["faixa_etaria"].replace("40 a 44 anoConecta Recife", "40 a 44 anos")
df["faixa_etaria"] = df["faixa_etaria"].replace("5 a 9 ano0 a 4 anos", "5 a 9 anos")
df["faixa_etaria"] = df["faixa_etaria"].replace("10 a 14 RECIFE", "10 a 14 anos")
df["faixa_etaria"] = df["faixa_etaria"].replace("20 a 24 DS 6: CNES: 0001392 - MIGUEL DE LIMA VALVERDE.", "20 a 24 anos")
df["faixa_etaria"] = df["faixa_etaria"].replace("30 a 34 ano3 - COMIRNATY (PFIZER)", "30 a 34 anos")

# Apagando as linhas com valores nulos
total_faixa_etaria = df.dropna(subset=["faixa_etaria"])






def main():

    st.title("Análise Pessoas Vacinadas Contra Covid-19 em PE em 2022")

    periodo = st.sidebar.date_input('Selecione o Período', 
                value=(pd.to_datetime('2022-01-01'), pd.to_datetime('2022-12-31')))
    
    data_inicial = pd.to_datetime(periodo[0])
    data_final = pd.to_datetime(periodo[1])
    

    # Filtrar os dados com base no range de datas selecionado
    dados_filtrados = df[(df['data_vacinacao'] >= data_inicial) & (df['data_vacinacao'] <= data_final)]
    

    genero = dados_filtrados.loc[(dados_filtrados["sexo"] == "FEMININO") | (dados_filtrados["sexo"] == "MASCULINO") | (dados_filtrados["sexo"] == "OUTROS")]
    total_gen = genero["sexo"].value_counts()
    # Gráfico total vacinados por gênero
    fig = px.pie(total_gen, values=total_gen.values, names=total_gen.index,hole=0.6, title='Total Vacinados por Gênero',
            color_discrete_sequence=px.colors.qualitative.Dark2)
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig)

    top_10 = dados_filtrados["grupo"].value_counts().nlargest(10).sort_values(ascending=True)

    # Gráfico total de vacinados por grupo
    fig1 = px.bar(top_10, orientation='h', text=top_10.values, title="Top 10 vacinados por grupo",
            color_discrete_sequence=px.colors.qualitative.Dark2,
            labels={"value":"Total Vacinados", "index":"Grupo"})
    fig1.update_layout(title_x=0.5)
    st.plotly_chart(fig1)

    # Total de Vacinados por mês
    total_mes = dados_filtrados["data_vacinacao"].dt.month.value_counts().sort_index()
    fig2 = px.line(x=total_mes.index, y=total_mes.values, title="Total Vacinados por mês", markers=True,
              labels={'x':"Mês", 'y':"Total Vacinados"}, color_discrete_sequence=px.colors.qualitative.Dark2)
    fig2.update_layout(title_x=0.5)
    st.plotly_chart(fig2)

    total_faixa_etaria = dados_filtrados.loc[(dados_filtrados["faixa_etaria"] != "1RECIFE") & (dados_filtrados['faixa_etaria'] != "6CRIANÇAS DE 05 A 11 ANOS") &
                           (dados_filtrados["faixa_etaria"] != "20 a 24 15 a 19 anos") &
                            (dados_filtrados["faixa_etaria"] != "54 - JANSSEN COVID-19 VACCINE (JOHNSON & JOHNSON)") &
                           (dados_filtrados["faixa_etaria"] != "FEMININO")]

    total_idade = total_faixa_etaria["faixa_etaria"].value_counts().reset_index().rename(columns={"index":"Faixa_Etaria", "faixa_etaria":"Total"})
    st.write(total_idade)

    # Criação do gráfico de Treemap
    fig3 = px.treemap(total_idade, path=['Faixa_Etaria'], values="Total", title="Total de Vacinados por Faixa Etária",
                color_discrete_sequence=px.colors.qualitative.Dark2)
    # Atualizar o layout para centralizar o título
    fig3.update_layout(title_x=0.5)
    st.plotly_chart(fig3)


if __name__ == "__main__":
    main()
