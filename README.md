# RAG
A Gentle Introduction to RAG

<h2>Installation</h2>

```sh
pip install -r requirements.txt
```


<h2>Obtaining Secrets</h2>

It is not necessary to have a key from semantic scholar, but it is recommended.  You can obtain a key from <a href="https://www.semanticscholar.org/product/api#api-key">here</a>.
<p>
  However, VecML keys are required.  You can obtain a key from <a href="www.vecml.com">here</a>.  Click on login -> API Key.
</p>

<p>Create a file in $HOME/.secrets.json containing this:</p>


```sh
{"s2_apikeys" : [ ** insert zero or more semantic scholar api keys here ** ], 
"vecml_apikeys" : [ ** insert one or more vecml api keys here ** ] }
```

To start the web server

```sh
cd ** directory containing this README.md file **
python3 -m http.server --cgi
```

Then you should be able run these examples on the local host.

<h2>Examples</h2>

<ol>
  <li>Test server.  You should see "hello world" if the server is running when you click <a href="http://0.0.0.0:8000/cgi-bin/hello.py">here</a>.</li>
  <li>Click <a href="http://0.0.0.0:8000/cgi-bin/compare_and_contrast?ids=ACL:P89-1010,ACL:P98-2127">here</a></li> and wait about 10 seconds.  Then you will see a json object that compares and contrasts two ACL papers.</li>
  <li><a href="http://0.0.0.0:8000/cgi-bin/compare_and_contrast_texts?text1=I love you.&text2=I hate you.">example</a></li>
</ol>


<h2>Paper Ids</h2>

The id argument for the above can be any of the following:

<ol>
  <li>sha (40 byte hex); <a href="http://34.204.188.58//cgi-bin/lookup_paper?id=ea7886975510353c194303931b333af983a63ed7&fields=title,authors,citationCount,externalIds">example</a></li>
  <li>CorpusId (the primary key in Semantic Scholar); <a href="http://34.204.188.58//cgi-bin/lookup_paper?id=CorpusId:10491450&fields=title,authors,citationCount,externalIds">example</a></li>
  <li>PMID (pubmed ids); <a href="http://34.204.188.58//cgi-bin/lookup_paper?id=PMID:24335157&fields=title,authors,citationCount,externalIds">example</a></li>
  <li>ACL (<a href="https://aclanthology.org/">acl anthology</a> ids); <a href="http://34.204.188.58//cgi-bin/lookup_paper?id=ACL:2022.lrec-1.676&fields=title,authors,citationCount,externalIds">example</a></li>
  <li><a href="https://arxiv.org/">arXiv</a>; <a href="http://34.204.188.58//cgi-bin/lookup_paper?id=arXiv:2111.03628&fields=title,authors,citationCount,externalIds">example</a></li>
  <li>MAG (<a href="https://www.microsoft.com/en-us/research/project/microsoft-academic-graph/">Microsoft Academic Graph</a>); <a href="http://34.204.188.58//cgi-bin/lookup_paper?id=MAG:3167354871&fields=title,authors,citationCount,externalIds">example</a></li>
</ol>

More documentation on APIs can be found <a href="http://34.204.188.58//similar_documentation.html">here</a>
    
