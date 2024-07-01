# A Gentle Introduction to RAG<br> (<b>Windows version, under development</b>)

<h2>Table of Contents</h2>

<ol>
<li><a href="#Getting_Started">Getting Started</a></li>
<li><a href="#chat">Chat</a></li>
<li><a href="#RAG">RAG</a> (uploading files just in time)</li>
<!-- <li><a href="#API">API</a> (Creating an web server on your local host)</li> -->
</ol>

<h2 id="PyPrelims">Preliminaries, Python, etc.</h2>

This document is help Windows users try out these RAG ideas on their Windows machines. Now there are a large number of Windows versions, and shells like Anaconda on top. We'll try to keep the installation discussion general. If you run into issues, you may have to explore a bit.

First of all, Windows machines do not hav Python pre-insalled. You will have to install a suitable version for your Windows environment, perhaps one of the versions listed <a href="https://www.python.org/downloads/windows/">here</a>.

<h2 id="Getting_Started">Installation of Packages</h2>

```sh
pip install -r requirements.txt
```

<h2 id="secrets">Obtaining Secrets</h2>

Some of the features below require secret keys from different organizations.

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
    <td><a href="https://www.semanticscholar.org/product/api#api-key">here</a>; click on Request Authentication</td>
  </tr>

  <tr>
    <td>LangChain</td>
    <td>LANGCHAIN_API_KEY</td>
    <td align="center">&check;</td>
    <td><a href="https://www.langchain.com/">here</a>; click on sign up, and then on settings, and then click on API keys and then create API key (far right)</td>
   </tr>

  <tr>
    <td>VecML</td>
    <td>VECML_API_KEY</td>
    <td align="center">&check;</td>
    <td><a href="https://www.vecml.com">here</a>; click on login, and then click on API Key.
  </tr>
</table>

It is not necessary to obtain keys, but it is recommended that you
obtain (at least) the free keys, and set the environment variables
appropriately.

One way to set the environment variables to store all the keys in a .BAT file, and 'invoke' it before you try out any of these RAG code snippets. For example, you can create a filenamed, say, `apikeys.bat` with your API keys, one per line, like:

    set OPENAI_API_KEY=.......
    set LANGCHAIN_API_KEY=...

Save this file, and invoke it from a Command Prompt/Windows Terminal thus:

    apikeys.bat

That will make all the keys in the file available as environment varibles.

<h2 id="chat">Simple Chat Usage</h2>

<h3>OpenAI</h3>


<!-- If you have an OpenAI key and set it to the environment variable OPENAI_API_KEY,
then you can run this in a shell window.  It will return an error if the key is not valid. [Note that the caret signs (`^`) ??? indicate continuations of the command on the next line. They will be removed before command execution.]

????????? Not working yet

```sh
 curl -H "Content-Type: application/json" -H "Authorization: Bearer %OPENAI_API_KEY%" -d '{ "model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "Say this is a test!"}], "temperature": 0.7 }' https://api.openai.com/v1/chat/completions 
``` -->

If you have an OpenAI key and set it to the environment variable OPENAI_API_KEY,
then you can run this simple example of a chat with OpenAI.  This example refers
to two files in this repository under src/OpenAI: <a href="src/OpenAI/chat.py">chat.py</a> and
<a href="src/OpenAI/sample_chats/sample_chat1.txt">sample_chats/sample_chat1.txt</a>.


```sh
python src/OpenAI/chat.py < src/OpenAI/sample_chats/sample_chat1.txt
```

When we ran the example above, we received the following output:
<br>
<i>The World Series in 2020 was played at Globe Life Field in Arlington, Texas.</i>

