import PyPDF2
import json
import pandas as pd
import traceback


def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise Exception("error reading the pdf file and error is ", e)
    elif file.name.endswith("txt"):
        return file.read().decode("utf-8")
    else:
        raise Exception("unsupported file format only pdf and text format are accepted")


def get_table_data(quiz_str):
    try:
        # convert quiz from str to dict
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []

        # iterate over the quiz dictionary and extract the required information
        for key, value in quiz_dict.items():
            mcq = value["mcq"]
            options = " || ".join(
                [
                    f"{option}: {option_value}"
                    for option, option_value in value["options"].items()
                ]
            )
            correct = value["correct"]
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})
        return quiz_table_data
    except Exception as e:
        raise Exception("got error while return table data and it is : ", e)

