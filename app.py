
import streamlit as st
import pandas as pd
import os
import glob
import numpy as np
import re
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import webbrowser

from process_funcs import *

# Create a sidebar
st.sidebar.title("About the Project")

# Write a description of the project
st.sidebar.write(
    '''
    This is a custom data processing app. 
    It allows users to input multiple Excel files and generates information in the specific format.
    '''
)

header = st.container()
dataset = st.container()
results = st.container()

with header:
    st.title('Program Objectives Project')
    
    # Instructions text
    instructions = """
    #### App Instructions

    This is a custom app for computing the Program Objectives for graduates. Follow these instructions to use the app:

    1. Upload course evaluation reports.
    2. Upload the graduation list.
    3. Upload the course list file.
    4. Click 'Run Task' button.

    """

    # Display the instructions on the app
    st.markdown(instructions)
    
with dataset:
    st.subheader('Step 1 - Upload Course Evaluation Reports')

    eval_files = st.file_uploader("Upload the Excel files (Upload ALL Reports)", accept_multiple_files=True, key='file_uploader1')
    st.write(f'{len(eval_files)} files are uploaded.')


    st.subheader('Step 2 - Upload the Graduation List')
    
    
    ###################################
    # Sample DataFrame
    data = {'Öğrenci': [],
            'No': [],
            'Adı': [],
            'Soyadı': [],
            'Durumu': [],
            'Akademik Birim': [],
            'Mezuniyet Yılı': [],
            'Mezuniyet Tarihi': []
            }
    df = pd.DataFrame(data)
    
    # Add a button to open the DataFrame in a new tab
    if st.button("Show the format of the Graduation List in New Tab"):
        # Save the DataFrame to an HTML file
        df.to_html("dataframe.html", index=False)

        # Open the HTML file in a new tab
        new_tab_url = "dataframe.html"
        webbrowser.open_new_tab(new_tab_url)
    ###################################
        

    # Create a file uploader
    grad_list_file = st.file_uploader("Choose an Excel file", key='file_uploader2')

    # Read the uploaded file to a Pandas DataFrame
    if grad_list_file is not None:
        df_mezun_list = pd.read_excel(grad_list_file)
        disp_df = df_mezun_list.style.format(precision=0, thousands='')
        # Display the DataFrame
        st.write(disp_df)

    st.subheader('Step 3 - Upload the Course List File')
    # Create a file uploader
    course_list_file = st.file_uploader("Choose an Excel file", key='file_uploader3')

    # Read the uploaded file to a Pandas DataFrame
    if course_list_file is not None:
        df_pc_dersler = pd.read_excel(course_list_file)
        
        # Apply the extract_pattern function to each row in the 'Dersler' column
        df_pc_dersler['Dersler'] = df_pc_dersler['Dersler'].apply(extract_pattern)

        # Display the DataFrame
        st.write(df_pc_dersler)
    
with results:
    # Add a button to trigger the action
    if st.button("Run Task"):
        
        if eval_files is not None and grad_list_file is not None and course_list_file is not None:
        
        
            # Display a waiting spinner while the task is running
            with st.spinner("Running the task..."):

                # Get all excel files in the folder as list of dataframes
                all_df = process_excel_files(eval_files)

                # Preprocess these dataframes
                processed_df = [preprocess_data(df) for df in all_df]

                # Store the id's in a list
                mezun_list = list(df_mezun_list['Öğrenci No'])

                # Get result_dfs
                result_dfs = extract_rows_by_id(processed_df, mezun_list)

                # Remove the empty dataframes of students and get which ones are deleted
                result_dfs, deleted_ids = delete_empty_dfs(result_dfs, mezun_list)

                # Create a dataframe of deleted ones
                deleted_students = df_mezun_list[df_mezun_list['Öğrenci No'].isin(deleted_ids)]
                deleted_students = deleted_students.style.format(precision=0, thousands='')

            # Task completed, remove the spinner
            st.success("Task completed!")
        
            # st.title('Deleted ones')
            # st.dataframe(deleted_students)

            st.title('Result')
            df = process_result_dfs_v3(result_dfs, df_pc_dersler)
            df = append_average_row(df)
            st.table(df)

            # Create a download button
            def download_excel():
                df.to_excel('dataframe.xlsx', index=False)
                with open('dataframe.xlsx', 'rb') as f:
                    data = f.read()
                st.download_button(
                    label="Download Excel File",
                    data=data,
                    key='download_excel',
                    file_name='dataframe.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                )

            # Call the download button function
            download_excel()
            
        else: # when the files are not uploaded
            # Display a warning message
            st.warning("This is a warning message. Please upload the necessary files.")
            