Here are some more examples.  The inputs are:
<a href="src/OpenAI/sample_chats/">sample_chats/*.txt</a>.

```sh
cd src/OpenAI
for /R "sample_chats" %F in (*.txt) do more %F & python chat.py < %F

```
See the paper for further discussion of these examples.

<h4 id="RAG">RAG</h4>

RAG allows one to upload files and ask questions about them:

```sh
echo 'Who won the world series in 2021?' | python src\OpenAI\RAG.py "sample_files\World_Series\List of World Series champions - Wikipedia.pdf"
```

The example above outputs (ignoring the warnings and info messages) the response: <i>The Atlanta Braves won the World Series in 2021.</i>

There are a number of versions of <b>RAG.py</b> and <b>chat.py</b> that use different methods to do more or less the same thing.
For example:

```sh
dir/s chat.py RAG.py
```

The difference between <b>RAG.py</b> and <b>chat.py</b> is that <b>RAG.py</b> uploads files from the command line, and <b>chat.py</b> does not upload files.

This example is similar to the one above except that it uses VecML instead of OpenAI.

```sh
echo 'Who won the world series in 2023?' | python src\VecML\RAG.py "sample_files\World_Series\List of World Series champions - Wikipedia.pdf"
```
We get the correct response <i>The Texas Rangers won the World Series in 2023.</i>

The following example shows how to summarize academic papers.  Since there
are two papers in this directory, the prompt asks to summarize one of them (and not the other):


```sh
echo 'Please summarize the paper on psycholinguistics.' | python src/OpenAI/RAG.py sample_files\papers\C98-2122.pdf sample_files\papers\J90-1003.pdf
```

The example above outputs the response:

<i>The paper on psycholinguistics discusses the concept of word association norms and extends it towards the information theoretic definition of mutual information. It also delves into a statistical calculation that can be applied effectively. Additionally, the paper highlights the complexities of lexicography, particularly in distinguishing between different uses of words like "time" in various contexts.</i>

There are three versions of RAG.py in this github, illustrating three
slightly differently solutions.

<h3>VecML</h3>

If you have a key from VecML and set it to the environment variable VECML_API_KEY,
you can do this:

```sh
echo 'Please summarize the paper on psycholinguistics.' > tempfile.txt
echo 'Please summarize the paper on clustering.' >> tempfile.txt
echo 'What are the similarities between these two papers?' >> tempfile.txt
echo 'What are the differences?' >> tempfile.txt
python src/VecML/RAG.py sample_files\papers\C98-2122.pdf sample_files\papers\J90-1003.pdf < tempfile.txt

```
<p>The code above produces the following outputs (one output for each of the four input prompts):</p>

<i><ol>
<li>The paper on psycholinguistics discusses the importance of word association norms in psycholinguistic research, particularly in the area of lexical retrieval. It mentions that subjects respond quicker to words that are highly associated with each other. While noun-noun word associations like "doctor/nurse" are extensively studied, less attention is given to associations among verbs, function words, adjectives, and other non-nouns. The paper concludes by linking the psycholinguistic notion of word association norms to the information-theoretic concept of mutual information, providing a more precise understanding of word associations.</li>
<li>The paper discusses a triangulation approach for clustering concordance lines into word senses based on usage rather than intuitive meanings. It highlights the superficiality of defining a word measure for clustering words without explicit preprocessing tools such as Church's parts program or Hindle's parser. The paper briefly mentions future work on clustering similar words and reviews related work while summarizing its contributions.</li>
<li>The similarities between the two papers include a focus on analyzing language data, using distributional patterns of words, evaluating similarity measures for creating a thesaurus, and discussing the importance of smoothing methods in language processing tasks.</li>
<li>The differences between the two thesaurus entries can be measured based on the cosine coefficient of their feature vectors. In this case, the differences are represented in the relationships between the words listed in each entry. For example, in the given entries, "brief (noun)" is associated with words like "differ," "scream," "compete," and "add," while "inform" and "notify" are related to each other in the second entry. These associations indicate the semantic relationships and differences between the words in each entry.</li>
</ol></i>

<!-- Strangely, VecML seems to be working and is fast, but does not give similarities !!
Instead, this is what I get:

    python src/VecML/RAG.py sample_files\papers\C98-2122.pdf sample_files\papers\J90-1003.pdf < tempfile.txt
Connecting to the VecML server...
The paper on psycholinguistics discusses research on word association norms, particularly focusing on a study by Palermo and Jenkins (1964) that measured word associations based on responses from subjects. The study involved 200 words and participants were asked to write down a word associated with each of the 200 words. The results were analyzed and presented in tabular form, showing which words were most commonly associated with each target word. The paper also proposes an alternative measure called the association ratio, based on mutual information, as a more objective and cost-effective way to measure word associations compared to the subjective method used in the Palermo and Jenkins study.
The paper discusses a similarity measure based on the amount of information shared between objects, as proposed by Lin in 1997. It utilizes a broad-coverage parser to extract dependency triples from a text corpus. The paper mentions evaluating constructed thesauri by computing similarity with manually created thesauri, as well as future work on clustering similar words. Additionally, it reviews related work and summarizes contributions at the end.
I'm sorry, but I can't provide specific similarities between the two papers mentioned.
The mentioned text discusses the differences between Hindle and Hindler in the context of their use of different types of dependencies, such as subject and object relationships. It also mentions that the performance of sim, Hindler, and cosine is quite close. To determine whether the differences are statistically significant, computations were done on their similarities to WordNet and Roget thesaurus for each individual entry, as shown in Table 2. The text refers to the average and standard deviation of the average difference to analyze these distinctions.
7.474891662597656 seconds -->


<h4>RAG is not magic</h4>

The output above conflates the two papers in places.  It is also not clear that it "understands" the difference between similarities and differences. It is tempting to attribute these issues to a lack of "understanding," but actually, many of the issues involve OCR challenges
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

echo 'Please summarize the paper on word associations.' | python  src\VecML\RAG.py sample_files\papers\J90-1003.pdf

echo 'Please summarize the paper on clustering.' | python src\VecML\RAG.py sample_files\papers\C98-2122.pdf

echo 'Please summarize the paper on RAG.' | python src\VecML\RAG.py papers\NeurIPS-2020-retrieval-augmented-generation-for-knowledge-intensive-nlp-tasks-Paper.pdf

```

We get the following responses, for the commands above:

```
echo 'Please summarize the paper on word associations.' | python  src\VecML\RAG.py sample_files\papers\J90-1003.pdf
Connecting to the VecML server...
The paper discusses the concept of word associations in linguistics and psycholinguistics, focusing on how words are related to each other based on their co-occurrence and meanings. It introduces a new objective measure called the association ratio, based on mutual information, to estimate word association norms from computer-readable corpora. This measure is considered more reliable and cost-effective compared to traditional subjective methods. The paper highlights the importance of word associations in understanding linguistic phenomena and provides examples of highly associated words based on the proposed measure.
2.332857608795166 seconds

echo 'Please summarize the paper on clustering.' | python src\VecML\RAG.py sample_files\papers\C98-2122.pdf
Connecting to the VecML server...
The paper discusses a similarity measure based on Lin's proposal in 1997, where similarity between objects is defined by common information divided by information in object descriptions. Dependency triples are extracted using a parser from a text corpus to compute similarity. The paper mentions future work in clustering similar words and evaluates constructed thesauri by comparing them to manually created thesauri. It reviews related work and contributions in the field of distributional clustering of English words and linguistically based term associations by various researchers.
2.2619476318359375 seconds

echo 'Please summarize the paper on RAG.' | python src\VecML\RAG.py papers\NeurIPS-2020-retrieval-augmented-generation-for-knowledge-intensive-nlp-tasks-Paper.pdf
Connecting to the VecML server...
The paper on RAG (Retrieval-Augmented Generation) discusses the generation abilities of RAG models, particularly in the context of open-domain question generation for Jeopardy. RAG models aim to generate more specific and factually accurate responses by leveraging retriever models to enhance generation tasks. The authors highlight the challenging nature of generating Jeopardy questions, where the question must be a precise and factual statement that corresponds to a specific answer entity. The paper presents examples of RAG model responses and emphasizes the use of parametric knowledge in generating reasonable responses to questions that cannot be answered solely based on the reference answer. Additionally, the paper acknowledges the assistance of HuggingFace and other contributors, as well as the funding sources for the research.
2.783205986022949 seconds
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
python src/spacy/summarize_with_spacy.py sample_files\papers\J90-1003.pdf sample_files\papers\C98-2122.pdf papers\NeurIPS-2020-retrieval-augmented-generation-for-knowledge-intensive-nlp-tasks-Paper.pdf
```

To get spacy working, you may be prompted to download some data files using a command like:
```sh
    python -m spacy download en_core_web_lg
```

The summarize_with_spacy command above produces the following output.  Note that OCR and equations introduce interesting challenges:

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
echo 'What is the capital of Spain?' | python src/transformers/RAG.py
```


```
??? I had to add `trust_remote_code=True at about line 286 in the load_dataset call in 
...\lib\site-packages\transformers\models\rag\retrieval_rag.py
and
set KMP_DUPLICATE_LIB_OK=TRUE  
to get this to work. ???
```


The following example illustrates the timeliness issue.  In this case, the bot returns a dated answer that was correct
when the bot was trained, but is no longer correct.

```sh
echo 'Who is President of the United States?' | python src/transformers/RAG.py
```

If we upload a csv file with more recent information, then we obtain
the currectly correct answer (as of 2024).

```sh
echo 'Who is President of the United States?' | python src/transformers/RAG.py sample_files/csv_datasets/administration.csv 
```

```sh
    ??? Not really. This does not work on Windows. Why does it work on macos?

echo 'Who is President of the United States?' | python src/transformers/RAG.py sample_files/csv_datasets/administration.csv
sample_files/csv_datasets/administration.csv
Repo card metadata block was not found. Setting CardData to empty.
Traceback (most recent call last):
  File "D:\OneDrive\Documents\Work\EAI\Code\ETrag\src\transformers\RAG.py", line 21, in <module>
    dataset = load_dataset(".", data_files=data_files, delimiter='\t'
  File "C:\ProgramData\Anaconda3\envs\ETrag\lib\site-packages\datasets\load.py", line 2594, in load_dataset
    builder_instance = load_dataset_builder(
  File "C:\ProgramData\Anaconda3\envs\ETrag\lib\site-packages\datasets\load.py", line 2301, in load_dataset_builder
    builder_cls = get_dataset_builder_class(dataset_module, dataset_name=dataset_name)
  File "C:\ProgramData\Anaconda3\envs\ETrag\lib\site-packages\datasets\load.py", line 256, in get_dataset_builder_class
    raise ValueError("dataset_name should be specified but got None")
ValueError: dataset_name should be specified but got None
```

This solution is provided for pedagogical purposes.  The <a href="sample_files/csv_datasets/administration.csv">csv file</a> is a short (toy) example.  Similarly,
<a href="src/transformers/RAG.py">RAG.py</a> was written to be easy to read and easy to run (but is not fast and does not use GPUs).

------------------------------------------
<!-- 
<h2 id="API">Creating Your Own API</h2>

To start your a web server on your local machine, run this on a shell window.

```sh
cd ** directory containing this README.md file **
python -m http.server --cgi
```

Then you should be able run these examples on the local host.

<h2>Examples</h2>

<ol>
  <li><b>Test server</b>:  You should see "hello world" if the server is running when you click <a href="http://localhost:8000/cgi-bin/hello.py">here</a>.</li>
      ??? Had to change 0.0.0.0 to localhost

  <li><b>RAG</b> (on files): Click <a href="http://localhost:8000/cgi-bin/compare_and_contrast?ids=ACL:J90-1003,ACL:C98-2122">here</a> and wait about 10 seconds.  Then you will see a json object that compares and contrasts two ACL papers.

      ??? Changing 0.0.0.0 to localhost invokes the script. But
       Exception occurred during processing of request from ('::1', 50523, 0, 0)
      Traceback (most recent call last):
      File "C:\ProgramData\Anaconda3\envs\ETrag\lib\socketserver.py", line 683, in process_request_thread
        self.finish_request(request, client_address)
      File "C:\ProgramData\Anaconda3\envs\ETrag\lib\http\server.py", line 1304, in finish_request
        self.RequestHandlerClass(request, client_address, self,
      File "C:\ProgramData\Anaconda3\envs\ETrag\lib\http\server.py", line 668, in __init__
        super().__init__(*args, **kwargs)
      File "C:\ProgramData\Anaconda3\envs\ETrag\lib\socketserver.py", line 747, in __init__
        self.handle()
      File "C:\ProgramData\Anaconda3\envs\ETrag\lib\http\server.py", line 433, in handle
        self.handle_one_request()
      File "C:\ProgramData\Anaconda3\envs\ETrag\lib\http\server.py", line 421, in handle_one_request
        method()
      File "C:\ProgramData\Anaconda3\envs\ETrag\lib\http\server.py", line 672, in do_GET
        f = self.send_head()
      File "C:\ProgramData\Anaconda3\envs\ETrag\lib\http\server.py", line 1010, in send_head
        return self.run_cgi()
      File "C:\ProgramData\Anaconda3\envs\ETrag\lib\http\server.py", line 1211, in run_cgi
        p = subprocess.Popen(cmdline,
      File "C:\ProgramData\Anaconda3\envs\ETrag\lib\subprocess.py", line 971, in __init__
        self._execute_child(args, executable, preexec_fn, close_fds,
      File "C:\ProgramData\Anaconda3\envs\ETrag\lib\subprocess.py", line 1456, in _execute_child
        hp, ht, pid, tid = _winapi.CreateProcess(executable, args,
    OSError: [WinError 193] %1 is not a valid Win32 application

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
  <li><b>RAG</b> (on texts): Like above, but takes texts as inputs (as opposed to files): Click <a href="http://localhost:8000/cgi-bin/compare_and_contrast_texts?text1=I love you.&text2=I hate you.">example</a> and wait about 10 seconds</li>
</ol>

  ??? OSError: [WinError 193] %1 is not a valid Win32 application -->


<h3>LangChain</h3>


We provide a further RAG implementation with the LangChain library. Similar to VecML, PDFs are sent to for the retrieval index and then multiple text queries may be chained together, with both the document retrieval and previous chat history adding to the LLM context. 

The following command submits two papers and asks four successive questions about them to a ChatGPT-4 RAG system:
```sh
(echo Please summarize the paper on psycholinguistics.^
& echo Please summarize the paper on clustering.^
& echo What are the similarities between the two papers?^
& echo What are the differences between the two papers?) | python src/LangChain/RAG.py sample_files\papers\J90-1003.pdf sample_files\papers\C98-2122.pdf 
```
