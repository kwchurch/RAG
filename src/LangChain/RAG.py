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
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.document_loaders import DirectoryLoader,JSONLoader,TextLoader,CSVLoader,PDFMinerLoader,WebBaseLoader

# 1. Load, chunk and index the contents of the blog to create a retriever.

loader = PDFMinerLoader(sys.argv[1])

# if sys.argv[1].startswith('http'):
#     loader = WebBaseLoader(
#         web_paths=sys.argv[1:],
#         bs_kwargs=dict(
#             parse_only=bs4.SoupStrainer(
#                 class_=("post-content", "post-title", "post-header")
#             )
#         ),
#     )
# else:
#     loader = DirectoryLoader(sys.argv[1],
#                              { ".json": JSONLoader,
#                                ".txt": TextLoader,
#                                ".csv": CSVLoader,
#                                ".pdf": PDFMinerLoader,
#                               })

docs = loader.load()

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

for line in sys.stdin:
    response = rag_chain.invoke({"input": line})
    print(response["answer"])
