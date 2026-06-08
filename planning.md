# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

This project focuses on students reviews of CS professors at Austin Community College collected from Rate My Professors. The goal is to build an unofficial guide that helps students find information about teaching style, difficulty, feedback quality, and course experiences by searching and summarizing review content. This knowledge is difficult to find because student experiences are scattered across many individual professor review pages and are not available through official college resources.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Rate My Professors | Adrian Edmundson reviews | https://www.ratemyprofessors.com/professor/1771010 |
| 2 | Rate My Professors | David Trevino reviews | https://www.ratemyprofessors.com/professor/1157272 |
| 3 | Rate My Professors | Femi Onabajo reviews | https://www.ratemyprofessors.com/professor/601010 |
| 4 | Rate My Professors | Fred Kumi reviews | https://www.ratemyprofessors.com/professor/247118 |
| 5 | Rate My Professors | Kimberly Jorgenson reviews | https://www.ratemyprofessors.com/professor/1965147 |
| 6 | Rate My Professors | Murtaza Ally reviews | https://www.ratemyprofessors.com/professor/1229898 |
| 7 | Rate My Professors | Michael Miller reviews | https://www.ratemyprofessors.com/professor/2037000 |
| 8 | Rate My Professors | Ralph Hooper reviews | https://www.ratemyprofessors.com/professor/2321388 |
| 9 | Rate My Professors | Rene Polanco reviews | https://www.ratemyprofessors.com/professor/1011587 |
| 10 | Rate My Professors | Rudi Martinez reviews | https://www.ratemyprofessors.com/professor/1104237 |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** ~1 review per chunk (soft limit: 800 characters)

**Overlap:** 0 characters

**Reasoning:** Originally, a 350-character fixed chunk size was chosen based on the assumption that reviews were short and self-contained. However, each review has more characters and contains structured information including course, professor, date, and review text. So, a soft limit of ~800 characters is used as a safeguard to prevent unusually long reviews from becoming too large for embedding models. After testing, most reviews naturally fall below this threshold, so no aggressive splitting is applied. Additionally, since each review is a distinct unit of feedback, no overlap is needed between chunks. Fixed-size character chunking was avoided because it can break reviews mid-sentence.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2 via sentence-transformers

**Top-k:** 5

**Production tradeoff reflection:** If cost wasn’t a concern, I would use a larger embedding model such as OpenAI embeddings because they generally produce better semantic understanding, especially for opinion-based text like student reviews. The tradeoff of course is how expensive and slow they can run, but they usually improve retrieval accuracy and handle refined language better than lightweight models like MiniLM. They can also better capture subtle differences in meaning (e.g., sarcasm or slang) instead of exact keywords.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Which professor is most frequently described as having unclear lectures or structure? | |
| 2 | Which professor is most often described as having very difficult exams? | |
| 3 | Which professor receives repeated complaints about lack of communication (emails not answered)? | |
| 4 | Which professor is described as having a very difficult course with heavy workload? | |
| 5 | What are the 3 most common negative themes across CS professors at ACC? | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Reviews are subjective and often biased, meaning the same professor can be described in completely different ways depending on the student experience.
2. Some professors may have way more reviews than others, which can bias the vector store toward those professors and make comparisons uneven or skewed.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->
```
[Rate My Professors pages (ACC CS professors)]
            ↓
[Pull reviews + basic cleaning (remove HTML / extra noise)]
            ↓
[Break into chunks (each review = one chunk, max ~800 chars)]
            ↓
[Create embeddings using sentence-transformers (MiniLM)]
            ↓
[Store vectors in FAISS index]
            ↓
[Search similar reviews (top 5 results)]
            ↓
[Send retrieved reviews to LLM]
            ↓
[Generate answer + cite reviews used]
```

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

I will use ChatGPT to help implement different parts of the pipeline by giving it specific sections of my planning.md as context. For example, I will provide my Chunking Strategy section and ask it to implement a chunk_text() function that follows my rule of "one review per chunk with a 800-character limit." I will also give it my Retrieval Approach section when building the vector search step so it uses the correct embedding model and top-k value. For prompt design, I will provide the requirement that the system must only use retrieved reviews and must include citations, and ask it to generate a grounded prompt template. I will verify each output by testing it against my sample documents and checking that it matches the exact constraints defined in my spec.

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
