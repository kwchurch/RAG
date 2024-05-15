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
  <li><a href="http://0.0.0.0:8000/cgi-bin/hello.py">hello</a></li>
  <li><a href="http://0.0.0.0:8000/cgi-bin/compare_and_contrast_texts?text1=I love you.&text2=I hate you.">example</a></li>
  <li><a href="http://0.0.0.0:8000/cgi-bin/compare_and_contrast?ids=ACL:P89-1010,ACL:P98-2127">example2</a></li>
</ol>

