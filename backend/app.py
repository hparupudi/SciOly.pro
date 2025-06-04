from flask import Flask, session, request, jsonify
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import os
import secrets
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
import ast 
import random
from datetime import timedelta
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from typing import List, Any
from langchain.output_parsers import PydanticOutputParser
from langchain.docstore.document import Document
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain.chains import create_retrieval_chain, SequentialChain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re
import uuid
from pinecone import Pinecone, ServerlessSpec

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.permanent_session_lifetime = timedelta(days=1)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": ["http://localhost:3000/", "https://sciolypro.web.app/"]}})

load_dotenv()

topics_list = {
    'astronomy': ["stellar classification", "spectral features and chemical composition", "luminosity",
"blackbody radiation", "color index and H-R diagram transitions", "H I/II regions", "molecular clouds", 
"protostars", "Herbig-Haro Objects", "T Tauri variables", "Herbig Ae/Be stars", "planet formation", "brown dwarfs", 
"protoplanetary disks", "debris disks", "exoplanets"]
}

def encode_cipher(plaintext, plaintext_alphabet, cipher_alphabet):
  frequency = [0] * 26
  alphabet = plaintext_alphabet
  index_alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
  ciphertext = ""
  for x in range(len(plaintext)):
    if (plaintext[x].upper() in alphabet):
      cipherletter = cipher_alphabet[alphabet.index(plaintext[x])]
      ciphertext += cipherletter
      frequency[index_alphabet.index(cipherletter)]+=1
    else:
      ciphertext += plaintext[x]
  return plaintext, plaintext_alphabet, ciphertext, cipher_alphabet, frequency

def encode_k1(plaintext, keyword):
  keyword_idx = random.randint(10, 25)
  plaintext_alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
  new_plaintext = [''] * 26
  ciphertext_alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
  for x in range(0, 26):
    new_plaintext[(x + keyword_idx) % 26] = plaintext_alphabet[x]
  plaintext_alphabet = new_plaintext
  keyword_idx = random.randint(0, 25)
  counter = 0

  while (len(keyword) > 0):
    plaintext_alphabet.remove(keyword[0:1])
    plaintext_alphabet.insert(keyword_idx, keyword[0:1])
    keyword = keyword.replace(keyword[0:1], "")
    keyword_idx+=1
    keyword_idx%=26
    counter+=1

  ciphertext = encode_cipher(plaintext.upper(), plaintext_alphabet, ciphertext_alphabet)
  return ciphertext

def encode_k2(plaintext, keyword):
  keyword_idx = random.randint(0, 25)
  plaintext_alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
  alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
  ciphertext_alphabet = [''] * 26
  for i in range(0, 26):
    if len(keyword) > 0:
      ciphertext_alphabet[keyword_idx] = keyword[0:1].upper()
      alphabet.remove(keyword[0:1].upper())
      keyword = keyword.replace(keyword[0:1], "")
    else:
      random_letter = alphabet[0]
      alphabet.remove(random_letter)
      ciphertext_alphabet[keyword_idx] = random_letter
    keyword_idx+=1
    keyword_idx%=26
  ciphertext = encode_cipher(plaintext.upper(), plaintext_alphabet, ciphertext_alphabet)
  return ciphertext

@app.route('/aristo', methods=["POST"])
@cross_origin(suports_credentials=True)
def generate_aristo():
  llm = ChatOpenAI(model="gpt-4.1", api_key=os.getenv("OPENAI_API"), temperature=1.5)
  aristo_type = request.form.get('type')
  difficulty = request.form.get('difficulty')
  if difficulty == "Easy":
    min_len = 1
    max_len = 3
  elif difficulty == "Medium":
    min_len = 3
    max_len = 5
  else:
    min_len = 5
    max_len = 7

  class Plaintext(BaseModel):
    """Generates a plaintext quote and a keyword for encryption."""
    quote: str = Field(description=f'''Generate a quote by a famous individual or a unique quote 
                       between {min_len} to {max_len} sentences long.''')
    keyword: str = Field(description="Generate a unique keyword, related to the quote, " \
    "between 5 and 7 characters long.")

  llm = llm.bind_tools([Plaintext])
  response = llm.invoke("Generate a quote and keyword.").additional_kwargs['tool_calls'][0]['function']['arguments']
  quote = ast.literal_eval(response)['quote']
  keyword = ast.literal_eval(response)['keyword']

  if aristo_type == "K1":
    plaintext, plain_alphabet, ciphertext, cipheralphabet, frequency = encode_k1(quote.upper(), keyword.upper())

  else:
    plaintext, plain_alphabet, ciphertext, cipheralphabet, frequency = encode_k2(quote.upper(), keyword.upper())

  return jsonify({"plaintext": plaintext, "ciphertext": ciphertext, "plain_alphabet": plain_alphabet, 
                  "cipher_alphabet": cipheralphabet, "frequency": frequency}), 200

@app.route('/mcq', methods=['GET', 'POST'])
@cross_origin(suports_credentials=True)
def generate_mcq():
  event = str(request.form.get('event'))
  index = "scioly" + event
  topic_list = topics_list[event]
  subtopic = topic_list[random.randint(0, len(topics_list))]

  llm = ChatOpenAI(model="o4-mini", api_key=os.getenv('OpenAI_API'), temperature=1.0)
  embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=os.getenv('OpenAI_API'))
  vectorstore = PineconeVectorStore(index_name="sciolyastronomy", embedding=embeddings, pinecone_api_key=os.getenv('PINECONE_API_KEY'))
  docsearch = vectorstore.from_existing_index(index_name=index, embedding=embeddings)

  class generateTest(BaseModel):
    question: str = Field(description='''Generate a multiple-choice question for the General Knowledge section 
                    of Astronomy. ''')
    options: List[str] = Field(description='''Generate a list of the four answer options to the General Knowledge
                               Astronomy multiple-choice question. Do not include the letters 
                               'a, b, c, d' as part of the answer options.''')
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
  
  return jsonify({"response": str(response['answer'])}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)

