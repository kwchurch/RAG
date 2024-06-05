#!/usr/bin/env python3

import logging,sys,os,getpass,openai
from pypdf import PdfReader

from llama_index.core import VectorStoreIndex
from llama_index.core.schema import TextNode

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

assert "OPENAI_API_KEY" in os.environ, "The environment variable, OPENAI_API_KEY, must be assigned to a valid api key for OpenAI"
openai.api_key = os.environ["OPENAI_API_KEY"]

def split_large_chunks(chunks):
    res = []
    for chunk in chunks:
        if len(chunk) >= 2000:
            cs = chunk.split(". ")
            for c in cs:
                snippet = (c.replace("\n", " ")).replace("  ", " ")
                if len(snippet) >= 20:
                    res.append(snippet)
        else:
            snippet = (chunk.replace("\n", " ")).replace("  ", " ")
            if len(snippet) >= 20:
                res.append(snippet)
    return res


def read_pdf_files(files):
    all_nodes = []
    for file in files:
        txt = []
        for p,page in enumerate(PdfReader(file).pages):
            try:
                text = page.extract_text()
                txt.append(text)
            except:
                print("Error reading page " + str(p + 1) + " in file " + file, file=sys.stderr)

        # Chunk text in pages and create nodes to index
        chunks = (' '.join(txt)).split(". \n")
        for node_number,chunk in enumerate(split_large_chunks(chunks)):
            node = TextNode(text=chunk, id_=file + "_" + str(node_number))
            all_nodes.append(node)
        print("Done with  [" + file + "]", file=sys.stderr)
    return VectorStoreIndex(all_nodes)

index = read_pdf_files(sys.argv[1:])
query_engine = index.as_query_engine(response_mode="tree_summarize", verbose=True)

for prompt in sys.stdin:
    response = query_engine.query(prompt)
    print(response)
