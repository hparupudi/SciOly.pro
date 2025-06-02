from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from pydantic import BaseModel, Field
from typing import List, Any
from dotenv import load_dotenv
from langchain.output_parsers import PydanticOutputParser
from pypdf import PdfReader
from langchain.docstore.document import Document
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain.chains import create_retrieval_chain, SequentialChain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re
import uuid
from pinecone import Pinecone, ServerlessSpec
import random

load_dotenv()

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--diable-dve-shm-uage')
driver = webdriver.Chrome(options=options)

topics_list = ["stellar classification", "spectral features and chemical composition", "luminosity",
"blackbody radiation", "color index and H-R diagram transitions", "H I/II regions", "molecular clouds", 
"protostars", "Herbig-Haro Objects", "T Tauri variables", "Herbig Ae/Be stars", "planet formation", "brown dwarfs", 
"protoplanetary disks", "debris disks", "exoplanets"]

llm = ChatOpenAI(model="o4-mini", api_key=os.getenv('OpenAI_API'), temperature=1.0)
embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=os.getenv('OpenAI_API'))
index = "sciolyastronomy"
vectorstore = PineconeVectorStore(index_name=index, embedding=embeddings, pinecone_api_key=os.getenv('PINECONE_API_KEY'))

def text_to_db(url):
    driver.get(url)
    page_text = driver.find_element(by=By.XPATH, value="/html/body").text
    start_idx = page_text.index("From Wikipedia, the free encyclopedia") + 37
    end_idx = page_text.index("References[edit]")
    page_text = page_text[start_idx:end_idx]
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_text = text_splitter.split_text(page_text)
    docs = []
    for item in split_text:
        doc = Document(page_content=item, metadata={"source": "local"}, id=str(uuid.uuid4()))
        docs.append(doc)
    vectorstore.add_documents(documents=docs)

def generate_question(subtopic):
    docsearch = vectorstore.from_existing_index(index_name=index, embedding=embeddings)
    class generateTest(BaseModel):
        question: str = Field(description='''Generate a multiple-choice question for the General Knowledge section 
                                of Astronomy. ''')
        answer: str = Field(description='''Generate the corresponding answer to the multiple-choice question for
                            the General Knowledge section of Astrononmy.''')
  
    rag_parser = PydanticOutputParser(pydantic_object=generateTest)

    rag_prompt = PromptTemplate(
        template = '''Based on the dataset of Astronomy General Knowledge multiple choice questions,
        generate a multiple-choice question of the General Knowledge section of Astronomy. 
        Generate the corresponding answer to the multiple-choice question.'''
        '''The output should be formatted a string for the question and a string for the
        answer based on {format_instructions}'''
        '''Dataset: \n{context}\n''',
        partial_variables = {"format_instructions": rag_parser.get_format_instructions()}
    )

    retriever = docsearch.as_retriever(search_time="mmr", search_kwargs={"k": 10})
    qa_chain = create_stuff_documents_chain(llm=llm, prompt=rag_prompt)
    chain = create_retrieval_chain(retriever, qa_chain)
    response = chain.invoke({'input': f'''Generate a General Knowledge astronomy multiple choice question
                            in the topic of {subtopic}.'''})
    return response

subtopic = topics_list[random.randint(0, len(topics_list))]
response = generate_question(subtopic)
print(response)
