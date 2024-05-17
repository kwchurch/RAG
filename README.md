# A Gentle Introduction to RAG

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

It is not necessary to obtain keys, but it is recommended that you
obtain (at least) the free keys, and set the environment variables
appropriately.

<h2>Simple Usage</h2>

<h3>OpenAI</h3>

If you have an OpenAI key and set it to the environment variable OPENAI_API_KEY,
then you can run this in a shell window.  It will return an error if the key is not valid.

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

<h3>VecML</h3>

If you have a key from VecML and set it to the environment variable VECML_API_KEY,
you can do this:

```sh
echo 'Please summarize the paper on psycholinguistics.' >/tmp/x
echo 'Please summarize the paper on clustering.' >>/tmp/x
echo 'What are the similarities between the two papers?' >>/tmp/x
echo 'What are the differences?' >>/tmp/x
src/RAG.py sample_files/*pdf </tmp/x
```

<p>The code above produces the following outputs (one output for each of the four input prompts):</p>
						
<ol>
<li>The paper on psycholinguistics discusses the importance of word association norms in psycholinguistic research, particularly in the area of lexical retrieval. It mentions that subjects respond quicker to words that are highly associated with each other. While noun-noun word associations like "doctor/nurse" are extensively studied, less attention is given to associations among verbs, function words, adjectives, and other non-nouns. The paper concludes by linking the psycholinguistic notion of word association norms to the information-theoretic concept of mutual information, providing a more precise understanding of word associations.</li>
<li>The paper discusses a triangulation approach for clustering concordance lines into word senses based on usage rather than intuitive meanings. It highlights the superficiality of defining a word measure for clustering words without explicit preprocessing tools such as Church's parts program or Hindle's parser. The paper briefly mentions future work on clustering similar words and reviews related work while summarizing its contributions.</li>
<li>The similarities between the two papers include a focus on analyzing language data, using distributional patterns of words, evaluating similarity measures for creating a thesaurus, and discussing the importance of smoothing methods in language processing tasks.</li>
<li>The differences between the two thesaurus entries can be measured based on the cosine coefficient of their feature vectors. In this case, the differences are represented in the relationships between the words listed in each entry. For example, in the given entries, "brief (noun)" is associated with words like "differ," "scream," "compete," and "add," while "inform" and "notify" are related to each other in the second entry. These associations indicate the semantic relationships and differences between the words in each entry.</li>
</ol>

<h4>RAG is not magic</h4>

The output above conflates the two papers in places.  It is also not clear that it "understands" the difference between similarities and differences.

It is tempting to attribute these issues to a lack of "understanding," but actually, many of the issues involve OCR challenges
and unnecessarily complicated inputs.

There are a couple of opportunities to improve the example above:
<ol>
  <li>OCR errors: garbage in &rarr; garbage out</li>
<li>KISS (keep it simple, stupid):
  <ol>
    <li>It is safer to process fewer files at a time, and</li>
    <li>to decompose prompts into smaller subtasks (Chain of Thought Reasoning)</li>
  </ol>
</li>
</ol>

As we will see, older pdf files on the ACL Anthology introduce a number
of OCR errors.  The table below shows three papers, two older papers with OCR issues
as well as a newer paper without OCR issues.

The RAG outputs in the table were created with:

```sh
echo 'Please summarize the paper on word associations.' | 
src/RAG.py sample_files/J90-1003.pdf

echo 'Please summarize the paper on clustering.' |
src/RAG.py sample_files/C98-2122.pdf

echo 'Please summarize the paper on RAG.' | 
src/RAG.py papers/NeurIPS-2020-retrieval*.pdf
```

In general, abstractive summarization is more ambitious than extractive summarization.
The table below compares the RAG summaries with tldr summaries from Semantic Scholar.
If one clicks on links in the first column, then
one can see the paper in Semantic Scholar with tldr summaries.

Note that those summaries are shorter than the RAG summaries,
and less likely to suffer from inconsistencies and misinformation.
The bold face in the table below calls out some misinformation
introduced by RAG.

