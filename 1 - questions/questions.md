# Theory Questions

> NLP - NATURAL LANGUAGE PROCESSING  Q1-Q3


## 1

What is tokenization? Give an example - show how the sentence "I'm learning NLP in 2025!" would be tokenized. Expected: a list of tokens and a one-sentence explanation of what tokenization does and why it's the first step in NLP.

## Answer:

Tokenization breaks text into smaller pieces such as words, punctuation, or subwords. For example, "I'm learning NLP in 2025!" can be split as ["I", "'m", "learning", "NLP", "in", "2025", "!"]. It comes first because a model needs tokens to work with text instead of raw characters.

----

## 2
What is the difference between stemming and lemmatization? Apply both to the words "running" and "better" and explain which preserves more linguistic meaning. Hint: stemming is fast but crude (cuts off suffixes). Lemmatization uses a dictionary to find the base form.

## Answer:
Stemming is a rough shortcut. It chops off endings, so "running" often becomes "run", and "better" may stay as "better". Lemmatization is smarter. It uses word forms and a dictionary, so "running" becomes "run" and "better" becomes "good". That makes lemmatization better at preserving real meaning.

----

3 What does TF-IDF stand for? Explain in plain language why the word "the" scores almost zero in TF-IDF, while the word "photosynthesis" would score high. Think about: what makes a word useful for identifying a specific document among many documents?

## Answer:
TF-IDF stands for Term Frequency times Inverse Document Frequency. It gives a word more weight when it appears a lot in one document but not many others. "The" shows up everywhere, so it gets a low score. "Photosynthesis" is rarer and more specific, so it gets a much higher score and helps identify the right document.

----

> VECTOR DATABASES & EMBEDDINGS  Q4-Q6

## 4
What is a sentence embedding? How is it fundamentally different from one-hot encoding? Give one advantage embeddings have that one-hot vectors don't. Think about: what can you measure between two embeddings that you can't measure between two one-hot vectors?

## Answer:
A sentence embedding is a numeric vector that captures meaning. One-hot encoding is much more basic, because it only marks whether something is present or not. Embeddings are useful because they let you compare meanings, not just check exact matches.

----

## 5
Explain cosine similarity in plain language. If two document vectors point in almost the same direction, what does that tell us about the documents they represent? You don't need to write the formula - a geometric or intuitive explanation is enough. Bonus (+0.5 optional): When might Euclidean distance be a poor choice for comparing embeddings?

## Answer:
Cosine similarity looks at the direction of two vectors. If they point in almost the same direction, the documents are probably about similar ideas. Euclidean distance can be a bad choice when the vectors differ a lot in length, because size can get in the way of the real comparison.

----

## 6
Why can't a regular SQL query like `WHERE description LIKE '%pizza%'` find semantically similar documents? What does a vector index solve that SQL can't? Example to think about: "Italian food" and "pasta and risotto" - one contains the word, the other doesn't, but they're about the same topic.

## Answer:
A normal SQL search only matches the exact words it is given. It cannot tell that two different phrases might be talking about the same idea. A vector index solves that by comparing embeddings and finding content with similar meaning, even when the wording is different.

----

RAG - RETRIEVAL-AUGMENTED GENERATION  Q7-Q8

## 7
What problem does RAG solve that a plain LLM (without RAG) cannot? Give a concrete example of when you would choose RAG over just prompting the LLM directly. Think about: knowledge cutoffs, private data, hallucinations, up-to-date information.

## Answer:
RAG helps when the model needs real information, not just what it remembers. It gives the model actual documents to read, which is useful for private data, recent facts, or anything that needs to be accurate. A good example is asking about an internal company policy, where RAG can pull the relevant passage instead of making it up.

----

## 8
Describe the 3 main steps of a RAG pipeline in the correct order. Be clear about what happens at ingestion time (when you load documents) vs query time (when a user asks a question). The 3 steps are: chunk > embed > store (ingestion) and embed query > retrieve > generate (query time).

## Answer:
At ingestion time, you split the documents into chunks, turn those chunks into embeddings, and store them in a vector database. At query time, you embed the question, find the closest chunks, and let the model answer using those chunks as context.

----

DOCKER  +  AI AGENTS  Q9-Q10

## 9
What is the difference between a Docker image and a Docker container? Use an analogy to explain. Common analogies: class vs instance, recipe vs cake, blueprint vs building. Any analogy that works is fine.

## Answer:
A Docker image is like a recipe or blueprint. It contains the setup for an app. A container is the live thing you run from that recipe, so it is the actual working instance.

----

## 10
What is the difference between a simple LLM chatbot and an AI agent with tools? Give one concrete example of a "tool" and explain why it makes the agent more capable. Think about: what can an agent do that a plain LLM cannot? (e.g., look things up in real-time, run code, query a database, send an email...)

## Answer:
A simple chatbot mostly just writes text. An agent can also use tools, such as a web search or a calculator, to get live information and do real actions. That makes it much more useful than a chatbot that only talks.

----

MCP & AGENT SKILLS  Q11-Q12

## 11
What is MCP (Model Context Protocol)? What problem does it solve for AI coding assistants like GitHub Copilot? Name two examples of things an MCP server might expose to an AI assistant. Think about: how does a language model normally know about your database, your files, or your GitHub issues? What does MCP standardize?

## Answer:
MCP is a standard for giving AI assistants access to outside tools and data. It solves the problem of models not knowing how to connect to files, databases, or GitHub in a consistent way. Two examples are a file server and a database query server.

----

##12
What are Agent Skills in the context of AI coding assistants? How are they different from just writing instructions in a plain prompt? Show a minimal example of what a skill's `.md` metadata block might look like. Think about: a skill has a name, a description, and a path to a detailed instructions file - it lets the AI decide when to activate domain-specific knowledge automatically.

## Answer:
Agent Skills are reusable pieces of guidance that help an assistant know when to use a certain capability. They are more structured than a plain prompt, so the assistant can choose the right behavior automatically. A simple example looks like this:

```
name: mongodb-query-optimizer
description: Optimize MongoDB queries and recommend indexes for slow aggregations.
file: skills/mongodb-query-optimizer/SKILL.md
```

# Example skill metadata in copilot-instructions.md
<skill>
	<name>mongodb-query-optimizer</name>
	<description>Help with MongoDB query optimization and indexing.
	Use when the user asks "How do I optimize this query?"
	or "Why is this query slow?"</description>
	<file>path/to/skills/mongodb-query-optimizer/SKILL.md</file>
</skill>
