# Q1 __

Question:
What is tokenization? Illustrate your answer with an example — how would the sentence "I'm learning NLP in 2025!" be tokenized?

Answer:
Tokenization refers to splitting text into tokens that are words or subwords that can be processed by the machine learning model. Tokenization is the first step in NLP since raw text cannot be processed by the machine learning model but tokens can.

Example:
The sentence "I'm learning NLP in 2025!" will be tokenized as follows:
["I", "'m", "learning", "NLP", "in", "2025", "!"]
---

# Q2 __

Question:
What is the difference between stemming and lemmatization? Apply both to the words "running" and "better" and explain which preserves more linguistic meaning.

Answer:
By using a set of rules, stemming removes suffixes from words - but lemmatization uses a dictionary to find the root form of a word. Because of this reliance on a dictionary, more information remains intact when a person uses lemmatization. 

For "running": stemming results in "run" and lemmatization results in "run".
And for "better": stemming results in "bet", while lemmatization results in "good".
---

# Q3 __

Question:
What is the meaning of the abbreviation TF-IDF? For what reason does "the" receive a low numerical weight in the TF-IDF calculation while "photosynthesis" receives a high weight? In your response consider the qualities that enable a word to distinguish one specific document from a collection of documents.

Answer:
TF-IDF is the result when a person multiplies the Term Frequency by the Inverse Document Frequency. As "The" exists in a large portion of the data set, it has a low IDF value - but because "photosynthesis" occurs in only a small number of instances, it has a high IDF value. When terms occur rarely across a collection, they are more effective for the identification of specific texts.

---

# Q4

Question:
What is a sentence embedding? How is it fundamentally different from one-hot encoding? Give one advantage embeddings have that one-hot vectors don't. Think about: what can you measure between two embeddings that you can't measure between two one-hot vectors?

Answer:
Embeddings are dense vectors capturing meaning. One-hot is sparse binary (1 and 0s only). Embeddings let you measure cosine similarity; one-hot vectors always have 0 similarity.

Example:
"cat sleeping" and "dog resting": embeddings cosine ≈ 0.85; one-hot cosine = 0
---

# Q5

Question:
Explain cosine similarity in plain language. If two document vectors point in almost the same direction, what does that tell us about the documents they represent?

Answer:
Cosine similarity measures the angle between vectors. Same direction = close to 1 = semantically similar. Euclidean distance is poor because it's affected by vector length, not just direction.

---

# Q6 __

Question:
Why can't a regular SQL query like WHERE description LIKE '%pizza%' find semantically similar documents? What does a vector index solve that SQL can't?

Answer:
A SQL LIKE command searches for exact string of characters but not semantics. Vector indexing refers to the embedding of a process through which a semantic similarity between documents is established even if they do not have identical words.

Example:
search using SQL LIKE '%car%' would not result in the identification of any document having words like "automobile" or "vehicle".

---

# Q7 __

Question:
What problem does RAG solve that a plain LLM (without RAG) cannot? Give a concrete example of when you would choose RAG over just prompting the LLM directly.

Answer:
RAG allows an artificial intelligence system to examine specific user files, like PDFs or private documents. If RAG is absent, the system is unable to access those external files and it therefore provides an invented response or states "I don’t know"

Example - When a user asks about a document that contains a new company policy, RAG is able to process the text to provide an accurate answer - but a standard artificial intelligence system is only able to guess because it lacks access to the data.
---

# Q8

Question:
Describe the 3 main steps of a RAG pipeline in the correct order. Be clear about what happens at ingestion time (when you load documents) vs query time (when a user asks a question).

Answer:
Ingestion: chunk documents → create embeddings → store in vector DB. Query: embed user question → retrieve similar docs → send to LLM for answer.

---

# Q9 __

Question:
What is the difference between a Docker image and a Docker container? Use an analogy to explain. Common analogies: class vs instance, recipe vs cake, blueprint vs building. Any analogy that works is fine.

Answer
An image is equivalent to a blueprint, a class or a recipe - A container is a running instance, a constructed house or a finished cake. As a template the image exists in a fixed state. To have a running copy, you must have a container.

Example
By comparing them, an image is like a recipe card that does not change. Then again a container is the cake that exists because you followed the recipe. If you have one recipe, you are able to create many cakes.
---

# Q10 __

Question:
What is the difference between a simple LLM chatbot and an AI agent with tools? Give one concrete example of a "tool" and explain why it makes the agent more capable. Think about: what can an agent do that a plain LLM cannot? (e.g., look things up in real-time, run code, query a database, send an email...)

Answer
The chatbot creates text - the agent triggers functions which are tools to carry out commands. With those tools the agent connects with databases or different systems - using an API.

As an example
Chatbot: "The weather tomorrow will be fine" Agent with a weather_tool: "Actually checking API.." "Tomorrow will be sunny with temperature 72°F"
---

# Q11 __

Question:
What is MCP (Model Context Protocol)? What problem does it solve for AI coding assistants like GitHub Copilot? Name two examples of things an MCP server might expose to an AI assistant. Think about: how does a language model normally know about your database, your files, or your GitHub issues? What does MCP standardize?

Answer:
MCP is a standard for connecting AI assistants to external data sources and tools. Solves: LLMs don't know about your private data. MCP allows standardized access to files, databases, GitHub, APIs.

Example:
MCP servers expose: (1) filesystem access (read your project files), (2) GitHub API (check issues, PRs).

---

# Q12 __

Question:
What are Agent Skills in the context of AI coding assistants? How are they different from just writing instructions in a plain prompt? Show a minimal example of what a skill's `.md` metadata block might look like. Think about: a skill has a name, a description, and a path to a detailed instructions file — it lets the AI decide when to activate domain-specific knowledge automatically.

Answer:
Skills are reusable domain knowledge packages with metadata. AI auto-activates them when relevant (vs. static prompts that always run). Skills have name, description, file path.

Example:
```xml
<skill>
  <name>mongodb-optimizer</name>
  <description>Help optimize MongoDB queries. Activate when user asks "optimize query"</description>
  <file>path/to/skills/mongodb/SKILL.md</file>
</skill>
```
