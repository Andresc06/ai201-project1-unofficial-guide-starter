# Milestone 5: grounded answer generation.
import os

from dotenv import load_dotenv
from groq import Groq

from vector_store import retrieve

load_dotenv()

client = Groq(api_key=os.environ["GROQ_API_KEY"])
MODEL = "llama-3.3-70b-versatile"

# Grounding is ENFORCED here: the model is told to use only the reviews we
# pass in, and to refuse with a fixed sentence when they don't answer.
SYSTEM_PROMPT = (
    "You answer questions about Austin Community College professors using "
    "ONLY the student reviews provided as context. Do not use any outside "
    "knowledge or assumptions. If the reviews do not contain enough "
    "information to answer the question, reply with exactly this sentence: "
    "\"I don't have enough information on that.\" "
    "Every claim in your answer must be supported by the reviews provided."
)


def build_context(chunks):
    """Format retrieved chunks into a labeled context block for the prompt."""
    blocks = []
    for c in chunks:
        blocks.append(f"[Source: {c['source']}]\n{c['text']}")
    return "\n\n".join(blocks)


def ask(question, k=5):
    """Retrieve, generate a grounded answer, and return it with its sources.

    Returns a dict: {answer, sources, chunks}.
    """
    chunks = retrieve(question, k=k)
    context = build_context(chunks)

    user_prompt = (
        f"Context (student reviews):\n{context}\n\n"
        f"Question: {question}\n\n"
        "Answer using only the reviews above."
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,  # deterministic, sticks closely to the context
    )
    answer = response.choices[0].message.content.strip()

    # Source attribution is guaranteed programmatically (not left to the LLM):
    # unique source filenames of the chunks we actually retrieved, in order.
    sources = list(dict.fromkeys(c["source"] for c in chunks))

    return {"answer": answer, "sources": sources, "chunks": chunks}


# Quick end-to-end test:  python query.py
if __name__ == "__main__":
    test_questions = [
        "Which professor do students repeatedly say never responds to emails the most?",
        "What grading system is Rudi Martinez most criticized for?",
        "What is the best dining hall on campus?",  # out-of-scope -> should refuse
    ]

    for q in test_questions:
        result = ask(q)
        print("=" * 80)
        print("Q:", q)
        print("-" * 80)
        print(result["answer"])
        print("\nSources:", ", ".join(result["sources"]))
        print()
