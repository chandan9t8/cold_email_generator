# Cold Email Generator

This application is used to generate cold emails to recruiters based on the link to the job posting. It extracts the job
description from the link and generates personalised cold emails by including relevant portfolio links from
your profile that matches the Job description.

## Tech Stack
- Llama 3.1 (70b)
- Langchain : open-source framework used for developing applications powered by large language models (LLMs)
- Groq : For faster inference
- Streamlit : for creating quick data-driven web applications


## Run the app
- Copy the API key for Groq and set it as an environment variable using `export GROQ_API_KEY = "your_API_key"`
- `pip install -r requirements.txt`
- `streamlit run ./app/main.py`

