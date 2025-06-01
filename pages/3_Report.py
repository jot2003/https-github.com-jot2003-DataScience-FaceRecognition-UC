import streamlit as st
from Home import face_reco
# st.set_page_config(page_title='Reporting', layout='wide')
st.subheader('Reporting')

#Retrive logs data and show in Report.py
#Extract data from redis list
name = 'attendance:logs'
def load_logs(name, end=-1):
    logs_list = face_reco.r.lrange(name, start=0, end=end) #extract all data from the redis database
    return logs_list

#tabs to show the info
tab1, tab2 = st.tabs(['Registered Data', 'Logs'])
with tab1:
    if st.button('Refresh Data'):
        #Retrieve the data from the redis database
        with st.spinner('Retrieving Data from Redis DB ...'):
            redis_face_db = face_reco.retrieve_data(name='academy:register')
            st.dataframe(redis_face_db[['Name', 'Role']])
with tab2:
    if st.button('Refresh Logs'):
        st.write(load_logs(name=name))


