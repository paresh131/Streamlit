import streamlit as st
import plotly.io as pio
from plotly.subplots import make_subplots
from plotly.graph_objs import *
import plotly.graph_objects as go
from matplotlib import cm
import plotly.express as px

import numpy as np
import json
import urllib.request


from operator import index
import gspread
from matplotlib.pyplot import prism
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import pandas as pd
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("smooth-comfort-350907-f0c98ac8a58c.json", scope)

client = gspread.authorize(creds)

sheet = client.open("cfpa data sheet").sheet1  # Open the spreadhseet

data = sheet.get_all_records()  # Get a list of all records

# convert the json to dataframe
records_df = pd.DataFrame.from_dict(data)

# view the top records
# records_df.head()
# print(records_df
# )
#records_df['complaint_sum']=pd.tprecords_df['complaint_id'].sum()
#print(records_df['complaint_sum'])
# records_df['MonthYear']=(pd.to_datetime(records_df['MonthYear'],unit='d',origin='1900-01-01')-pd.Timedelta(2, "d")).dt.date

# df_latest=records_df[records_df['MonthYear']==records_df['MonthYear'].max()]

total_complaints=pd.to_numeric(records_df['complaint_id']).sum()
print(total_complaints)
print(pd.to_numeric(records_df['complaint_id']).sum())
print(pd.to_numeric(records_df.loc[records_df['company_response'] == 'Closed with explanation', 'complaint_id']).sum())
print(pd.to_numeric(records_df.loc[records_df['company_response'] == 'In progress', 'complaint_id']).sum())
#print(pd.to_numeric(records_df.loc[records_df['timely'] == 'In progress', 'complaint_id']).sum())
perce=pd.to_numeric(records_df.loc[records_df['timely'] == 'Yes','complaint_id']).sum()/total_complaints
print(perce)
def create_kpi(val,text,format,color,header_size,value_size):
	return (go.Indicator(
        value = val,
        title= {"text":text,"font":{"size":15}},
        number={'valueformat':format,"font":{"size":50,"family":'Times New Roman',"color": color}}
    ))

#records_df['date_received'] = pd.to_datetime(records_df['date_received']).dt.to_period('m')
with st.container():
    c1, c2, c3, c4,c5 = st.columns(5)
    c1.plotly_chart(go.Figure(create_kpi(total_complaints,'Total Number of Complaints',',d%','#000000',20,80)).update_layout(autosize=True,width=200,height=150))
    c2.plotly_chart(go.Figure(create_kpi(pd.to_numeric(records_df.loc[records_df['company_response'] == 'Closed with explanation', 'complaint_id']).sum(),'CP-Closed Status',',d%','#000000',20,80)).update_layout(autosize=True,width=200,height=150))
    c3.plotly_chart(go.Figure(create_kpi(pd.to_numeric(records_df.loc[records_df['timely'] == 'Yes','complaint_id']).sum()/total_complaints,'% OF TRC',',d%','#000000',20,80)).update_layout(autosize=True,width=200,height=150))
    c4.plotly_chart(go.Figure(create_kpi(pd.to_numeric(records_df.loc[records_df['company_response'] == 'In progress', 'complaint_id']).sum(),'CP-IN Process Status',',d%','#000000',20,80)).update_layout(autosize=True,width=200,height=150))
    state_filter = st.selectbox("Select the State", pd.unique(records_df["state"]))

    records_df = records_df[records_df["state"] == state_filter]
    

    # header1_fig.add_trace(
	# 	create_kpi(temp_df['Cumulative tests performed'].sum(),'Test Performed',',.0f','#7f7f7f',15,50), row=1, col=2
	# )

	# header1_fig.add_trace(
	# 	create_kpi(temp_df['Cumulative Test positive'].sum(),'Test Postive',',.0f','#7f7f7f',15,50), row=1, col=3
	# )

	# header1_fig.add_trace(
	# 	create_kpi(temp_df['Still admitted'].sum(),'Still Admitted',',.0f','#7f7f7f',15,50), row=1, col=4
	# )

complaints_month_fig, complaints_prod_fig = st.columns(2)
complaints_issue_fig, complaints_status_fig = st.columns(2)

complaints_prod = records_df.groupby(['product']).size().reset_index(name='count').sort_values(by='count', ascending=True)
with complaints_prod_fig:
    st.subheader("Complaints by Product")
    fig = px.bar(complaints_prod, x='product', y='count')
    st.write(fig)

complaints_status = records_df.groupby(['submitted_via']).size().reset_index(name='count').sort_values(by='count', ascending=True)


# with complaints_issue_fig:
#     st.subheader("Complaints by Issue and Sub-Issue")
#     fig = px.treemap(complaints_issue, path=['issue', 'sub_issue'], values='count')
#     st.write(fig)
with complaints_status_fig:
    st.subheader("Complaints by Submitted via")
    fig = px.pie(complaints_status, values='count', names='submitted_via')
    st.write(fig)


#records_df['month'] = records_df['MonthYear'].dt.month
#records_df['date_received'] = pd.to_datetime(records_df['date_received']).dt.to_period('m')
complaints_month = records_df.groupby(['MonthYear']).size().reset_index(name='count').sort_values(by='MonthYear', ascending=True)


with complaints_month_fig:
    st.subheader("Complaints by Month")
    fig = px.line(complaints_month , x='MonthYear', y='count')
    st.write(fig)
