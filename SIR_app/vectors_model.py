import os
import re
import math
from collections import defaultdict
from .read import read_documents

def preprocess(text):
    return re.findall(r'\b\w+\b', text.lower())

def calculate_tf(term, document):
    return document.split().count(term)

def calculate_idf(term, documents):
    document_count = sum(1 for doc in documents if term in doc)
    return math.log(len(documents) / (document_count + 1e-10))

def create_vector(document, query_terms, documents):
    vector = {}
    for term in query_terms:
        tf = calculate_tf(term, document)
        idf = calculate_idf(term, documents)  # Consider all documents for IDF
        vector[term] = tf * idf
    return vector

def cosine_similarity(vector1, vector2):
    dot_product = sum(vector1.get(term, 0) * vector2.get(term, 0) for term in set(vector1) & set(vector2))
    magnitude1 = math.sqrt(sum(value ** 2 for value in vector1.values()))
    magnitude2 = math.sqrt(sum(value ** 2 for value in vector2.values()))
    if magnitude1 == 0 or magnitude2 == 0:
        return 0
    return dot_product / (magnitude1 * magnitude2)

def rank_documents(query_vector, document_vectors):
    rankings = [(doc, cosine_similarity(query_vector, doc_vector)) for doc, doc_vector in document_vectors.items()]
    rankings.sort(key=lambda x: x[1], reverse=True)
    return rankings

def vecotr_search(query):
    documents = read_documents()
    query_terms = preprocess(query)
    document_vectors = {doc: create_vector(content, query_terms, documents.values()) for doc, content in documents.items()}
    query_vector = create_vector(query, query_terms, documents.values())
    ranked_documents = rank_documents(query_vector, document_vectors)

    highlighted_results = []
    context_size = 100  # number of characters before and after the match to include in the snippet

    for doc, _ in ranked_documents:
        text = documents[doc]
        snippets = []
        for word in query_terms:
            for match in re.finditer(f"\\b({word})\\b", text, flags=re.IGNORECASE):
                start = max(match.start() - context_size, 0)
                end = min(match.end() + context_size, len(text))
                snippet = text[start:end].replace(match.group(), f"<strong>{match.group()}</strong>")
                snippets.append(snippet)
        highlighted_snippet = "<br><br>".join(snippets)  # Using '<br>' to separate snippets on new lines
        highlighted_results.append((doc, highlighted_snippet))

    return highlighted_results

