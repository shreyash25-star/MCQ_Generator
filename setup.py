from setuptools import find_packages,setup

setup(
    name='mcqgenrator',
    version='0.0.2',
    author='Shreyash Patil',
    author_email='pshreyash195@gmail.com',
    install_requires=["langchain","streamlit","python-dotenv","PyPDF2","google-generativeai"],
    packages=find_packages()
)