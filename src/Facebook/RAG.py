#!/usr/bin/env python3


import sys,os
from transformers import RagSequenceForGeneration, RagTokenizer, RagRetriever

retriever = RagRetriever.from_pretrained(
    "facebook/rag-token-nq", index_name="exact", use_dummy_dataset=True
)
model = RagSequenceForGeneration.from_pretrained("facebook/rag-token-nq", retriever=retriever)
tokenizer = RagTokenizer.from_pretrained("facebook/rag-token-nq")

def chat(prompt):
    input_ids = tokenizer.question_encoder(prompt, return_tensors="pt")["input_ids"]
    generated = model.generate(input_ids)
    question_hidden_states = model.question_encoder(input_ids)[0]
    docs_dict = retriever(input_ids.cpu().numpy(), question_hidden_states.cpu().detach().numpy(), return_tensors="pt")
    print(tokenizer.batch_decode(generated, skip_special_tokens=True)[0])
    print(docs_dict)
    # sources = []
    # for doc in docs_dict["doc_ids"][0].tolist():
    #     sources.append(dataset[doc]["title"])
    # print(sources)


for prompt in sys.stdin:
    print(chat(prompt))


