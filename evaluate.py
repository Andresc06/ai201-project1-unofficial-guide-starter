# Milestone 6: run all 5 evaluation questions end-to-end.

from query import ask

EVAL_QUESTIONS = [
    "Which professor do students repeatedly say never responds to emails the most?",
    "What grading system is Rudi Martinez most criticized for?",
    "Why do students say Rene Polanco grades harshly even when their code works?",
    "What recurring complaint do students have about Femi Onabajo's lectures?",
    "Which professor is most often called the best programming professor at ACC?",
]

for i, question in enumerate(EVAL_QUESTIONS, start=1):
    result = ask(question)

    print("=" * 80)
    print(f"Q{i}: {question}")
    print("=" * 80)
    print("\nANSWER:")
    print(result["answer"])

    print("\nCITED SOURCES:")
    for s in result["sources"]:
        print(f"  • {s}")

    print("\nRETRIEVED CHUNKS (source | position | distance):")
    for hit in result["chunks"]:
        print(f"  [{hit['distance']:.3f}] {hit['source']} (pos {hit['position']})")

    print("\n")
