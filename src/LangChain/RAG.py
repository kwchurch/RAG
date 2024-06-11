#!/usr/bin/env python3

# see https://python.langchain.com/v0.2/docs/tutorials/qa_chat_history/

import getpass
import sys,os

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

import bs4
from langchain import hub
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.document_loaders import DirectoryLoader,JSONLoader,TextLoader,CSVLoader,PDFMinerLoader,WebBaseLoader

# 1. Load, chunk and index the files specified in sys.argv[1:] to create a retriever.
docs = []
for pdf_path in sys.argv[1:]:
  try:
    loader = PDFMinerLoader(pdf_path)
    docs.extend(loader.load())
  except Exception as e:
    print(f'Failed to load {pdf_path} with Exception: {e}')

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever()


# 2. Incorporate the retriever into a question-answering chain.
system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

chat_history = [] 
for line in sys.stdin:
    response = rag_chain.invoke({"input": line, "chat_history": chat_history})
    chat_history.extend([HumanMessage(content=line), response["answer"]])
    print(response["answer"])
