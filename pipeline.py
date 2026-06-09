import os
import random

def load_all_documents(folder_path):
    documents = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)

            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()

            documents.append({
                "source": filename,
                "text": text
            })

    return documents


def chunk_text(text, source, max_size=800):
    chunks = []
    position = 0  # index of this chunk within its source document

    reviews = text.split("Course:")

    for r in reviews:
        r = r.strip()
        if not r:
            continue

        r = "Course:" + r

        # attach metadata
        if len(r) > max_size:
            for i in range(0, len(r), max_size):
                chunks.append({
                    "source": source,
                    "position": position,
                    "text": r[i:i+max_size]
                })
                position += 1
        else:
            chunks.append({
                "source": source,
                "position": position,
                "text": r
            })
            position += 1

    return chunks


def print_random_chunks(chunks, n=5):
    print("\n=== RANDOM CHUNK INSPECTION ===\n")

    sample = random.sample(chunks, min(n, len(chunks)))

    for i, chunk in enumerate(sample):
        print(f"Source: {chunk['source']}")
        print(chunk["text"])
        print("\n" + "-" * 80 + "\n")


def get_all_chunks(folder_path="./documents"):
    # Load every document and return one flat list of chunks.
    documents = load_all_documents(folder_path)

    all_chunks = []
    for doc in documents:
        doc_chunks = chunk_text(doc["text"], doc["source"])
        all_chunks.extend(doc_chunks)

    return all_chunks


# ---------------- MAIN ----------------

if __name__ == "__main__":
    documents = load_all_documents("./documents")
    all_chunks = get_all_chunks("./documents")

    print(f"TOTAL DOCUMENTS: {len(documents)}")
    print(f"TOTAL CHUNKS: {len(all_chunks)}\n")

    print_random_chunks(all_chunks, n=5)