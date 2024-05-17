#!/usr/bin/env python3

from vecml import vecml
import sys,os

chatName = sys.argv[1]

vecml.init(os.environ['VECML_API_KEY'], "us-west")
vecml.create_chat(chatName, sys.argv[1:])

for prompt in sys.stdin:
    print(vecml.chat(chatName, prompt))

vecml.delete_data(chatName)

