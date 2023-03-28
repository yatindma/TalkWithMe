from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def find_most_similar_source(query, sources):
    """
    Compares the query with the provided sources and returns the source with the highest similarity.
    """
    vectorizer = TfidfVectorizer()
    source_texts = [source["text"] for source in sources]
    tfidf_matrix = vectorizer.fit_transform(source_texts + [query])

    cosine_similarities = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1])
    most_similar_index = cosine_similarities.argmax()

    return sources[most_similar_index]
