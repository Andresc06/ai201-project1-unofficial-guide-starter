import chromadb
from sentence_transformers import SentenceTransformer

from pipeline import get_all_chunks

# Load the embedding model once when this module is imported, then reuse it.
print("Loading embedding model: all-MiniLM-L6-v2 ...")
model = SentenceTransformer("all-MiniLM-L6-v2")


def build_vector_store(folder_path="./documents"):
    """Embed every chunk and (re)load them into ChromaDB with source metadata."""
    chunks = get_all_chunks(folder_path)

    texts = [c["text"] for c in chunks]

    print(f"Embedding {len(texts)} chunks ...")
    # encode() turns each chunk of text into a vector of 384 numbers.
    embeddings = model.encode(texts, show_progress_bar=True).tolist()

    client = chromadb.PersistentClient(path="./chroma_db")

    # Start clean each run so re-running doesn't pile up duplicate chunks.
    try:
        client.delete_collection("professor_reviews")
    except Exception:
        pass

    # "cosine" distance => score in [0, 2]; lower = more similar.
    # (This is the scale the milestone's 0.18 / 0.61 examples use.)
    collection = client.create_collection(
        name="professor_reviews",
        metadata={"hnsw:space": "cosine"},
    )

    # ChromaDB needs a unique id per chunk; metadata carries attribution.
    ids = [f"{c['source']}::chunk{c['position']}" for c in chunks]
    metadatas = [
        {"source": c["source"], "position": c["position"]} for c in chunks
    ]

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f"Stored {collection.count()} chunks in ChromaDB at {"./chroma_db"}\n")
    return collection


def get_collection():
    """Open the already-built collection (used by retrieve / later milestones)."""
    client = chromadb.PersistentClient(path="./chroma_db")
    return client.get_collection("professor_reviews")


def retrieve(query, k=5):
    """Return the top-k most semantically similar chunks for a query.

    Each result is a dict: text, source, position, distance.
    """
    collection = get_collection()

    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k,
    )

    # Chroma wraps each field in an extra list (one per query); we sent one query.
    hits = []
    for text, meta, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        hits.append({
            "text": text,
            "source": meta["source"],
            "position": meta["position"],
            "distance": distance,
        })
    return hits
