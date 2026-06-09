from vector_store import build_vector_store, retrieve

# Step 1: embed all chunks and load them into ChromaDB.
build_vector_store()

# Step 2: 3 of the 5 evaluation questions from planning.md.
test_queries = [
    "Which professor has unclear lectures or disorganized course structure?",
    "Which professor is described as having very difficult exams?",
    "Which professor does not respond to emails or lacks communication?"
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
