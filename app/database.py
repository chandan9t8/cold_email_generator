import pandas as pd
import chromadb as ch
import uuid

class Database:

    def __init__(self, file_path = './app/resources/Portfolio.csv'):
        self.file_path = file_path
        self.data = pd.read_csv(self.file_path)
        self.client = ch.PersistentClient('myVectorStore')
        self.collection = self.client.get_or_create_collection(name='myPortfolio')

    def store_portfolio(self):
        """
        stores the portfolio links in the vector database
        """
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(documents=row["Techstack"],
                               metadatas={"links": row["Link to portfolio"]},
                               ids=[str(uuid.uuid4())]  # universally unique identifiers for each record
                               )


    def get_links(self, skills):
        """
        :param skills: The skills in the job description
        :return: links that match the skills in JD
        """
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])