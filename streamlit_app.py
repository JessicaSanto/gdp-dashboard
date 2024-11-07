import numpy as np
import streamlit as st
#  Importa o Streamlit, uma biblioteca que permite criar aplicações web interativas em Python.
import pandas as pd
#  Importa o Pandas, uma biblioteca para manipulação e análise de dados.
import plotly.express as px
# Importa o Plotly Express, uma biblioteca para criação de gráficos interativos.
from query import *
# Importa todas as funções e variáveis do módulo query, que pode incluir a função view_all_data() usada para obter dados de uma API.

# Consulta SQL
query = "SELECT * FROM registro"

# Carregar os dados do MySQL
df = get_mysql_data(query)

# Botão para atualizar os dados
if st.button("Atualizar Dados"):
    df = get_mysql_data(query)

# Sidebar
st.sidebar.header("Selecione a Informação para Gráficos")
# Adiciona um cabeçalho à barra lateral do aplicativo Streamlit, com o texto "Selecione a Informação para Gráficos".

# Seleção de colunas para gráficos
x_axis = st.sidebar.selectbox(
# Cria uma caixa de seleção na barra lateral para o usuário escolher a coluna a ser usada no eixo X do gráfico.
    "Eixo X",
    options=["umidade", "temperatura", "pressao", "altitude", "co2"],
#  Lista de opções que o usuário pode selecionar.
    index=0
# Define a opção selecionada por padrão (0 = primeira opção, 1 = segunda opção, etc.).
)

y_axis = st.sidebar.selectbox(
# Cria uma caixa de seleção semelhante para o eixo Y.
    "Eixo Y",
    options=["umidade", "temperatura", "pressao", "altitude", "co2", "poeira1", "poeira2"],
#  Lista de opções que o usuário pode selecionar.
    index=1
# Define a opção selecionada por padrão (0 = primeira opção, 1 = segunda opção, etc.).
)

# Função para verificar se um atributo deve ser exibido no filtro
def filtros(attribute):
    return attribute in [x_axis, y_axis]
# Define uma função que verifica se o atributo dado deve ser exibido como um filtro, 
# retornando True se o atributo está sendo usado nos eixos X ou Y do gráfico.

st.sidebar.header("Selecione o Filtro")
# Adiciona um cabeçalho "Selecione o Filtro" na barra lateral, indicando que abaixo dessa linha serão exibidos filtros de dados.


# Exibir sliders apenas se o atributo correspondente for selecionado
if filtros("temperatura"):
# Exibe um controle deslizante (slider) na barra lateral para filtrar a temperatura, 
# mas apenas se a temperatura estiver selecionada como eixo X ou Y.
    temperatura_range = st.sidebar.slider(
        "Temperatura (°C)",
        min_value=float(df["temperatura"].min()),
    # Valor mínimo do slider, baseado nos dados carregados.
        max_value=float(df["temperatura"].max()),
    # Valor máximo do slider.
        value=(float(df["temperatura"].min()), float(df["temperatura"].max())),
    # Faixa de valores padrão selecionada.
        step=0.1
    # Incremento para cada movimento do slider.
    )

if filtros("pressao"):
    pressao_range = st.sidebar.slider(
        "Pressão (hPa)",
        min_value=float(df["pressao"].min()),
        max_value=float(df["pressao"].max()),
        value=(float(df["pressao"].min()), float(df["pressao"].max())),
        step=0.1
    )
# Exibe um controle deslizante para filtrar a pressão, com funcionamento similar ao slider de temperatura.

if filtros("altitude"):
    altitude_range = st.sidebar.slider(
        "Altitude (m)",
        min_value=float(df["altitude"].min()),
        max_value=float(df["altitude"].max()),
        value=(float(df["altitude"].min()), float(df["altitude"].max())),
        step=1.0
    )
# Exibe um controle deslizante para filtrar a altitude.
# Definindo min e max de forma segura para o slider
min_umidade = float(df["umidade"].min())
max_umidade = float(df["umidade"].max())

# Garantir que os valores não sejam iguais
if min_umidade == max_umidade:
    # Se os valores forem iguais, aumentar ou diminuir um valor pequeno para que o slider funcione
    max_umidade += 0.1  # Aumenta o valor máximo em 0.1 para garantir que o slider tenha intervalo
    min_umidade -= 0.1  # Diminui o valor mínimo em 0.1

