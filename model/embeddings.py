from sentence_transformers import SentenceTransformer, util

# Load a light, fast embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str):
    """
    Generate an embedding vector from text.
    This is used for both resume and JD similarity scoring.
    """
    return model.encode(text, convert_to_tensor=True)

def compute_similarity(text1: str, text2: str) -> float:
    """
    Compute cosine similarity between two text embeddings.
    Returns a float between 0 and 1.
    """
    emb1 = get_embedding(text1)
    emb2 = get_embedding(text2)

    similarity = util.cos_sim(emb1, emb2)
    return float(similarity.item())
