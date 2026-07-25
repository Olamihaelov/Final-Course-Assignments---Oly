# Theory Questions

> NLP - NATURAL LANGUAGE PROCESSING  Q1-Q3


### 1 - What is tokenization? Give an example - show how the sentence "I'm learning NLP in 2025!" would be tokenized.

## Answer:

Tokenization breaks text into smaller pieces - words, numbers, punctuation marks.

This is the first NLP step because models can't process raw text as one long string.

For example: "I'm learning NLP in 2025!"

Breaks into: ["I", "'m", "learning", "NLP", "in", "2025", "!"]

----

### 2 - What is the difference between stemming and lemmatization? Apply both to the words "running" and "better" and explain which preserves more linguistic meaning.


## Answer:

Stemming and lemmatization both try to reduce words to a simpler form, but they work differently.
Stemming is the quick and rough way - it just chops off endings.
So "running" becomes "run".

Lemmatization is smarter. It looks at the word and uses a dictionary, so "better" becomes "good" instead of staying as "better".

That's why lemmatization keeps more of the real meaning. In our exercises I preferred lemmatization when accuracy was more important than speed.

----

### 3 - What does TF-IDF stand for? Explain in plain language why the word "the" scores almost zero in TF-IDF, while the word "photosynthesis" would score high.

## Answer:

TF-IDF stands for Term Frequency-Inverse Document Frequency.

The word "the" gets a low score because it appears in almost every document, so it doesn't carry much meaning.

In contrast, "photosynthesis" gets a high score because it is rare and appears mainly in specific science-related documents.

A good word for identifying a document is a word that:
- appears many times in the current document
- appears rarely in other documents

This is what allows TF-IDF to distinguish between documents.

----

> VECTOR DATABASES & EMBEDDINGS  Q4-Q6

### 4 - What is a sentence embedding? How is it fundamentally different from one-hot encoding? Give one advantage embeddings have that one-hot vectors don't.

## Answer:

A sentence embedding is a single vector that represents the meaning of a whole sentence.

One-hot encoding is different — each word gets its own position in the vector, filled with zeros except for one 1. 
So similar words like "happy" and "joyful" have no connection at all.

The advantage of embeddings is that you can measure similarity between sentences using cosine similarity. 
One-hot vectors don't allow that.

----

### 5 - Explain cosine similarity in plain language. If two document vectors point in almost the same direction, what does that tell us about the documents they represent?

## Answer:

Cosine similarity looks at the angle created between two vectors.

When two document vectors point in almost the same direction, it tells us those documents likely share the same topic or general idea.

This works well because cosine focuses on direction, rather than the raw length of the vectors.

----

### 6 - Why can't a regular SQL query `like WHERE description LIKE '%pizza%'` find semantically similar documents? What does a vector index solve that SQL can't?

## Answer:

A SQL query like `WHERE description LIKE '%pizza%'` looks for exact words only.
It doesn’t understand meaning, so it can miss related texts that use different wording.

Vector indexing works differently: it turns text into vectors that represent meaning,
and then compares vectors by semantic similarity.

So basically, SQL matches words, while vector indexing matches meaning.

----

> RAG - RETRIEVAL-AUGMENTED GENERATION  Q7-Q8

### 7 - What problem does RAG solve that a plain LLM (without RAG) cannot? Give a concrete example of when you would choose RAG over just prompting the LLM directly.

## Answer:

RAG helps when a normal LLM is not enough, especially with private or new information.

The idea is simple: first bring the relevant information, then give it to the model, and only after that the model answers.

Because of that, the answer is usually more accurate and there are fewer hallucinations.

----

### 8 - Describe the 3 main steps of a RAG pipeline in the correct order. Be clear about what happens at ingestion time (when you load documents) vs query time (when a user asks a question).

## Answer:_____
At ingestion time, you split the documents into chunks, turn those chunks into embeddings, and store them in a vector database. At query time, you embed the question, find the closest chunks, and let the model answer using those chunks as context.

----

> DOCKER  +  AI AGENTS  Q9-Q10

### 9 - What is the difference between a Docker image and a Docker container? Use an analogy to explain.

## Answer:_____
A Docker image is like a recipe or blueprint. It contains the setup for an app. A container is the live thing you run from that recipe, so it is the actual working instance.

----

### 10 - What is the difference between a simple LLM chatbot and an AI agent with tools? Give one concrete example of a "tool" and explain why it makes the agent more capable.

## Answer:_____
A simple chatbot mostly just writes text. An agent can also use tools, such as a web search or a calculator, to get live information and do real actions. That makes it much more useful than a chatbot that only talks.

----

> MCP & AGENT SKILLS  Q11-Q12

### 11 - What is MCP (Model Context Protocol)? What problem does it solve for AI coding assistants like GitHub Copilot? Name two examples of things an MCP server might expose to an AI assistant.

## Answer:_____
MCP is a standard for giving AI assistants access to outside tools and data. It solves the problem of models not knowing how to connect to files, databases, or GitHub in a consistent way. Two examples are a file server and a database query server.

----

### 12 - What are Agent Skills in the context of AI coding assistants? How are they different from just writing instructions in a plain prompt? Show a minimal example of what a skill's .md metadata block might look like.

## Answer:_____
Agent Skills are reusable pieces of guidance that help an assistant know when to use a certain capability. They are more structured than a plain prompt, so the assistant can choose the right behavior automatically. A simple example looks like this:

```
name: pet-store-assistant
description: Help with pet store inventory, orders, and customer support questions.
file: skills/pet-store-assistant/SKILL.md
```

```
<skill>
	<name>pet-store-assistant</name>
	<description>Help with pet store inventory, orders, and customer support questions.
	Use when the user asks "How do I check stock?"
	or "What is the status of this order?"</description>
	<file>path/to/skills/pet-store-assistant/SKILL.md</file>
</skill>
```
