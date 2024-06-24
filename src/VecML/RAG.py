#!/usr/bin/env python3

from vecml import vecml
import sys,os,time

chatName = sys.argv[1]

try:
    vecml.delete_data(chatName)
except:
    "do nothing"

vecml.init(os.environ['VECML_API_KEY'], "us-west")
vecml.create_chat(chatName, sys.argv[1:])

t0 = time.time()
for prompt in sys.stdin:
    print(vecml.chat(chatName, prompt))

vecml.delete_data(chatName)
print(str(time.time() - t0) + ' seconds')