# Agora, o slider funcionará com os valores ajustados
if filtros("umidade"):
    umidade_range = st.sidebar.slider(
        "Umidade (%)",
        min_value=min_umidade,
        max_value=max_umidade,
        value=(min_umidade, max_umidade),
        step=0.1
    )
# Exibe um controle deslizante para filtrar a umidade.

if filtros("co2"):
    co2_range = st.sidebar.slider(
        "CO2 (ppm)",
        min_value=float(df["co2"].min()),
        max_value=float(df["co2"].max()),
        value=(float(df["co2"].min()), float(df["co2"].max())),
        step=1.0
    )
    
if filtros("poeira1"):
    poeira1_range = st.sidebar.slider(
        "Poeira (ppm)",
        min_value=float(df["poeira1"].min()),
        max_value=float(df["poeira1"].max()),
        value=(float(df["poeira1"].min()), float(df["poeira1"].max())),
        step=1.0
    )
# Exibe um controle deslizante para filtrar o CO2.

# Filtragem do DataFrame com base nos intervalos selecionados na sidebar
df_selection = df.copy()
# Cria uma cópia do DataFrame original df. Isso é feito para garantir que as operações 
# subsequentes de filtragem sejam aplicadas em uma nova instância do DataFrame (df_selection),
# sem alterar os dados originais em df.
if filtros("temperatura"):
# Verifica se a função filtros("temperatura") retorna True. Esta função provavelmente verifica 
# se o atributo "temperatura" deve ser filtrado (por exemplo, 
# se o usuário selecionou essa coluna em um painel de filtros).
    df_selection = df_selection[
# Aqui, a filtragem está sendo aplicada à coluna temperatura do DataFrame df_selection.
        (df_selection["temperatura"] >= temperatura_range[0]) & 
# Mantém apenas as linhas em que o valor da coluna temperatura é maior ou igual ao limite inferior (temperatura_range[0]).
        (df_selection["temperatura"] <= temperatura_range[1])
# Mantém apenas as linhas em que o valor da coluna temperatura é menor ou igual ao limite superior (temperatura_range[1]).
    ]
# Cria uma cópia do DataFrame df e filtra os dados com base no intervalo selecionado para a temperatura, se aplicável.

if filtros("pressao"):
    df_selection = df_selection[
        (df_selection["pressao"] >= pressao_range[0]) & 
        (df_selection["pressao"] <= pressao_range[1])
    ]
# Filtra os dados com base no intervalo selecionado para a pressão, se aplicável.

if filtros("altitude"):
    df_selection = df_selection[
        (df_selection["altitude"] >= altitude_range[0]) & 
        (df_selection["altitude"] <= altitude_range[1])
    ]
# Filtra os dados com base no intervalo selecionado para a altitude, se aplicável.

if filtros("umidade"):
    df_selection = df_selection[
        (df_selection["umidade"] >= umidade_range[0]) & 
        (df_selection["umidade"] <= umidade_range[1])
    ]
# Filtra os dados com base no intervalo selecionado para a umidade, se aplicável.

if filtros("co2"):
    df_selection = df_selection[
        (df_selection["co2"] >= co2_range[0]) & 
        (df_selection["co2"] <= co2_range[1])
    ]
    
if filtros("poeira1"):
    df_selection = df_selection[
        (df_selection["poeira1"] >= poeira1_range[0]) & 
        (df_selection["poeira1"] <= poeira1_range[1])
    ]
# Filtra os dados com base no intervalo selecionado para o CO2, se aplicável.

def Home():
# Define a função Home(), responsável por exibir os dados tabulares filtrados.
    with st.expander("Tabular"):
# Cria uma seção expansível intitulada "Tabular". Usuário pode expandir ou recolher essa área conforme necessário.
        showData = st.multiselect('Filter: ', df_selection.columns, default=[], key="showData_home")
# Permite ao usuário selecionar colunas específicas para exibição em uma tabela.
        if showData:
# Exibe os dados filtrados apenas se o usuário selecionar alguma coluna.
            st.write(df_selection[showData])
