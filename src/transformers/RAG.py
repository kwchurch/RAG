#!/usr/bin/env python3


import sys,os
from transformers import RagSequenceForGeneration, RagTokenizer, RagRetriever, DPRContextEncoder, DPRContextEncoderTokenizer
import numpy as np

if len(sys.argv[1:]) == 0:
    dataset = None
    retriever = RagRetriever.from_pretrained(
        "facebook/rag-token-nq", index_name="exact", use_dummy_dataset=True)
    model = RagSequenceForGeneration.from_pretrained("facebook/rag-token-nq", retriever=retriever)
    tokenizer = RagTokenizer.from_pretrained("facebook/rag-token-nq")

for d in sys.argv[1:]:
    from datasets import load_dataset
    data_files = {"train": d}
    dataset = load_dataset(".", data_files=data_files, delimiter='\t')
    dataset = dataset["train"]
    ctx_encoder = DPRContextEncoder.from_pretrained("facebook/dpr-ctx_encoder-single-nq-base")
    ctx_tokenizer = DPRContextEncoderTokenizer.from_pretrained("facebook/dpr-ctx_encoder-single-nq-base")
    
    # Get embeddings for all the text in the dataset so we can represent the text
    embeddings_dataset = dataset.map(lambda example: {'embeddings': ctx_encoder(**ctx_tokenizer(example["text"], return_tensors="pt", padding=True, truncation=True))[0][0].detach().numpy()})
    embeddings_dataset.add_faiss_index(column='embeddings', index_name='embeddings')

    # Update the retriever and the model
    retriever = RagRetriever.from_pretrained(
        "facebook/rag-sequence-nq", index_name="embeddings", indexed_dataset=embeddings_dataset
    )
    model = RagSequenceForGeneration.from_pretrained("facebook/rag-sequence-nq", retriever=retriever)
    tokenizer = RagTokenizer.from_pretrained("facebook/rag-token-nq")

def chat(prompt, dataset):
    input_ids = tokenizer.question_encoder(prompt, return_tensors="pt")["input_ids"]
    generated = model.generate(input_ids)
    question_hidden_states = model.question_encoder(input_ids)[0]
    docs_dict = retriever(input_ids.cpu().numpy(), question_hidden_states.cpu().detach().numpy(), return_tensors="pt")
    return tokenizer.batch_decode(generated, skip_special_tokens=True)[0]

for prompt in sys.stdin:
    print(chat(prompt, dataset))
    
    


