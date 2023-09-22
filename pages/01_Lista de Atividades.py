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

with st.container():
    st.table(activities_df)

with st.container():
    st.title("Lista de Atividades")
    
with st.container():
    with st.form(key="Nova Atividade", clear_on_submit=True):
        new_activity_name = st.text_input(label="Nova Atividade")
        new_activity_values = [new_activity_name.strip()]
        new_activity_submmited = st.form_submit_button(label="Salvar", use_container_width=True)
        if new_activity_submmited:
            f.new_row_to_csv(p.activities_csv, activities_df, l.activities_columns, new_activity_values)
            st.rerun()

with st.container():
    st.table(activities_df)