import streamlit as st
import zipfile
import os
from my_functions import *
import shutil
import pandas as pd


# Streamlit app title
st.title("Data Processing App")

# Upload a zip file
uploaded_file = st.file_uploader("Upload a Zip File", type=["zip"])

if uploaded_file:

    # Create a temporary directory to extract the files
    temp_dir = "temp_zip_extract"
    os.makedirs(temp_dir, exist_ok=True)


    # Extract the zip file
    with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
        zip_ref.extractall(temp_dir)

    # List and display the files in the zip
    st.write("Files in the Zip:")
    for root, _, files in os.walk(temp_dir):
        for file in files:
            st.write(file)

if os.path.exists("temp_zip_extract"):
    shutil.rmtree("temp_zip_extract")
    
# Upload an Excel file
uploaded_file = st.file_uploader("Upload an Excel File for Weights", type=["xlsx", "xls"])

if uploaded_file is not None:
    # Read the Excel file into a DataFrame
    df = pd.read_excel(uploaded_file)

    # Display the DataFrame
    st.write("Data from the Excel file:")
    st.dataframe(df)