import streamlit as st
import pandas as pd
import io
import os
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

#@st.cache_data
#def load_data():
 #   df = pd.read_parquet(file)
 #   return df

#@st.cache_data
#def load_data_returns():
 #   df = pd.read_parquet(file_return)
  #  return df


#@st.cache_data
#def load_data_withdraw():
 #   df = pd.read_parquet(file_withdraw)
  #  return df

#file = r'C:\Users\l.Islomkhujaev\Desktop\Streamlit\january-september.parquet'
#file_return = r'C:\Users\l.Islomkhujaev\Desktop\Streamlit\january-september-returns.parquet'
#file_withdraw = r'C:\Users\l.Islomkhujaev\Desktop\Streamlit\january-september-withdraw.parquet'
#pdf_returns = load_data_returns()
#pdf_withdraw = load_data_withdraw()
#pdf = load_data()


# Создайте список страниц
pages = ["Промо Календарь", "Информация по товару","Найти товар" , "Краткое инфо 2023г", 'Компенсации','Список_маркетов', 'Карта']

# Выберите страницу из боковой панели
selected_page = st.sidebar.selectbox("Выберите страницу", pages)


# Отобразите контент, соответствующий выбранной странице
if selected_page == "Промо Календарь":
    
    st.title('Промо :blue[Календарь]:')

    df = pd.read_excel('Промо календарь.xlsx')
    
    st.dataframe(df, width=800, height = 500)
    

