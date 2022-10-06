import pandas as pd
import streamlit as st

uploaded_file1 = st.file_uploader("Upload downloaded file from Zoho")
uploaded_file2 = st.file_uploader("Upload Goled Kft file")
 
if uploaded_file1 and uploaded_file2:
    option = st.selectbox('Please select a sheet!',pd.ExcelFile(uploaded_file2.name).sheet_names)
        
    if st.button('Execute'):
        orders = pd.read_excel(uploaded_file1.name)
        orders_sent = pd.read_excel(uploaded_file2.name,sheet_name=option,header=None, names=['Number', 'Invoice', 'Date'])
         
        orders_sent['Number'] = 'HU' + orders_sent['Number'].astype(str)
        orders_sent['Number'] = orders_sent['Number'].replace('HUSO','SO', regex=True)
        orders_sent['Number'] = orders_sent['Number'].replace('HUso','SO', regex=True)
        orders_sent_list = orders_sent["Number"].to_list()

        df = pd.concat([orders[orders["PurchaseOrder"].isin(orders_sent_list)], orders[orders["SalesOrder Number"].isin(orders_sent_list)]], axis=0)

        csv =  df.groupby("SKU").agg({"QuantityOrdered":"sum"}).to_csv(sep=";").encode('utf-8')

        st.download_button(label="Download",data=csv,file_name=option+'.csv',mime='text/csv')
