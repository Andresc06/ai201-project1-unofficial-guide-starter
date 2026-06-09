# The Unofficial Guide — Project 1
---

## Domain

This system covers **student reviews of Computer Science professors at Austin
Community College (ACC)**, collected from Rate My Professors. It answers
questions about teaching style, communication, grading, workload, and exam
difficulty, the kind of information students actually use to decide who to
take.

This knowledge is valuable but hard to find through official channels: the ACC
course catalog lists what a class covers, but says nothing about whether a
professor answers emails, grades fairly, or is understandable in lecture.

---

## Document Sources

10 documents, one `.txt` file per professor, each containing that professor's
full set of Rate My Professors reviews.

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Rate My Professors — Adrian Edmundson | Reviews (.txt) | https://www.ratemyprofessors.com/professor/1771010 |
| 2 | Rate My Professors — David Trevino | Reviews (.txt) | https://www.ratemyprofessors.com/professor/1157272 |
| 3 | Rate My Professors — Femi Onabajo | Reviews (.txt) | https://www.ratemyprofessors.com/professor/601010 |
| 4 | Rate My Professors — Fred Kumi | Reviews (.txt) | https://www.ratemyprofessors.com/professor/247118 |
| 5 | Rate My Professors — Kimberly Jorgenson | Reviews (.txt) | https://www.ratemyprofessors.com/professor/1965147 |
| 6 | Rate My Professors — Murtaza Ally | Reviews (.txt) | https://www.ratemyprofessors.com/professor/1229898 |
| 7 | Rate My Professors — Michael Miller | Reviews (.txt) | https://www.ratemyprofessors.com/professor/2037000 |
| 8 | Rate My Professors — Ralph Hooper | Reviews (.txt) | https://www.ratemyprofessors.com/professor/2321388 |
| 9 | Rate My Professors — Rene Polanco | Reviews (.txt) | https://www.ratemyprofessors.com/professor/1011587 |
| 10 | Rate My Professors — Rudi Martinez | Reviews (.txt) | https://www.ratemyprofessors.com/professor/1104237 |

---

## Chunking Strategy

**Chunk size:** one review per chunk, with a soft limit of 800 characters.

**Overlap:** 0 characters.

**Preprocessing:** each document is split on the `Course:` delimiter, so every
review (Course, Professor, Date, Quality, Difficulty, and the review text)
becomes a single chunk. Reviews longer than 800 characters are split into
800-character pieces as a safeguard, but in practice almost every review is
shorter, so very little splitting happens.

**Why these choices fit my documents:** each review is a self-contained unit of
feedback — a complete opinion about one professor in one course. Splitting by
review keeps that thought intact and attaches its metadata, so a retrieved
chunk is meaningful on its own. I avoided fixed-size character chunking because
it would cut reviews mid-sentence and mix two students' opinions into one
chunk. No overlap is needed because reviews don't continue across boundaries.

**Final chunk count:** 560 chunks across the 10 documents.

### Sample chunks

1. **Professor David Trevino.txt**
   > Course: ITSE2309 — Never responds to emails. Disorganized. Assignments missing. Tests cover obscure book details. Allegedly protected by department chair.

2. **Professor Rudi Martinez.txt**
   > Course: ITSE1359 — No partial credit. 90% correct = 0. 50% correct = 0. Doesn't provide feedback. Worst experience.

3. **Professor Rene Polanco.txt**
   > Course: COSC1336 — Even if your code works exactly as required, you'll be docked if it's not in his preferred style. Many methods to solve problems, but he only accepts one.

4. **Professor Femi Onabajo.txt**
   > Course: COSC1336 — Thick accent, tells random stories, rarely covers important material. Tests didn't match lectures. Never reviewed exams. Great personality, terrible teaching.

5. **Professor Murtaza Ally.txt**
   > Course: COSC1337 — Second time taking him. C++ harder than Python but still enjoyable. Best programming professor at ACC.

