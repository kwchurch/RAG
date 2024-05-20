#!/usr/bin/env python3

import os,sys,argparse
from openai import OpenAI

parser = argparse.ArgumentParser()
parser.add_argument("--stream", help="output with streaming", action='store_true')
args = parser.parse_args()

client = OpenAI()

messages = []

for line in sys.stdin:
    fields = line.rstrip().split('|')
    if len(fields) >= 2:
        role,content = fields[0:2]
        messages.append({"role" : role, "content" : content})

response = client.chat.completions.create(
    model="gpt-3.5-turbo", 
    messages=messages,
    stream=args.stream)

if not args.stream:
    d = response.to_dict()
    for choice in d['choices']:
        print(choice['message']['content'])
else:
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")

