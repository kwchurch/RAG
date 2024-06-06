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

Here is a simple example of a chat with OpenAI.  This example refers
to several files in this repository under src/OpenAI: <a href="src/OpenAI/chat.py">chat.py</a> and
<a href="src/OpenAI/sample_chats/sample_chat1.txt">sample_chats/sample_chat1.txt</a>.


```sh
src/OpenAI/chat.py < src/OpenAI/sample_chats/sample_chat1.txt
```

When we ran the example above, we received the following output:
<br>
<i>The World Series in 2020 was played at Globe Life Field in Arlington, Texas.</i>

Here are some more examples.  The inputs are:
<a href="src/OpenAI/sample_chats/">sample_chats/*.txt</a>.

```sh
cd src/OpenAI
for f in sample_chats/*.txt
do
echo working on $f
cat $f
echo ""
echo Response from OpenAI:
./chat.py < $f
echo ""	    
done
```

See the paper for more discussion of these examples.

<h4>RAG</h4>

RAG allows one to upload files and ask questions about them:

```sh
echo 'Who won the world series in 2023?' | 
src/OpenAI/RAG.py sample_files/World_Series/*pdf
```

The example above outputs the response: <i>The Texas Rangers won the World Series in 2023.</i>

```sh
echo 'Please summarize the paper on psycholinguistics.' | 
src/OpenAI/RAG.py sample_files/papers/*pdf
```

The example above outputs the response:

<i>The paper on psycholinguistics discusses the extension of the
concept of word association norms towards the information theoretic
definition of mutual information. It provides a statistical
calculation applicable to various areas such as language models for
speech recognition and optical character recognition, disambiguation
cues for parsing ambiguous syntactic structures, text retrieval from
large databases, and productivity enhancement for computational
linguists and lexicographers.</i>

There are three versions of RAG.py in this github, illustrating three
slightly differently solutions.

<h3>VecML</h3>


If you have a key from VecML and set it to the environment variable VECML_API_KEY,
you can do this:

```sh
echo 'Please summarize the paper on psycholinguistics.' >/tmp/x
echo 'Please summarize the paper on clustering.' >>/tmp/x
echo 'What are the similarities between the two papers?' >>/tmp/x
echo 'What are the differences?' >>/tmp/x
src/VecML/RAG.py sample_files/papers/*pdf </tmp/x
```

<p>The code above produces the following outputs (one output for each of the four input prompts):</p>
						
<i><ol>
<li>The paper on psycholinguistics discusses the importance of word association norms in psycholinguistic research, particularly in the area of lexical retrieval. It mentions that subjects respond quicker to words that are highly associated with each other. While noun-noun word associations like "doctor/nurse" are extensively studied, less attention is given to associations among verbs, function words, adjectives, and other non-nouns. The paper concludes by linking the psycholinguistic notion of word association norms to the information-theoretic concept of mutual information, providing a more precise understanding of word associations.</li>
<li>The paper discusses a triangulation approach for clustering concordance lines into word senses based on usage rather than intuitive meanings. It highlights the superficiality of defining a word measure for clustering words without explicit preprocessing tools such as Church's parts program or Hindle's parser. The paper briefly mentions future work on clustering similar words and reviews related work while summarizing its contributions.</li>
<li>The similarities between the two papers include a focus on analyzing language data, using distributional patterns of words, evaluating similarity measures for creating a thesaurus, and discussing the importance of smoothing methods in language processing tasks.</li>
<li>The differences between the two thesaurus entries can be measured based on the cosine coefficient of their feature vectors. In this case, the differences are represented in the relationships between the words listed in each entry. For example, in the given entries, "brief (noun)" is associated with words like "differ," "scream," "compete," and "add," while "inform" and "notify" are related to each other in the second entry. These associations indicate the semantic relationships and differences between the words in each entry.</li>
</ol></i>

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
cd src/VecML
echo 'Please summarize the paper on word associations.' | 
./RAG.py sample_files/J90-1003.pdf

echo 'Please summarize the paper on clustering.' |
./RAG.py sample_files/C98-2122.pdf

echo 'Please summarize the paper on RAG.' | 
./RAG.py papers/NeurIPS-2020-retrieval*.pdf
```

In general, abstractive summarization is more ambitious than extractive summarization.
The table below compares the RAG summaries with tldr summaries from Semantic Scholar.
If one clicks on links in the first column, then
one can see the paper in Semantic Scholar with tldr summaries.
Note that tldr summaries are shorter than RAG summaries,
and less likely to suffer from inconsistencies/misinformation.
The <i><b>bold italics</b></i> in the table below calls out misinformation
introduced by RAG.

In addition to misinformation, the discussion of Section 5 in the table
below contributes little new information.
The section in question would be better charcterized as 
<i>conclusions</i> than <i>contributions</i>, but it would be even better
to summarize the content of the conclusions than to state the obvious.  It should come as no
surprise that the paper ends with conclusions.

<table>
  <tr><th>Id: Title</td> <th align="center">OCR</th><th> tldr </th> <th> RAG Summary</th></tr>
  

<tr><td><a href="https://www.semanticscholar.org/paper/b4130e315df099e981342542536edfe36f77a20f">ACL:J90-1003</a>: Word Association Norms, Mutual Information, and Lexicography</td>
<td align="center"> &check; </td>

<td> The proposed measure, the association ratio, estimates word association norms directly from computer readable corpora, making it possible to estimate norms for tens of thousands of words.</td>

<td> The paper discusses the importance of word association norms in psycholinguistic research, particularly in lexical retrieval. It introduces the concept of the association ratio as a measure to estimate word association norms directly from computer-readable corpora. The paper extends the psycholinguistic notion of word association norms towards an information theoretic definition of mutual information, providing statistical calculation that can be applied effectively. The standard method of obtaining word association norms through testing subjects is deemed costly and unreliable compared to the proposed measure utilizing computer data.</td>
</tr>

<tr><td><a href="https://www.semanticscholar.org/paper/11157109b8f3a098c5c3f801ba9acbffd2aa49b1">ACL:C98-2122</a>: Automatic Retrieval and Clustering of Similar Words</td>
<td align="center"> &check; </td> 

<td>A word similarity measure based on the distributional pattern of words allows a thesaurus to be constructed using a parsed corpus and shows that the thesaurus is significantly closer to WordNet than Roget Thesaurus is.</td>

<td>The paper discusses clustering similar words and evaluates clusters based on their ability to recover data items that are removed from the input corpus. It also indirectly evaluates collocations and their associated scores by their use in parse tree distributional clustering of English words. The paper was presented at <i><b>ACL93</b></i> and authored by <i><b>Gerda Ruge</b></i> in <i><b>1992</b></i>. The future work in clustering similar words is briefly mentioned in Section 4, while related work and the contributions of the paper are summarized in Section 5.</td>
</tr>

<tr><td> <a href="https://www.semanticscholar.org/paper/58ed1fbaabe027345f7bb3a6312d41c5aac63e22">ArXiv:2005.11401</a>: Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks</td>
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

</table>

<h2>Summarizing with Spacy</h2>

It may be useful to compare the summaries above with spacy:

```sh
src/summarize_with_spacy.py sample_files/J*pdf sample_files/C*pdf papers/Neur*pdf
```

The command above produces the following output.  Note that OCR and equations create interesting challenges:

<ol>
<li>The 
, proposed measure, the association ratio, estimates 
word association norms directly from computer 
readable corpora, waki,~g it possible to estimate 
norms for tens of thousands of words. 
[Meyer, Schvaneveldt 
and Ruddy (1975), p. 98] 

Much of this psycholinguistic research is based on 
empirical estimates of word association norms such 
as [Palermo and Jenkins (1964)], perhaps the most 
influential study of its kind, though extremely small 
and somewhat dated.</li>

<li>
Unlike sim, simninale and simHinater, they only 
770 
210g P(c) ,~ simwN(wl, w2) = maxc~ eS(w~)Ac2eS(w2) (maxcesuper(c~)nsuper(c2) log P(cl )+log P(c2) ! 
21R(~l)nR(w2)l simRoget(Wl, W2) = IR(wx)l+lR(w2)l 
where S(w) is the set of senses of w in the WordNet, super(c) is the set of (possibly indirect) 
superclasses of concept c in the WordNet, R(w) is the set of words that belong to a same Roget 
category as w. 
Figure 2: Word similarity measures based on WordNet and Roget 
make use of the unique dependency triples and ig- 
Contextual word similarity and estimation from sparse 
data.</li>
<li>
We introduce
RAG models where the parametric memory is a pre-trained seq2seq model and
the non-parametric memory is a dense vector index of Wikipedia, accessed with
a pre-trained neural retriever.
	For language generation tasks,
we ﬁnd that RAG models generate more speciﬁc, diverse and factual language than
a state-of-the-art parametric-only seq2seq baseline.
</li>
</ol>

<h3>Transformers</h3>

We provide yet another solution to RAG based on the transformers package.  This version takes one or more csv files on the command line
and uploads them to the bot before responding to prompts.
For simple questions, it is not necessary to provide a csv file:

```sh
echo 'What is the capital of Spain?' |
src/transformers/RAG.py
```

The following example illustrates the timeliness issue.  In this case, the bot returns a dated answer that was correct
when the bot was trained, but is no longer correct.

```sh
echo 'Who is President of the United States?' | 
src/transformers/RAG.py
```

If we upload a csv file with more recent information, then we obtain
the currectly correct answer (as of 2024).

```sh
echo 'Who is President of the United States?' | 
src/transformers/RAG.py sample_files/csv_datasets/administration.csv 
```

This solution is provided for pedagogical purposes.  The <a href="sample_files/csv_datasets/administration.csv">csv file</a> is a short (toy) example.  Similarly,
<a href="src/transformers/RAG.py">RAG.py</a> was written to be easy to read and easy to run (but is not fast and does not use GPUs).

<h2>Creating Your Own API</h2>

To start your a web server on your local machine, run this on a shell window.

```sh
cd ** directory containing this README.md file **
python3 -m http.server --cgi
```

Then you should be able run these examples on the local host.

<h2>Examples</h2>

<ol>
  <li><b>Test server</b>:  You should see "hello world" if the server is running when you click <a href="http://0.0.0.0:8000/cgi-bin/hello.py">here</a>.</li>
  <li><b>RAG</b> (on files): Click <a href="http://0.0.0.0:8000/cgi-bin/compare_and_contrast?ids=ACL:J90-1003,ACL:C98-2122">here</a> and wait about 10 seconds.  Then you will see a json object that compares and contrasts two ACL papers.
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
  <li><b>RAG</b> (on texts): Like above, but takes texts as inputs (as opposed to files): Click <a href="http://0.0.0.0:8000/cgi-bin/compare_and_contrast_texts?text1=I love you.&text2=I hate you.">example</a> and wait about 10 seconds</li>
</ol>