In addition to misinformation, the discussion of Section 5 in the table
below does not contribute much new information.
Section 5 of the paper in question would be better charcterized as 
<i>conclusions</i> than <i>contributions</i>, but it would be even better
to summarize the conclusions than to say that the paper ends with conclusions.



<table>
  <tr><th>Id</td> <th align="center">OCR</th><th> tldr </th> <th> RAG Summary</th></tr>
  

<tr><td></td>
<td align="center"> &check; </td>

<td> The proposed measure, the association ratio, estimates word association norms directly from computer readable corpora, making it possible to estimate norms for tens of thousands of words.</td>

<td> The paper discusses the importance of word association norms in psycholinguistic research, particularly in lexical retrieval. It introduces the concept of the association ratio as a measure to estimate word association norms directly from computer-readable corpora. The paper extends the psycholinguistic notion of word association norms towards an information theoretic definition of mutual information, providing statistical calculation that can be applied effectively. The standard method of obtaining word association norms through testing subjects is deemed costly and unreliable compared to the proposed measure utilizing computer data.</td>
</tr>

<tr><td><a href="https://www.semanticscholar.org/paper/11157109b8f3a098c5c3f801ba9acbffd2aa49b1">ACL:C98-2122</a></td>
<td align="center"> &check; </td> 

<td>A word similarity measure based on the distributional pattern of words allows a thesaurus to be constructed using a parsed corpus and shows that the thesaurus is significantly closer to WordNet than Roget Thesaurus is.</td>

<td>The paper discusses clustering similar words and evaluates clusters based on their ability to recover data items that are removed from the input corpus. It also indirectly evaluates collocations and their associated scores by their use in parse tree distributional clustering of English words. The paper was presented at <font color="red" style="background-color:yellow"><b>ACL93</b></font> and authored by <b>Gerda Ruge</b> in </b>1992</b>. The future work in clustering similar words is briefly mentioned in Section 4, while related work and the contributions of the paper are summarized in Section 5.</td>
</tr>

<tr><td> <a href="https://www.semanticscholar.org/paper/58ed1fbaabe027345f7bb3a6312d41c5aac63e22">ArXiv:2005.11401</a></td>
 <td align="center"> &#x2717; </td> 

<td>A general-purpose fine-tuning recipe for retrieval-augmented
generation (RAG) -- models which combine pre-trained parametric and
non-parametric memory for language generation, and finds that RAG
models generate more specific, diverse and factual language than a
state-of-the-art parametric-only seq2seq baseline.</td>

<td>The paper on RAG discusses the use of Retrieval-Augmented
Generation (RAG) for question answering (QA). RAG directly minimizes
the negative log-likelihood of answers and is compared to traditional
extractive QA methods and Closed-Book QA approaches. RAG's retriever
is initialized using DPR's retriever, and it achieves results
comparable to the DPR QA system. RAG is able to generate answers
without the need for specialized pre-training like "salient span
masking." Additionally, RAG demonstrates high accuracy in classifying
claims as true or false based on evidence it retrieves, achieving
results within 2.7% of a model that uses gold evidence sentences. In
analyzing RAG's performance, the overlap in article titles between
the documents retrieved by RAG and the gold evidence in FEVER dataset
is calculated.</td>
</tr>


<table>





The summary above can be retrieved with <a href="http://34.204.188.58//cgi-bin/lookup_paper?id=ACL:C98-2122&fields=title,tldr">this</a>.
The Semantic Scholar description of this paper can be found <a href="https://www.semanticscholar.org/paper/Automatic-Retrieval-and-Clustering-of-Similar-Words-Lin/11157109b8f3a098c5c3f801ba9acbffd2aa49b1">here</a>,
and the ACL Anthology description of this paper can be found <a href="https://aclanthology.org/P98-2127/">here</a>.

It may be useful to compare RAG summaries with older technologies such as spacy.


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
