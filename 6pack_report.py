import streamlit as st
import backend



with st.form("my_form"):
   #st.write("Please upload ")
   am_dispatch = st.file_uploader('Upload AM Dispatch Excel file')
   crew_lineup_sheet = st.file_uploader('Upload Crew Line-up Excel File')
   size = st.selectbox('Consist Size', ['L6','L10','L12'])
   st.form_submit_button('Generate Report')

if am_dispatch is not None and crew_lineup_sheet is not None:
 
    
    
   generated_file_name = backend.main(am_dispatch, crew_lineup_sheet, size)


   with open(generated_file_name, 'rb') as file:
        st.download_button(label = 'Download Report',
                    data = file, 
                    file_name = generated_file_name, 
                    mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',


                    )

