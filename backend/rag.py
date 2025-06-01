import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv
from langchain.output_parsers import PydanticOutputParser
from pypdf import PdfReader
import re

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

#Function to combine question & answer into one object and make a list of those dict objects
def generate_test_dict(question_url, answer_url):

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

  question_bank = []
  for x in range(len(response['text'].questions)):
    question_object = {
        'question': response['text'].questions[x],
        'answer': response['text'].answers[x]
    }
    question_bank.append(question_object)

  return question_bank

astro_path = "C:\\Users\\harsh\\scioly_backend\\SciOly Past Tests\\Astronomy"
astro_folders = list(os.scandir(astro_path))
astro_keys = list(os.scandir(astro_folders[0].path))
astro_tests = list(os.scandir(astro_folders[1].path))

question_pdf = str(astro_tests[0].path)
answer_pdf = str(astro_keys[0].path)
question_bank = generate_test_dict(question_pdf, answer_pdf)
print(question_bank)
