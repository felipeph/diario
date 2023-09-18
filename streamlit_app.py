################## Importação das bibliotecas ######################

# Streamlit para criação da página
import streamlit as st

# Pandas para manipulação dos dados
import pandas as pd

# Pathlib para manipulação de arquivos
from pathlib import Path

# Pytz para ajuste de timezone
import pytz

# Datetime para pegar a hora e a data atual
from datetime import datetime
###################################################################

############# Criação e carregamento do dataframe ################

register_columns_names = ["Descrição", 
                          "Data e Hora Início", 
                          "Data e Hora Fim", 
                          "Duração (min)",
                          "Categoria"]

# Variável com o endereço do arquivo csv dos registros
registers_csv = Path('registros.csv')


# Teste para verificar se esso arquivo existe

# Caso exista carrega o CSV como dataframe para a aplicação
if registers_csv.is_file():
    st.session_state['registers_df'] = pd.read_csv(registers_csv)

# Caso não exista, cria um dataframe novo
else:
    st.session_state['registers_df'] = pd.DataFrame(columns=register_columns_names)

# Converta as colunas de Data e Hora para datetime, se existirem
if "Data e Hora Início" in st.session_state['registers_df']:
    st.session_state['registers_df']['Data e Hora Início'] = pd.to_datetime(st.session_state['registers_df']['Data e Hora Início'])
if "Data e Hora Fim" in st.session_state['registers_df']:
    st.session_state['registers_df']['Data e Hora Fim'] = pd.to_datetime(st.session_state['registers_df']['Data e Hora Fim'])
    


######################################################################


################## Abrindo csv e criando dataframe ##################
category_columns_names = ["Nome", 
                        "Emoji"]

# Variável com o endereço do arquivo csv dos registros
category_csv = Path('categorias.csv')


# Teste para verificar se esso arquivo existe

# Caso exista carrega o CSV como dataframe para a aplicação
if category_csv.is_file():
    st.session_state['category_df'] = pd.read_csv(category_csv)

# Caso não exista, cria um dataframe novo
else:
    st.session_state['category_df'] = pd.DataFrame(columns=category_columns_names)

# Inverta a ordem das linhas para exibir os registros mais recentes no topo
st.session_state['category_df'] = st.session_state['category_df'].sort_values(by='Nome')
#-----------------------------------------------------------------------



# Título da página
st.title("Registros de Atividades")

############ Formulário para novos registros ########################

# Criação do objeto do formulário
form_add_register = st.form(key="Novo Registro", clear_on_submit=True)

# Caixa de texto para a descrição
text_description = form_add_register.text_input("Descrição:")

category_selected = form_add_register.selectbox(label="Categoria", options=st.session_state['category_df']['Nome'])

# Botão para envio do formulário
register_form_submitted = form_add_register.form_submit_button(label="Salvar", use_container_width=True)

#######################################################################

########## Lógica de registro de dados no dataframe e csv #############
if register_form_submitted:
    
    # Pega o data e hora atual no horário de Brasília
    now = datetime.now(pytz.timezone('America/Sao_Paulo'))
    
    # Verifica se dataframe não está vazio
    if not st.session_state['registers_df'].empty:
        
        # Obtenha a data e hora do fim da atividade mais recente
        last_record_time = st.session_state['registers_df']['Data e Hora Fim'].iloc[0]
    else:
        # Se não houver registros anteriores, use o horário atual como início
        last_record_time = now  
    
    # Calcule a duração em minutos entre o início da atividade mais recente e o horário atual
    duration_minutes = (now - last_record_time).total_seconds() / 60
    
    # Registro de nova atividade com horário de início e fim
    register_new_row = {
        "Descrição": text_description,
        "Data e Hora Início": last_record_time,
        "Data e Hora Fim": now,
        "Duração (min)": duration_minutes,
        "Categoria": category_selected
    }
    
    # Cria um dataframe de uma linha só com os novos dados para depois concatenar
    register_new_row_df = pd.DataFrame(register_new_row, index=[0])
    
    # Concatena o dataframe principal com a nova linha na forma de dataframe
    st.session_state['registers_df'] = pd.concat([register_new_row_df, st.session_state['registers_df']], ignore_index=True)

    # Salvar os dados em um arquivo CSV
    st.session_state['registers_df'].to_csv(registers_csv, index=False)

#####################################################################


################## Exibição do Dataframe organizado ##################

# Inverta a ordem das linhas para exibir os registros mais recentes no topo
st.session_state['registers_df'] = st.session_state['registers_df'].sort_values(by='Data e Hora Fim', ascending=False)

# Exibe o dataframe do mais recente para o mais antigo
st.dataframe(st.session_state['registers_df'], use_container_width=True, hide_index=True)

######################################################################


################## Categorias #######################################



################# Lista das categorias e formulário #################

with st.expander("Categorias"):
    ############ Formulário para novos registros ########################

    # Criação do objeto do formulário
    form_add_category = st.form(key="Nova Categoria", clear_on_submit=True)

    # Caixa de texto para a descrição
    category_name = form_add_category.text_input("Categoria:")
    category_emoji = form_add_category.text_input("Emoji:")

    # Botão para envio do formulário
    category_form_submitted = form_add_category.form_submit_button(label="Salvar", use_container_width=True)

    #######################################################################

    ########## Lógica de registro de dados no dataframe e csv #############
    if category_form_submitted:
        
        # Registro de nova atividade com horário de início e fim
        category_new_row = {
            "Nome": category_name,
            "Emoji": category_emoji,
        }
        
        # Cria um dataframe de uma linha só com os novos dados para depois concatenar
        category_new_row_df = pd.DataFrame(category_new_row, index=[0])
        
        # Concatena o dataframe principal com a nova linha na forma de dataframe
        st.session_state['category_df'] = pd.concat([category_new_row_df, st.session_state['category_df']], ignore_index=True)

        # Salvar os dados em um arquivo CSV
        st.session_state['category_df'].to_csv(category_csv, index=False)

    #####################################################################


    ################## Exibição do Dataframe organizado ##################

    # Inverta a ordem das linhas para exibir os registros mais recentes no topo
    st.session_state['category_df'] = st.session_state['category_df'].sort_values(by='Nome')

    # Exibe o dataframe do mais recente para o mais antigo
    st.dataframe(st.session_state['category_df'], use_container_width=True, hide_index=True)

    ######################################################################
    
    