6. **Professor Kimberly Jorgenson.txt**
   > Course: COSC1337 — Great professor. Lectures cover required material, instructions are clear, and exam reviews help. Responds to emails on time and provides helpful feedback.

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` via `sentence-transformers`. Chunks are stored in
**ChromaDB** with the collection configured for **cosine distance**, so scores
fall on a 0–2 scale where lower means more similar.

**Production tradeoff reflection:** if I were deploying this for real users and
cost wasn't a constraint, I would consider a larger hosted embedding model
(e.g., OpenAI's `text-embedding-3-large`). The tradeoffs I'd weigh:

- **Accuracy on domain-specific text:** review language is opinionated and full
  of slang, sarcasm, and implied meaning.
- **Context length:** MiniLM truncates input at 256 tokens, which is fine for
  short reviews but would be limiting for long-form documents.
- **Latency and cost:** a hosted API adds network latency and per-call cost and
  introduces rate limits (the opposite of MiniLM).

---

## Retrieval Test Results

I embed the query with the same model and ask ChromaDB for the top-5 nearest
chunks. Below are three of my evaluation queries with the sources and distances
of their top results.

**Query: "What grading system is Rudi Martinez most criticized for?"**
```
[0.402] Professor Rudi Martinez.txt (pos 27)
[0.415] Professor Rudi Martinez.txt (pos 3)
[0.432] Professor Rudi Martinez.txt (pos 43)
[0.449] Professor Rudi Martinez.txt (pos 40)
[0.452] Professor Rudi Martinez.txt (pos 9)
```
**Why these are relevant:** all five chunks come from the correct professor and
sit at low cosine distances (0.40–0.45). They contain the exact complaint the
query targets — reviews describing his "0-or-100" all-or-nothing grading. This
is textbook good retrieval: on-topic, on-source, tightly clustered.

**Query: "What recurring complaint do students have about Femi Onabajo's lectures?"**
```
[0.330] Professor Femi Onabajo.txt (pos 1)
[0.342] Professor Femi Onabajo.txt (pos 23)
[0.345] Professor Femi Onabajo.txt (pos 64)
[0.362] Professor Femi Onabajo.txt (pos 31)
[0.363] Professor Femi Onabajo.txt (pos 35)
```
**Why these are relevant:** the lowest distances in the whole evaluation
(0.33–0.36) and all from the right professor. The chunks describe lectures that
are "just reading slides," matching the query's intent even though the query
never used the word "slides" — semantic search found the meaning, not the exact
words.

**Query: "Which professor never responds to emails the most?"**
```
[0.501] Professor Fred Kumi.txt (pos 22)
[0.519] Professor Murtaza Ally.txt (pos 36)
[0.529] Professor David Trevino.txt (pos 31)
[0.532] Professor Adrian Edmundson.txt (pos 13)
[0.533] Professor David Trevino.txt (pos 11)
```
This retrieval was weaker — distances above 0.5 and a mix of sources. David
Trevino (the correct answer) appears only at ranks 3 and 5, and the top hit is
the mislabeled `Fred Kumi` file.

---

## Grounded Generation

**System prompt grounding instruction:**
```
You answer questions about Austin Community College professors using ONLY the
student reviews provided as context. Do not use any outside knowledge or
assumptions. If the reviews do not contain enough information to answer the
question, reply with exactly this sentence: "I don't have enough information on
that." Every claim in your answer must be supported by the reviews provided.
```

**How source attribution is surfaced:** attribution is handled
**programmatically, not by the LLM**. After generation, `query.py` collects the
unique source filenames of the chunks that were actually retrieved and returns
them alongside the answer. This guarantees every response is accompanied by the
real documents it drew from, even if the model forgets to cite them.

### Example responses

**Example 1 — in-scope, accurate, with attribution:**
> **Q:** What grading system is Rudi Martinez most criticized for?
> **A:** Rudi Martinez is most criticized for his 0-or-100 grading system,
> described in multiple reviews as nerve-wracking — one mistake results in a 0
> with no partial credit.
> **Retrieved from:** Professor Rudi Martinez.txt

**Example 2 — in-scope, accurate, with attribution:**
> **Q:** What recurring complaint do students have about Femi Onabajo's lectures?
> **A:** Students repeatedly complain that his lectures are just verbatim
> readings of PowerPoint or textbook slides with little added explanation
> (e.g., INTW1325, ITSY1300, ITNW2321).
> **Retrieved from:** Professor Femi Onabajo.txt

**Example 3 — out-of-scope query, correct refusal:**
> **Q:** What is the best dining hall on campus?
> **A:** I don't have enough information on that.

The third example is the key grounding test: the documents contain only
professor reviews, so the system correctly declined instead of inventing a
dining-hall answer from the model's training data.

---

## Query Interface

The interface is a **Gradio web app** (`app.py`).

- **Input field:** "Your question" — a free-text box for the student's question.
- **Output fields:** "Answer" (the grounded response) and "Retrieved from" (the
  list of source documents the answer drew from).

Run it with `python app.py`, then open http://localhost:7860.

**Sample interaction transcript:**
```
Your question:  What grading system is Rudi Martinez most criticized for?

Answer:         Rudi Martinez is most criticized for his 0-or-100 grading
                system, described in multiple reviews as nerve-wracking — one
                mistake results in a 0 with no partial credit.