# Exibe os dados filtrados com base nas colunas selecionadas pelo usuário.
#  Mostra uma tabela na interface com as colunas selecionadas. 
# df_selection[showData] cria um novo DataFrame contendo apenas as colunas escolhidas.
        
    # Compute top analytics
    if not df_selection.empty:
# Verifica se o DataFrame df_selection não está vazio.
#  O operador not inverte essa lógica, ou seja, o código dentro deste bloco será executado apenas se df_selection contiver dados.
        media_umidade = df_selection["umidade"].mean()
        media_temperatura = df_selection["temperatura"].mean()
        media_co2 = df_selection["co2"].mean()
        media_pressao = df_selection["pressao"].mean()
# Calcula a média de valores das colunas selecionadas no DataFrame df_selection.
# As médias calculadas são armazenadas nas variáveis media_umidade, media_temperatura, media_co2 e media_pressao.

        total1, total2, total3, total4 = st.columns(4, gap='large')
# Cria quatro colunas (widgets de layout) no painel do Streamlit.
# st.columns(4): Gera quatro colunas iguais em largura.
# gap='large': Adiciona um espaçamento maior entre as colunas.

        with total1:
# Inicia um bloco with para a primeira coluna total1. O código dentro deste bloco será aplicado exclusivamente a essa coluna.
            st.info('Média de Registros Umidade', icon='📌')
# Exibe uma caixa de informação com um título e um ícone na primeira coluna.
            st.metric(label="Média", value=f"{media_umidade:.2f}")
# Exibe uma métrica na primeira coluna mostrando a média de umidade calculada anteriormente.

        with total2:
            st.info('Média de Registro CO2', icon='📌')
            st.metric(label="Média", value=f"{media_co2:.2f}")
        
        with total3:
            st.info('Média de Registros de Temperatura', icon='📌')
            st.metric(label="Média", value=f"{media_temperatura:.2f}")
            
        with total4:
            st.info('Média de Registros de Pressão', icon='📌')
            st.metric(label="Média", value=f"{media_pressao:.2f}")
            
        st.markdown("""-----""")

