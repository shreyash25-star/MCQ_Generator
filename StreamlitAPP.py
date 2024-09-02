import os
import json

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from src.mcqgenerator.logger import logging
from src.mcqgenerator.MCQGenerator import quiz_chain,invoke_responce
from src.mcqgenerator.utils import read_file, get_table_data
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

with open(
        r'H:\hi\automated_mcq\Response.json') as file:
    RESPONCE_JSON = json.load(file)


# creating the title for the app
st.title("Assessment Created Application using GenAI")

# creating a form
with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Upload a pdf file or a text file")
    mcq_count = st.number_input("No of Question you want?", min_value=3, max_value=50)
    # subject = st.text_input("Insert Subject", max_chars=20)
    # tone = st.text_input("Complexity level of Question", max_chars=20, placeholder="Simple")
    button = st.form_submit_button("Create MCQs")

    #df = None

    if button and uploaded_file is not None and mcq_count :
        with st.spinner("Generation is in process"):
            try:
                text = read_file(uploaded_file)
                inputs =  \
                    {
                    "index":
                        {
                        "number": mcq_count,
                        "responce_json": json.dumps(RESPONCE_JSON),
                        # "subject": subject,
                        "text": text,
                        # "tone": tone,
                        }
                    }
                # print(inputs["index"]["responce_json"])
                # responce = quiz_chain.invoke(inputs)
                responce = invoke_responce(inputs)

            except Exception as e:
                raise Exception("error occured due to : ",e)
                st.error("Error occured")
            else:
                if isinstance(responce, dict):
                    quiz = responce.get("quiz", None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)
                            st.text_area(label="Review", value=responce["review"])
                        else:
                            st.error("Error in the table data")
                else:
                    st.write(responce)


