from vector_store import build_vector_store, retrieve

# Step 1: embed all chunks and load them into ChromaDB.
build_vector_store()

# Step 2: 3 of the 5 evaluation questions from planning.md.
test_queries = [
    "Which professor do students repeatedly say never responds to emails the most?",
    "What grading system is Rudi Martinez most criticized for?",
    "Why do students say Rene Polanco grades harshly even when their code works?",
]

# Step 3: retrieve and inspect.
for query in test_queries:
    print("=" * 80)
    print(f"QUERY: {query}")
    print("=" * 80)

    results = retrieve(query, k=5)

    for rank, hit in enumerate(results, start=1):
        print(
            f"\n[{rank}] source={hit['source']}  "
            f"position={hit['position']}  "
            f"distance={hit['distance']:.3f}"
        )
        print(hit["text"])

    print("\n")
