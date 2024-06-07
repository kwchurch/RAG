#!/usr/bin/env python3

import sys,os
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a world class technical documentation writer."),
    ("user", "{input}")
])
llm = ChatOpenAI()
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

for line in sys.stdin:
    print(chain.invoke(line))
    

