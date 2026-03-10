import os
import json

from sentence_transformers import SentenceTransformer
import faiss


class Retriever:

    def __init__(self):

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.documents = []
        self.doc_sources = []

        self.load_documents()

        embeddings = self.model.encode(self.documents)

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)

    def load_documents(self):

        data_folder = "data"

        # Load txt files
        for file in os.listdir(data_folder):

            path = os.path.join(data_folder, file)

            if file.endswith(".txt"):

                with open(path, "r") as f:
                    lines = f.readlines()

                    for line in lines:
                        clean = line.strip()

                        if clean:
                            self.documents.append(clean)
                            self.doc_sources.append(file)

            if file.endswith(".json"):

                with open(path, "r") as f:
                    data = json.load(f)

                    for key, value in data.items():

                        if isinstance(value, dict):
                            text = f"{key}: {value}"
                        else:
                            text = f"{key}: {value}"

                        self.documents.append(text)
                        self.doc_sources.append(file)

    def retrieve(self, query, k=3):

        query_embedding = self.model.encode([query])

        distances, indices = self.index.search(query_embedding, k)

        results = []
        sources = []

        for idx in indices[0]:
            results.append(self.documents[idx])
            sources = list(set(sources))

        return results, sources
    
    