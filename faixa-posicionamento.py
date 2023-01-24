import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from streamlit_extras.buy_me_a_coffee import button

st.set_page_config(
    page_title="Faixa de Posicionamento",
    page_icon="📍",
    layout="wide",
)

c30, c31 = st.columns([10.5, 1])

with c30:
    # st.image("logo.png", width=400)
    st.title("📍 Faixa de Posicionamento por Volume de Buscas")

with st.expander("ℹ - Sobre o App"):
    st.write(
        """     
-   Esta ferramenta tem como objetivo mostrar a faixa de posicionamento em relação ao volume de buscas para as principais palavras-chave de um site.
-   Instruções do padrão da planilha no [link](https://docs.google.com/spreadsheets/d/12STR9xaHbZGWThib6Zv1w1lUp76RhsKd/edit?usp=sharing&ouid=112866070513171929749&rtpof=true&sd=true).
-   Script criado por [Vinicius Stanula](https://viniciusstanula.com/).
	    """
    )

st.markdown("----")
st.markdown("## Selecione o arquivo 👇")

c1, c2 = st.columns([1.5, 4])

with c1:
    uploaded_file = st.file_uploader(
        "Escolhar o arquivo .XLSX",
        help="Escolha o arquivo .xlsx, respeitando o nome das categorias demonstradas no arquivo padrão.",
    )

    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        categorias1 = df["Categoria"].drop_duplicates()
        categorias = sorted(categorias1)

        option = st.multiselect(
            "Selecione a Categoria 👇",
            categorias,
            help="Escolha as categorias para adicionar ao gráfico. É possível selecionar quantas quiser.",
        )
        df = df[df["Categoria"].str.contains("|".join(option))]

        agree = st.checkbox(
            "Diferenciar CTR?",
            help="Selecione para que os círculos tenham tamanhos diferentes de acordo com o CTR.",
        )

        if agree:
            fig = px.scatter(
                df,
                x="Posição",
                y="Volume Buscas",
                title="Análise de Posicionamento por Volume de Buscas",
                color="Categoria",
                size="CTR",
                hover_data=["Palavra-Chave"],
            )
        else:
            fig = px.scatter(
                df,
                x="Posição",
                y="Volume Buscas",
                title="Análise de Posicionamento por Volume de Buscas",
                color="Categoria",
                hover_data=["Palavra-Chave"],
            )

        with c2:
            tab1, tab2, tab3 = st.tabs(["Gráfico 📈", "Tabela 💾", "Buscas por Categoria 📊"])
            with tab1:
                st.plotly_chart(fig, theme="streamlit", use_container_width=True, height=800)

            with tab2:
                st.markdown("## Tabela de Palavras-Chave")
                df = df.sort_values(by='Volume Buscas', ascending=False)
                st.dataframe(df, use_container_width=True)

                def to_excel(df):
                    output = BytesIO()
                    writer = pd.ExcelWriter(output, engine='xlsxwriter')
                    df.to_excel(writer, index=False, sheet_name='faixa-posicionamento')
                    workbook = writer.book
                    worksheet = writer.sheets['faixa-posicionamento']
                    format1 = workbook.add_format({'num_format': '0.00'})
                    worksheet.set_column('A:A', None, format1)
                    writer.save()
                    processed_data = output.getvalue()
                    return processed_data
                df_xlsx = to_excel(df)
                st.download_button(label='📥 Download do Excel',
                                   data=df_xlsx,
                                   file_name='faixa-de-posicionamento.xlsx')
            with tab3:
                df2 = df.groupby(['Categoria'], as_index=False).sum()
                df2 = df2.sort_values(by='Volume Buscas', ascending=False)

                fig2 = px.bar(df2,
                              x='Volume Buscas',
                              y='Categoria',
                              title="Volume de Buscas por Categoria",
                              color='Categoria')

                st.plotly_chart(fig2, theme="streamlit", use_container_width=True, height=800)
		
button(username="fake-username", floating=False, width=221)

st.markdown("----")
