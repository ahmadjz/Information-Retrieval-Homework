import re
from .read import read_documents

def preprocess(text):
    text = text.lower()
    text is re.sub(r"[^\w\s]", "", text)
    words = text.split()
    return set(words)

def create_index(documents):
    index = {}
    for doc, text in documents.items():
        words = preprocess(text)
        for word in words:
            index.setdefault(word, []).append(doc)
    return index

def parse_query(query):
    query = preprocess(query)
    stack = []
    precedence = {"not": 3, "and": 2, "or": 1}
    for word in query:
        if word in precedence:
            while stack and stack[-1] in precedence and precedence[word] <= precedence[stack[-1]]:
                yield stack.pop()
            stack.append(word)
        else:
            yield word
    while stack:
        yield stack.pop()

def evaluate_query(query, index):
    query = list(parse_query(query))
    stack = []
    for word in query:
        if word in {"not", "and", "or"}:
            if stack:
                a = stack.pop()
            else:
                a = set()
            if stack:
                b = stack.pop()
            else:
                b = set()

            if word == "not":
                stack.append(b - a)
            elif word == "and":
                stack.append(a & b)
            elif word == "or":
                stack.append(a | b)
        else:
            stack.append(set(index.get(word, [])))
    return stack.pop() if stack else set()

# Read the documents from a folder
documents = read_documents()

# Create an inverted index from the documents
index = create_index(documents)

def boolean_search(query):
    result_docs = evaluate_query(query, index)
    highlighted_results = []
    context_size = 100  
    query_words = preprocess(query)

    for doc in result_docs:
        text = documents[doc]
        snippets = []
        for word in query_words:
            # Find all occurrences of the word and extract context
            for match in re.finditer(f"\\b({word})\\b", text, flags=re.IGNORECASE):
                start = max(match.start() - context_size, 0)
                end = min(match.end() + context_size, len(text))
                snippet = text[start:end].replace(match.group(), f"<strong>{match.group()}</strong>")
                snippets.append(snippet)
        # Combine all snippets for this document with line breaks
        highlighted_snippet = "<br><br>".join(snippets)  # Using '<br>' to separate snippets on new lines
        highlighted_results.append((doc, highlighted_snippet))

    return highlighted_results
