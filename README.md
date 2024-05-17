# RAG
A Gentle Introduction to RAG

<h2>Installation</h2>

```sh
pip install -r requirements.txt
```


<h2>Obtaining Secrets</h2>

Some of the features below require secrets from different organizations

<table>
  <tr><th align="left">Company</th><th align="left">Environment Variable</th><th align="left">Free?</th><th align="left">Instructions for Obtaining Key</th></tr>
  <tr>
    <td>OpenAI</td>
    <td>OPENAI_API_KEY</td>
    <td align="center">&#x2717;</td>
    <td><a href="https://platform.openai.com/api-keys">here</a></td>
  </tr>

  <tr>
    <td>Semantic Scholar</td>
    <td>S2_API_KEY</td>
    <td align="center">&check;</td>
    <td><a href="https://www.semanticscholar.org/product/api#api-key">here</a></td>
  </tr>

  <tr>
    <td>VecML</td>
    <td>VECML_API_KEY</td>
    <td align="center">&check;</td>
    <td><a href="www.vecml.com">here</a>; click on login, and then click on API Key.
  </tr>
</table>

<h2>Simple Usage</h2>

It is suggested that you obtain (at least) the free keys, and set the environment variables appropriately.

After you obtain a key from VecML and set it to the environment variable VECML_API_KEY,
you should be able to do this:

```sh
echo 'Please summarize the paper on psycholinguistics.' >/tmp/x
echo 'Please summarize the paper on clustering.' >>/tmp/x
echo 'What are the similarities between the two papers?' >>/tmp/x
echo 'What are the differences?' >>/tmp/x
src/compare_and_contrast.py sample_files/*pdf </tmp/x
```

<p>The code above produces the following output:</p>
						
<ol>
<li>The paper on psycholinguistics discusses the importance of word association norms in psycholinguistic research, particularly in the area of lexical retrieval. It mentions that subjects respond quicker to words that are highly associated with each other. While noun-noun word associations like "doctor/nurse" are extensively studied, less attention is given to associations among verbs, function words, adjectives, and other non-nouns. The paper concludes by linking the psycholinguistic notion of word association norms to the information-theoretic concept of mutual information, providing a more precise understanding of word associations.</li>
<li>The paper discusses a triangulation approach for clustering concordance lines into word senses based on usage rather than intuitive meanings. It highlights the superficiality of defining a word measure for clustering words without explicit preprocessing tools such as Church's parts program or Hindle's parser. The paper briefly mentions future work on clustering similar words and reviews related work while summarizing its contributions.</li>
<li>The similarities between the two papers include a focus on analyzing language data, using distributional patterns of words, evaluating similarity measures for creating a thesaurus, and discussing the importance of smoothing methods in language processing tasks.</li>
<li>The differences between the two thesaurus entries can be measured based on the cosine coefficient of their feature vectors. In this case, the differences are represented in the relationships between the words listed in each entry. For example, in the given entries, "brief (noun)" is associated with words like "differ," "scream," "compete," and "add," while "inform" and "notify" are related to each other in the second entry. These associations indicate the semantic relationships and differences between the words in each entry.</li>
</ol>
						
After you obtain a key from OpenAI and set it to the environment variable OPENAI_API_KEY,
you can run this in a shell window.  It will return an error if the key is not valid.

```sh
 curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
     "model": "gpt-3.5-turbo",
     "messages": [{"role": "user", "content": "Say this is a test!"}],
     "temperature": 0.7
}'
```

<h2>Creating Your Own API</h2>

To start your a web server on your local machine, run this on a shell window.

```sh
cd ** directory containing this README.md file **
python3 -m http.server --cgi
```

Then you should be able run these examples on the local host.

<h2>Examples</h2>

<ol>
  <li>Test server.  You should see "hello world" if the server is running when you click <a href="http://0.0.0.0:8000/cgi-bin/hello.py">here</a>.</li>
  <li>Click <a href="http://0.0.0.0:8000/cgi-bin/compare_and_contrast?ids=ACL:J90-1003,ACL:C98-2122">here</a> and wait about 10 seconds.  Then you will see a json object that compares and contrasts two ACL papers.
    <p>The URL above takes two or more ids as input.  These ids should refer to papers in Semantic Scholar such as:</p>

<ol>
  <li>sha (40 byte hex); <a href="http://34.204.188.58//cgi-bin/lookup_paper?id=ea7886975510353c194303931b333af983a63ed7&fields=title,authors,citationCount,externalIds">example</a></li>
  <li>CorpusId (the primary key in Semantic Scholar); <a href="http://34.204.188.58//cgi-bin/lookup_paper?id=CorpusId:10491450&fields=title,authors,citationCount,externalIds">example</a></li>
  <li>PMID (pubmed ids); <a href="http://34.204.188.58//cgi-bin/lookup_paper?id=PMID:24335157&fields=title,authors,citationCount,externalIds">example</a></li>
  <li>ACL (<a href="https://aclanthology.org/">acl anthology</a> ids); <a href="http://34.204.188.58//cgi-bin/lookup_paper?id=ACL:2022.lrec-1.676&fields=title,authors,citationCount,externalIds">example</a></li>
  <li><a href="https://arxiv.org/">arXiv</a>; <a href="http://34.204.188.58//cgi-bin/lookup_paper?id=arXiv:2111.03628&fields=title,authors,citationCount,externalIds">example</a></li>
  <li>MAG (<a href="https://www.microsoft.com/en-us/research/project/microsoft-academic-graph/">Microsoft Academic Graph</a>); <a href="http://34.204.188.58//cgi-bin/lookup_paper?id=MAG:3167354871&fields=title,authors,citationCount,externalIds">example</a></li>
</ol>

More documentation on APIs can be
found <a href="http://34.204.188.58//similar_documentation.html">here</a>;
you can get ids from a query string with paper_search
(<a href="http://34.204.188.58//cgi-bin/paper_search?query=Word%20Association">example</a>).

</p>
</li>
  <li>Like above, but takes texts as files (as opposed to files): Click <a href="http://0.0.0.0:8000/cgi-bin/compare_and_contrast_texts?text1=I love you.&text2=I hate you.">example</a> and wait about 10 seconds</li>
</ol>
