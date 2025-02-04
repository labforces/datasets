import streamlit as st
import pandas as pd
import io
import os
from datetime import datetime, timedelta
import folium
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    df = pd.read_parquet(file)
    return df

@st.cache_data
def load_data_returns():
    df = pd.read_parquet(file_return)
    return df


@st.cache_data
def load_data_withdraw():
    df = pd.read_parquet(file_withdraw)
    return df

file = r'C:\Users\l.Islomkhujaev\Desktop\Streamlit\january-september.parquet'
file_return = r'C:\Users\l.Islomkhujaev\Desktop\Streamlit\january-september-returns.parquet'
file_withdraw = r'C:\Users\l.Islomkhujaev\Desktop\Streamlit\january-september-withdraw.parquet'
pdf_returns = load_data_returns()
pdf_withdraw = load_data_withdraw()
pdf = load_data()


# Создайте список страниц
pages = ["Промо Календарь", "Информация по товару","Найти товар" , "Краткое инфо 2023г", 'Компенсации','Список_маркетов', 'Карта']

# Выберите страницу из боковой панели
selected_page = st.sidebar.selectbox("Выберите страницу", pages)


# Отобразите контент, соответствующий выбранной странице
if selected_page == "Промо Календарь":
    
    st.title('Промо :blue[Календарь]:')
    
    os.chdir(r"C:\Users\l.Islomkhujaev\Desktop\Streamlit")

    df = pd.read_excel('Промо календарь.xlsx')
    
    df = df.fillna('-')
    
    df['Период подачи позиций'] = df['Период подачи позиций'].dt.strftime("%d/%m/%y")
    
    
    def calculate_date_difference(specific_date_str):

      # Convert the specific date string to a datetime object
      specific_date = pd.to_datetime(specific_date_str,format = '%d/%m/%y')
    
      # Get today's date as a datetime object
      today = pd.to_datetime('today',format = '%d/%m/%y')
    
      # Calculate the difference in days
      difference = specific_date - today

      # Return the number of days
      if difference.days < 0:
          return 0
      else:
          return difference

    df['Осталось до сдачи'] = df['Период подачи позиций'].apply(calculate_date_difference)
    
    new_order = ['Вид акции','Старт-окончание регулярного промо','Период подачи позиций', 'Осталось до сдачи', 'Комментарии']
    
    df = df[new_order]
    
    st.dataframe(df, width=800, height = 500)
    

elif selected_page == "Информация по товару":
    
    
    
    option_sap = st.multiselect('Выберите код',
                              (pdf[['Материал']].drop_duplicates()))
    

    option_month = st.multiselect('Выберите месяц',
                              (pdf[['Месяц']].drop_duplicates()))
    
    
    st.title('Инфо :blue[ТО , FM , Списание , Ретро , Возврат]:')
    
    by_sap = pdf[(pdf['Материал'].isin(list(option_sap))) & (pdf['Месяц'].isin(list(option_month)))].pivot_table(index = ['Материал','Название материала'],
                                                                     values = ['Стоимость за ЕИ нетто','Марж. Прибыль'],
                                                                     aggfunc = 'sum')
    
    by_sap['Маржа %'] = round((by_sap['Марж. Прибыль'] / by_sap['Стоимость за ЕИ нетто']) * 100,2)
    
    by_sap_returns = pdf_returns[(pdf_returns['Материал'].isin(list(option_sap))) & (pdf_returns['Месяц'].isin(list(option_month)))].groupby('Материал')[['Сумма во ВВ','Кол-во в ЕИ ввода']].sum().reset_index()
    
    by_sap = by_sap.merge(by_sap_returns,how='left', on='Материал')
    
    by_sap = by_sap.rename(columns = {
        'Сумма во ВВ':'Возвраты сумм',
        'Кол-во в ЕИ ввода':'Возвраты шт'
        })
    
    by_sap_withdraw = pdf_withdraw[(pdf_withdraw['Материал'].isin(list(option_sap))) & (pdf_withdraw['Месяц'].isin(list(option_month)))].groupby('Материал')[['Сумма во ВВ','Кол-во в ЕИ ввода']].sum().reset_index()
    
    by_sap = by_sap.merge(by_sap_withdraw,how='left', on='Материал')
    
    
    by_sap = by_sap.rename(columns = {
        'Сумма во ВВ':'Списания сумм',
        'Кол-во в ЕИ ввода':'Списания шт'
        })
    

    st.dataframe(by_sap)

    
    st.title('Инфо :blue[Продажи в шт]:')
    
    
    by_sap_quantity = pdf[(pdf['Материал'].isin(list(option_sap))) & (pdf['Месяц'].isin(list(option_month)))].pivot_table(index = ['Наименование иерарх группы мат 4 уровень'
                                                                                                                                   ,'Название материала'],
                                                                     columns = ['Месяц'],                                                 
                                                                     values = ['ФактурКоличество'],
                                                                     aggfunc = 'sum')


    

    st.dataframe(by_sap_quantity)
    
    if len(option_sap) == 1:
        
        by_sap_price = pdf[(pdf['Материал'].isin(list(option_sap))) & (pdf['Месяц'].isin(list(option_month)))]
        by_sap_rating = pdf[pdf['Месяц'].isin(list(option_month))].groupby('Материал')['ФактурКоличество'].sum().reset_index()
        by_sap_rating['Рейтинг'] = by_sap_rating['ФактурКоличество'].rank(ascending = False)
        
        st.metric("РЦ", round(by_sap_price[['Розничная цена']].max().iloc[0]))
        st.metric('Рейтинг',round(by_sap_rating[by_sap_rating['Материал'] == int(option_sap[0])]['Рейтинг'].iloc[0]))
        
    else:
        pass
    
elif selected_page == "Найти товар":
    
    # Create a search input
    search_query = st.text_input("Искать по наименованию:")
    
    # Filter the DataFrame based on the search query
    filtered_df = pdf[pdf['Название материала'].str.contains(search_query, case=False)][['Материал','Название материала']]
    
    # Display the filtered results
    st.write(filtered_df)
    

    
# elif selected_page == 'Информация по группе':
    


# elif selected_page == 'Компенсации':


    
# elif selected_page == 'Список_маркетов':
    

    

# elif selected_page == 'Карта':

