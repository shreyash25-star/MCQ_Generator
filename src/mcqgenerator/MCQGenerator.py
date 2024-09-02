import os
from dotenv import load_dotenv
import google.generativeai as genai
from operator import itemgetter

from langchain.chains.question_answering import load_qa_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from src.mcqgenerator.logger import logging
# from src.mcqgenerator.utils import read_file,get_table_data


# from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
# from langchain.callbacks import get_openai_callback


# take environment variables from .env.
load_dotenv()
key=os.getenv("google_api_key")

#setup and configure gemini LLM model
genai.configure(api_key=key)
llm = ChatGoogleGenerativeAI(model="gemini-pro")

#Defining a template for LLM
TEMPLATE="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  of {number} multiple choice questions for students in good tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}

"""

# Defining a prompt template by passing in the input variables and template
quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "response_json"],
    template=TEMPLATE
    )

def invoke_responce(inputs):
    # query = inputs['query'] # <-- Must unpack the dictionary to extract the query
    # documents = retriever.invoke(query)
    index = inputs["index"]
    text = index["text"]
    number = index["number"]
    response_json = index["responce_json"]
    model_input = quiz_generation_prompt.invoke({'text': text, 'response_json': response_json, 'number': number})
    model_output = llm.invoke(model_input)
    parser = StrOutputParser()
    parsed_output = parser.invoke(model_output)
    return parsed_output

# invoke_rag({"var_a": "foo", "var_b": "bar", "query": query})





# Creating a quiz chain by using llm model and prompt template and stroring output in quiz variable
# quiz_chain=load_qa_chain(llm=llm, prompt=quiz_generation_prompt)
quiz_chain =  quiz_generation_prompt | llm
# Creating a template to evaluate the output quiz
# TEMPLATE2="""
# You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
# You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis.
# if the quiz is not at per with the cognitive and analytical abilities of the students,\
# update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
# Quiz_MCQs:
# {quiz}
#
# Check from an expert English Writer of the above quiz:
# """

#defining a evaluation prompt template by using input variables and template
# quiz_evaluation_prompt=PromptTemplate(input_variables=["subject", "quiz"], template=TEMPLATE2)
#
# #defining review chain b  using evaluation prompt and llm
# # review_chain=LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)
# review_chain = quiz_evaluation_prompt |llm
#
# generate_evaluate_chain=SequentialChain(chains=[quiz_chain, review_chain], input_variables=["text", "number", "subject", "tone", "response_json"],
#                                         output_variables=["quiz", "review"], verbose=True,)

