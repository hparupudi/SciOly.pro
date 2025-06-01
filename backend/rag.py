import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from pydantic import BaseModel, Field
from typing import List, Any
from dotenv import load_dotenv
from langchain.output_parsers import PydanticOutputParser
from langchain_text_splitters import RecursiveJsonSplitter
from pypdf import PdfReader
from langchain.docstore.document import Document
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
import re
import json
import uuid

load_dotenv()

#LLM, Prompt & Structured Output setup

class Test(BaseModel):
  questions: List[str] = Field(description='''List of all the questions in General Knowledge section including all the options
  for multiple-choice questions.''')
  answers: List[str] = Field(description='''List of the corresponding answers to the questions in
  the General Knowledge section.''')

parser = PydanticOutputParser(pydantic_object=Test)

prompt = PromptTemplate(
    template = '''Create a list of all the questions including all options for multiple-choice questions
    in the General Knowledge section of {test}. Create a list of the
    answers to these questions using the exact given answers in {answer_key}.'''
    '''The output should be formatted as a list for the questions and a list for the
    answers based on {format_instructions}''',
    input_variables = ["test", "answer_key"],
    partial_variables = {"format_instructions": parser.get_format_instructions()}
)

llm = ChatOpenAI(model="gpt-4o", api_key=os.getenv('OpenAI_API'), temperature=1.0)
embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=os.getenv('OpenAI_API'))

#Function to combine question & answer into one object and make a list of those dict objects
def generate_test_list(question_url, answer_url):

  question_reader = PdfReader(question_url)
  question_text = ""
  for x in range(0, len(question_reader.pages)):
    question_text += question_reader.pages[x].extract_text()
  question_text = re.split(r'\d\. ', question_text)

  answer_reader = PdfReader(answer_url)
  answer_text = ""
  for x in range(0, len(answer_reader.pages)):
    answer_text += answer_reader.pages[x].extract_text()

  chain = LLMChain(llm=llm, prompt=prompt, output_parser=parser)
  response = chain.invoke(
    input={"test": f"{question_text}", "answer_key": f"{answer_text}"}
  )

  question_list = []
  for x in range(len(response['text'].questions)):
    question_str = "Question: " + response['text'].questions[x] + " Answer: " + response['text'].answers[x]
    question_list.append(question_str)

  return question_list

def load_question_bank(question_list, index):
    docs = []
    for q in question_list:
        doc = Document(page_content=q, metadata={"source": "local"}, id=str(uuid.uuid4()))
        docs.append(doc)
    vectorstore = PineconeVectorStore(index_name=index, embedding=embeddings, pinecone_api_key=os.getenv('PINECONE_API'))
    vectorstore.add_documents(documents=docs)

index = "sciolyastronomy"
astro_path = "C:\\Users\\harsh\\scioly_backend\\SciOly Past Tests\\Astronomy"
astro_folders = list(os.scandir(astro_path))
astro_keys = list(os.scandir(astro_folders[0].path))
astro_test_images = list(os.scandir(astro_folders[1].path))

for x in range(len(astro_keys)):
    answer_pdf = str(astro_keys[x].path)
    question_dir = list(os.scandir(astro_test_images[x].path))
    if len(question_dir) > 1:
        question_pdf = question_dir[1].path
    else:
       question_pdf = question_dir[0].path
    question_list = generate_test_list(question_pdf, answer_pdf)
    load_question_bank(question_list, index)

print("Completed!")
