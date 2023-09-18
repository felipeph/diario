import streamlit as st

from functions import load_or_create_df, new_row_to_csv, time_now, last_record_time

records_file = "records.csv"
records_columns_names = ["description",
                          "date_time_end",
                          "date_time_start",
                          ]
st.session_state["records_df"] = load_or_create_df(records_file, records_columns_names)
records_df = st.session_state["records_df"]
records_df = records_df.astype(str)


with st.form(key="Novo Registro", clear_on_submit=True):
    new_record_description = st.text_input("Descrição")
    now = time_now()
    last_record_end_time = last_record_time(records_df)
    new_record_values = [new_record_description,
                         now,
                         last_record_end_time,
                         ]
    new_record_submitted = st.form_submit_button(label="Salvar", use_container_width=True)

if new_record_submitted:
    new_row_to_csv(records_file, records_df, records_columns_names, new_record_values)
    st.success("Novo registro realizado com sucesso.")
    #st.experimental_rerun()

st.table(records_df)



st.download_button(
    label="Baixar dados como CSV",
    data=records_df.to_csv(index=False),
    file_name='records.csv',
    mime='text/csv',
)
    
# ---------------- Debug---------------------
st.sidebar.write(st.session_state)
st.sidebar.write(records_df)
st.sidebar.write(records_df.dtypes)
# -------------------------------------------