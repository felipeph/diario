import streamlit as st

import functions as f

import params.files as p

import params.lists as l

####################### Interface ##########################
# [] Título 
# [] Formulário que contenha a uma input_text
# [] Botão de salvar
# [] Lista de atividades
############################################################

activities_df = f.load_or_create_df(p.activities_csv, l.activities_columns)
activities_csv = activities_df.to_csv(index=False, encoding='utf-8')

records_df = f.load_or_create_df(p.records_csv, l.records_columns)
records_csv = records_df.to_csv(index=False, encoding='utf-8')

with st.container():
    st.title("Backup")
    
with st.container():
    st.download_button(
    label="Backup das Atividades",
    data=activities_csv,
    file_name='activities.csv',
    mime='text/csv',
    )

    st.download_button(
    label="Backup dos Registros",
    data=records_csv,
    file_name='records.csv',
    mime='text/csv',
    )