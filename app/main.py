import streamlit as sl
from chains import Chain
from langchain_community.document_loaders import WebBaseLoader
from database import Database
from utils import format_text

def cold_email_generator_app(llm, database, format_text):
    sl.title("Cold Email Generator")
    url_input = sl.text_input("Enter a URL:", value="https://")
    submit_button = sl.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            cleaned_text = format_text(loader.load().pop().page_content)
            database.store_portfolio()
            job_descr = llm.extract_job_descr(cleaned_text)

            for field in job_descr:
                skills = field.get('skills', [])
                links = database.get_links(skills)
                email = llm.generate_email(job_descr,links)
                sl.code(email, language='markdown')

        except Exception as e:
            sl.error(f"An error occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    database = Database()
    sl.set_page_config(layout = "wide", page_title = "Cold Email Generator")
    cold_email_generator_app(chain, database, format_text)