def graphs():
    # Define o título da página do dashboard
    st.title("Dashboard de Monitoramento")

    # Cria abas para diferentes seções do dashboard
    aba1, aba2, aba3 = st.tabs(["Gráficos de Média", "Registros Gerais", "Gráficos de Dispersão"])
    
    with aba1:
    # Define a função graphs(), responsável por gerar e exibir gráficos.
        if df_selection.empty:
            st.write("Nenhum dado disponível para gerar gráficos.")
            return
    # Verifica se o DataFrame filtrado está vazio, e, se estiver, exibe uma mensagem 
    # dizendo que não há dados disponíveis para gerar gráficos.

        
        # Verificação se os eixos X e Y são iguais
        if x_axis == y_axis:
            st.warning("Selecione uma opção diferente para os eixos X e Y.")
            return
    # Verifica se os eixos X e Y são iguais e, se forem, exibe um aviso pedindo ao usuário para selecionar opções diferentes.


        # Gráfico simples de barra
        try:
    # Inicia um bloco try, que é utilizado para capturar e lidar com exceções (erros) 
    # que possam ocorrer durante a execução do código. Se ocorrer um erro dentro desse bloco, 
    # ele será tratado em um bloco except correspondente (que não está visível neste trecho).

            # Agregando os dados conforme a seleção
            grouped_data = df_selection.groupby(by=[x_axis]).size().reset_index(name='contagem')
    # Agrega os dados do DataFrame df_selection com base na coluna selecionada para o eixo X (x_axis).
    # df_selection.groupby(by=[x_axis]): Agrupa os dados com base nos valores da coluna selecionada como eixo X.
    # .size(): Conta o número de ocorrências em cada grupo.
    # .reset_index(name='contagem'): Reseta o índice do DataFrame agrupado e nomeia a nova 
    # coluna com as contagens de cada grupo como "contagem"
            fig_valores = px.bar(
    # Cria um gráfico de barras horizontais usando o Plotly Express com os dados agrupados.
                grouped_data,
    # grouped_data: O DataFrame agrupado que contém os dados a serem plotados.
                x=x_axis,
    # x=x_axis: Define o eixo X do gráfico como a coluna selecionada no eixo X.
                y='contagem',
    # y='contagem': Define o eixo Y do gráfico como a coluna "contagem", que contém o número de registros em cada grupo.
                orientation='h',
    # orientation='h': Define a orientação do gráfico como horizontal.
                title=f"<b>Contagem de Registros por {x_axis.capitalize()}</b>",
    # title=f"<b>Contagem de Registros por {x_axis.capitalize()}</b>": Define o título do gráfico, com o nome da coluna do eixo X capitalizado.
                color_discrete_sequence=["#0083b8"],
    # color_discrete_sequence=["#0083b8"]: Define a cor das barras no gráfico.
                template="plotly_white"
    # template="plotly_white": Define um tema claro para o gráfico.
            )
            
            fig_valores.update_layout(
    # Atualiza o layout do gráfico para personalizar sua aparência:
                plot_bgcolor="rgba(0,0,0,0)",
    # plot_bgcolor="rgba(0,0,0,0)": Define a cor de fundo do gráfico como transparente.
                xaxis=dict(showgrid=False),
    # xaxis=dict(showgrid=False): Remove as linhas de grade do eixo X.
                yaxis=dict(showgrid=False)
    # yaxis=dict(showgrid=False): Remove as linhas de grade do eixo Y.
            )
        except Exception as e:
    # Inicia um bloco except, que é executado se algum erro ocorrer dentro do bloco try correspondente. 
    # O tipo de erro capturado aqui é a classe genérica Exception, que pode capturar qualquer tipo de exceção.
            st.error(f"Erro ao criar o gráfico de valores: {e}")
    # Exibe uma mensagem de erro no Streamlit utilizando a função st.error(). 
    # A mensagem informa ao usuário que ocorreu um erro ao criar o gráfico de valores.
    # {e} é interpolado na string para mostrar a mensagem detalhada do erro que foi capturado, 
    # fornecendo mais informações sobre o que deu errado.
            fig_valores = None
    # Define a variável fig_valores como None. Isso é feito para garantir que, se houver um erro ao criar o gráfico, 
    # fig_valores não conterá dados inválidos. Em seguida, o código pode lidar com essa ausência de um gráfico válido de forma segura, 
    # possivelmente ignorando a tentativa de exibição ou exibindo uma mensagem alternativa.
        
        # Gráfico simples de linha
        try:
            # Agregando os dados conforme a seleção
            grouped_data = df_selection.groupby(by=[x_axis]).agg({y_axis: 'mean'}).reset_index()
            fig_state = px.line(
                grouped_data,
                x=x_axis,
                y=y_axis,
                title=f"<b>Média de {y_axis.capitalize()} por {x_axis.capitalize()}</b>",
                color_discrete_sequence=["#0083b8"],
                template="plotly_white"
            )
            
            fig_state.update_layout(
                xaxis=dict(showgrid=False),
                plot_bgcolor="rgba(0,0,0,0)",
                yaxis=dict(showgrid=False)
            )
        except Exception as e:
            st.error(f"Erro ao criar o gráfico de linha: {e}")
            fig_state = None
        
        # Exibir gráficos
        left, right = st.columns(2)
    # Cria duas colunas lado a lado na interface do Streamlit. A variável left se refere à primeira coluna e right 
    # se refere à segunda coluna. O parâmetro 2 indica que você deseja criar duas colunas de largura igual. 
    # Esse layout permite a exibição de dois elementos (neste caso, gráficos) lado a lado.
        if fig_state:
    # Verifica se a variável fig_state contém um gráfico válido. A variável fig_state foi definida anteriormente no 
    # código e pode ser None se houver um erro na criação do gráfico de linha. Se fig_state não for None, significa que 
    # há um gráfico válido para exibir.
            with left:
    # with left: define que o seguinte bloco de código deve ser renderizado na coluna left criada anteriormente.
                st.plotly_chart(fig_state, use_container_width=True)
    # st.plotly_chart(fig_state, use_container_width=True) exibe o gráfico de linha fig_state na coluna left. 
    # A opção use_container_width=True faz com que o gráfico utilize a largura total da coluna onde está inserido, 
    # ajustando seu tamanho automaticamente para preencher o espaço disponível.
        if fig_valores:
    # Verifica se a variável fig_valores contém um gráfico válido. A variável fig_valores foi definida anteriormente e 
    # pode ser None se houver um erro na criação do gráfico de barras. Se fig_valores não for None, significa que há um gráfico 
    # válido para exibir.
            with right:
    # define que o seguinte bloco de código deve ser renderizado na coluna right criada anteriormente.
                st.plotly_chart(fig_valores, use_container_width=True)
    # st.plotly_chart(fig_valores, use_container_width=True) exibe o gráfico de barras fig_valores na coluna right. 
    # A opção use_container_width=True faz com que o gráfico utilize a largura total da coluna onde está inserido, 
    # ajustando seu tamanho automaticamente para preencher o espaço disponível.
    with aba2:
        # Função para preparar os dados para o gráfico de linha geral
        def prepare_chart_data(df, columns):
            chart_data = pd.DataFrame()  # Cria um DataFrame vazio para armazenar os dados do gráfico
            for column in columns:
                if column in df.columns:
                    # Cria um DataFrame temporário com os valores da coluna e uma coluna de "registro" para identificação
                    temp_df = df[[column]].copy()
                    temp_df['registro'] = column
                    temp_df = temp_df.rename(columns={column: 'valor'})
                    chart_data = pd.concat([chart_data, temp_df])  # Concatena os dados temporários ao DataFrame principal
            return chart_data

        # Lista de colunas que serão incluídas no gráfico
        columns = ["temperatura", "umidade", "co2", "altitude", "pressao", "poeira1", "poeira2"]
        chart_data = prepare_chart_data(df_selection, columns)

        # Verifica se há dados para exibir
        if not chart_data.empty:
            # Cria um gráfico de linha para mostrar todos os registros gerais
            fig = px.line(
                chart_data,
                y="valor",
                color="registro",  # Diferencia as linhas no gráfico por cor
                title="Registros Gerais",
                labels={"valor": "Valor", "registro": "Tipo de Registro"}
            )
            fig.update_layout(
                xaxis_title="Índice",  # Define o título do eixo X
                yaxis_title="Valor",   # Define o título do eixo Y
                plot_bgcolor="rgba(0,0,0,0)"  # Define o fundo do gráfico como transparente
            )
            st.plotly_chart(fig, use_container_width=True)  # Exibe o gráfico
        else:
            st.write("Nenhum dado disponível para gerar gráficos.")
            

    with aba3:
        # Prepara os dados para o gráfico de dispersão
        scatter_data = df_selection.copy()

        # Transforma o DataFrame para incluir uma coluna de "Variável" e valores "Valor"
        melted_data = pd.melt(
            scatter_data,
            id_vars=['umidade'],  # Inclua uma coluna para colorir os pontos
            value_vars=['temperatura', 'co2', 'altitude', 'pressao'],
            var_name='Variável',
            value_name='Valor'
        )

        # Verifica se há dados disponíveis para criar o gráfico
        if not melted_data.empty:
            # Cria um gráfico de dispersão com todas as variáveis, diferenciando por cor
            fig_scatter = px.scatter(
                melted_data,
                x='Valor',
                y='umidade',  # Usa 'umidade' como eixo Y para visualizar variação
                color='Variável',  # Diferencia os pontos por cor baseada na variável
                title="Dispersão de Variáveis com Cor Diferente",
                labels={'Valor': 'Valor', 'umidade': 'Umidade (%)'},
                color_discrete_map={  # Mapeia cores específicas para cada variável
                    'temperatura': 'blue',
                    'co2': 'red',
                    'altitude': 'green',
                    'pressao': 'orange'
                }
            )
            
            fig_scatter.update_layout(
                xaxis_title='Valor',  # Define o título do eixo X
                yaxis_title='Umidade (%)',  # Define o título do eixo Y
                plot_bgcolor="rgba(0,0,0,0)",  # Define o fundo do gráfico como transparente
                xaxis=dict(showgrid=False),  # Remove as linhas de grade do eixo X
                yaxis=dict(showgrid=False)   # Remove as linhas de grade do eixo Y
            )
            st.plotly_chart(fig_scatter, use_container_width=True)  # Exibe o gráfico de dispersão
        else:
            st.write("Nenhum dado disponível para gerar gráficos.")
Home()
graphs()