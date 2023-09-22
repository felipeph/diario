import streamlit as st
import pandas as pd

# Pytz para ajuste de timezone
import pytz

# Datetime para pegar a hora e a data atual
from datetime import datetime

from pathlib import Path


def load_or_create_df(csv_file, columns_names_list):
    """
    Load a dataframe from a CSV if it exists or create an empty dataframe from a list of name of columns
    
    Args:
        csv_file (str): The file path of the CSV to create a dataframe from
        columns_names_list (list): List of names for the header of the new dataframe
        
    Returns:
        dataframe : Empty or full, depending on the CSV file given
        
    """
    csv_file_path = Path(csv_file)
    try:
        dataframe = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        dataframe = pd.DataFrame(columns=columns_names_list)

    return dataframe

def new_row_to_csv(csv_file, dataframe, df_columns_names, new_row_values):
    """
    Add a new row to a dataframe and save it into the CSV file
    
    Args:
        csv_file (str): The file path of the CSV file to save into.
        dataframe (dataframe): Original Pandas dataframe to include de new row
        df_columns_names (list): List of names for the header of the new dataframe
        new_row_values (list): List of values with for the columns
    
    Returns:
        status
    
    """

    try:
        new_row_dict = dict(zip(df_columns_names, new_row_values))
        new_row_df = pd.DataFrame(new_row_dict, index=[0])
        dataframe = pd.concat([new_row_df, dataframe], ignore_index=True)
        dataframe.to_csv(csv_file, index=False)
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}.")
    return None

def time_now():
    """
    Return the time right now in Brazil official timezone
    """
    return datetime.now(pytz.timezone('America/Sao_Paulo'))
    
def last_record_time(dataframe):
    # Verifica se dataframe não está vazio
    dataframe = convert_registers_to_datetime(dataframe)
    if not dataframe.empty:
        
        # Obtenha a data e hora do fim da atividade mais recente
        last_record_time = dataframe['date_time_end'].iloc[0]
    else:
        # Se não houver registros anteriores, use o horário atual como início
        last_record_time = time_now()
    return last_record_time

def convert_registers_to_datetime(df):
    df["date_time_start"] = pd.to_datetime(df["date_time_start"])
    df["date_time_end"] = pd.to_datetime(df["date_time_end"])
    return df