import streamlit as st

import functions as f

import params.files as p

import params.lists as l

####################### Interface ##########################
# [] Título 
# [] Formulário que contenha a atividade como selectbox e uma input_text
# [] Botão de salvar
# [] Lista de registros
############################################################

activities_df = f.load_or_create_df(p.activities_csv, l.activities_columns)
records_df = f.load_or_create_df(p.records_csv, l.records_columns)
records_df = f.convert_registers_to_datetime(records_df)

with st.container():
    st.title("Registro de Atividades")
    
with st.container():
    with st.form(key="Novo Registro", clear_on_submit=True):
        new_register_activity = st.selectbox(label="Atividade:", options=activities_df.sort_values(by="activity"))
        new_register_start = f.last_record_time(records_df)
        new_register_end = f.time_now()
        new_register_duration = new_register_end - new_register_start
        new_register_values = [new_register_activity, new_register_start, new_register_end, new_register_duration]
        new_register_submmited = st.form_submit_button(label="Salvar", use_container_width=True)
        if new_register_submmited:
            f.new_row_to_csv(p.records_csv, records_df, l.records_columns, new_register_values)
            st.rerun()

with st.container():
    st.table(records_df)

    