Retrieved from: • Professor Rudi Martinez.txt
```

---

## Evaluation Report

All 5 test questions from `planning.md`, run through the full system.

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Which professor never responds to emails the most? | David Trevino | Correctly named David Trevino, but cited only one course and claimed "no other professor" is mentioned | Partially relevant (correct professor only ranks 3rd/5th; top hit is the mislabeled Fred Kumi file; distances 0.50–0.53) | Partially accurate |
| 2 | What grading system is Rudi Martinez most criticized for? | "0-or-100" all-or-nothing grading, no partial credit | "0-or-100 grading system… one mistake results in a 0 with no partial credit" | Relevant (all 5 from Rudi, 0.40–0.45) | Accurate |
| 3 | Why do students say Rene Polanco grades harshly even when their code works? | Deducts points for code not matching his exact style / things not in instructions | Said the reviews don't state the *context* of the harsh grading — only that he "grades harshly" and "doesn't explain mistakes" — so it couldn't explain the "even when code works" part | Relevant (all 5 from Polanco, 0.34–0.35) | **Inaccurate (failed to answer)** |
| 4 | What recurring complaint about Femi Onabajo's lectures? | Hard to understand (accent); just reads slides | "Lectures are just verbatim readings of PowerPoints/slides…" | Relevant (all 5 from Femi, 0.33–0.36) | Accurate |
| 5 | Which professor is most often called the best programming professor at ACC? | Murtaza Ally | Called it a "tie" between Murtaza Ally and Fred Kumi | Partially relevant (top hit is mislabeled Fred Kumi file) | Partially accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

**Question that failed:** "Why do students say Rene Polanco grades harshly even
when their code works?"

**What the system returned:** *"The reviews do not specifically state that Rene
Polanco grades harshly even when the students' code works. They only mention
that he 'grades harshly' and 'doesn't explain mistakes', but do not provide
information about the context of the harsh grading."* — in other words, a soft
refusal. This is wrong: many Polanco reviews explicitly explain the cause (e.g.,
*"Even if your code works exactly as required, you'll be docked if it's not in
his preferred style"*).

**Root cause (tied to a specific pipeline stage):** This was a generation-stage
failure caused by a retrieval–grounding mismatch. Retrieval correctly identified
Rene Polanco (all five chunks from his file at ~0.34 distance), but the specific
chunks that name the cause — code works but doesn't match his preferred style —
did not make the top 5. The chunks that did surface were general "grades
harshly / doesn't explain mistakes" reviews. The model's own response confirms
this: it explicitly says it only saw "grades harshly" and "doesn't explain
mistakes" and lacked the context. Because my grounding prompt requires strong
evidence, the model treated that context as insufficient and declined rather
than answering — even though the full answer exists elsewhere in the corpus.

**What I would change to fix it:** increase top-k (e.g., 8–10) so more of
Polanco's specific style-grading reviews are included, and/or soften the
grounding prompt to allow synthesis when the retrieved reviews are clearly
on-topic but don't contain a verbatim answer. 

---

## Spec Reflection

**One way the spec helped me during implementation:** my `planning.md`
Chunking Strategy and Retrieval Approach sections gave me concrete constraints
to hand the AI tool: "one review per chunk, 800-char soft limit, no overlap,
all-MiniLM-L6-v2, top-5." Because those decisions were already made and written
down, the generated `vector_store.py` matched what I actually needed on the
first pass instead of producing a generic fixed-size chunker. The architecture
diagram also kept the five pipeline stages clear as I built each file.

**One way my implementation diverged from the spec, and why:** my architecture
diagram originally said the vectors would be stored in a **FAISS** index, but I
implemented the system with **ChromaDB** instead. I switched because ChromaDB
is the course's recommended stack, it stores metadata (source filename and
position) alongside each vector, which I needed for source attribution in
Milestone 5, and it persists to disk automatically. I also changed my chunk size
from an initial 350-character plan up to an 800-character soft limit once I saw
that real reviews were longer and more structured than I first assumed.

---

## AI Usage

**Instance 1 — generating the embedding/retrieval code**
- *What I gave the AI:* my Retrieval Approach and Chunking Strategy sections
  from `planning.md`, plus the requirement to store chunks in ChromaDB with
  source metadata and cosine distance.
- *What it produced:* a `vector_store.py` with a `build_vector_store()` function
  and a `retrieve()` function, using a lazy-loading `get_model()` helper with a
  module-level cache.
- *What I changed or overrode:* I removed the `get_model()` wrapper and global
  variable because I found it unnecessary for this project, replacing it with a
  single module-level model load. I also inlined the configuration constants
  rather than keeping them as separate variables.

**Instance 2 — refining my evaluation questions**
- *What I gave the AI:* my draft evaluation questions and the Milestone 2
  instruction that each question needs a specific, verifiable expected answer.
- *What it produced:* a revised set of five questions, each targeting one
  professor's distinctive and verifiable trait, plus expected answers grounded
  in the actual review text.
- *What I changed or overrode:* I replaced my original subjective question ("the
  3 most common negative themes," which has no single checkable answer) with a
  verifiable positive-control question about the best programming professor.
  The AI also flagged the mislabeled `Fred Kumi` file, which I documented as a
  known limitation rather than silently fixing.

**Instance 3 — designing the grounding prompt**
- *What I gave the AI:* my requirement that answers must come only from
  retrieved reviews and must refuse when context is insufficient.
- *What it produced:* the strict system prompt with the fixed refusal sentence,
  plus programmatic source attribution instead of trusting the LLM to cite.
- *What I changed or overrode:* I kept the strict refusal behavior even after
  seeing it cause a false refusal on the Polanco question, because I decided an
  over-cautious system is more honest for this use case than one that
  hallucinates — and I documented that tradeoff in my failure analysis.
