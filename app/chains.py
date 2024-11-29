from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import os

class Chain:

    def __init__(self):
        self.model =  ChatGroq(temperature=1,
                               groq_api_key=os.getenv("GROQ_API_KEY"),
                               model_name="llama-3.1-70b-versatile")

    def extract_job_descr(self, text):

        """
        :param text: cleaned text from the scraped job description
        :return: JSON object containing the mentioned fields in the below template
        """

        prompt_job_description = ChatPromptTemplate.from_template(
            """
            
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            
            ### INSTRUCTION:
            The above text is scraped from the careers page of a website. Your task is to extract job posting 
            and return it in a JSON format. The JSON object should contain the following keys:
                - `role`: The job title or role.
                - `experience`: Experience required for the role.
                - `skills`: A list of required or preferred skills.
                - `description`: A brief description of the role.
            
            Rules:
            1. If a key is missing in the scraped data, use `null` for its value.
            2. Ignore irrelevant content.
            3. Only return the valid JSON object (no preamble or additional text).
        
            ### OUTPUT FORMAT:
                {{
                    "role": "Example Role",
                    "experience": "3+ years",
                    "skills": ["Skill 1", "Skill 2"],
                    "description": "This is a sample job description."
                }},
            """
        )

        # chain model and template together
        llm_chain_extract = prompt_job_description | self.model

        # get response based from llm
        res = llm_chain_extract.invoke(input = {"page_data" : text})


        json_parser = JsonOutputParser()
        json_output = json_parser.parse(res.content)

        return json_output if isinstance(json_output, list) else [json_output]


    def generate_email(self, job_description, portfolio_links):
        """
        :param job_description:
        :param portfolio_links:
        :return:
        """

        prompt_email_generation = ChatPromptTemplate.from_template(
            """
                ### JOB DESCRIPTION:
                {job_description}
    
                ### INSTRUCTION:
                You are Chandan a highly motivated graduate student in Computer Science from Purdue Indianapolis. You have strong hands-on experience and have 
                worked on impactful projects that demonstrate your ability to solve complex problems in these domains. 
    
                Your task is to draft a personalized email for the job described above. The email should:
                1. Highlight your relevant skills and expertise based on the job description.
                2. Mention your academic background at Purdue Indianapolis.
                3. Showcase one or two of your most relevant projects, including {portfolio_list} if applicable.
                4. Clearly communicate your interest in contributing to the company’s goals and how your experience aligns with their needs.
    
                Ensure the tone is professional yet enthusiastic, and make the email concise and impactful.
    
                ### EMAIL (NO PREAMBLE):
    
            """
        )

        llm_email_chain = prompt_email_generation | self.model
        cold_email = llm_email_chain.invoke({"job_description": str(job_description), "portfolio_list": portfolio_links})

        return cold_email.content

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))