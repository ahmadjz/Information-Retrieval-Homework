import os
import re
import math
from collections import defaultdict
from .read import read_documents

def preprocess(text):
    return re.findall(r'\b\w+\b', text.lower())

def calculate_weight(term, document, documents):
    tf = document.count(term)
    idf = math.log(len(documents) / (sum(term in d for d in documents.values()) + 1e-10))
    return tf * idf

def create_index(documents):
    index = defaultdict(dict)
    for filename, content in documents.items():
        for term in set(preprocess(content)):
            index[term][filename] = calculate_weight(term, content, documents)
    return index

def parse_query(query):
    operators = {'or': 0, 'and': 1, 'not': 2}
    stack = []
    output = []
    for term in query.split():
        if term not in operators:
            output.append(term)
        else:
            while stack and stack[-1] in operators and operators[term] <= operators[stack[-1]]:
                output.append(stack.pop())
            stack.append(term)
    while stack:
        output.append(stack.pop())
    return output

def not_operation(docs, all_docs):
    return {doc: weight for doc, weight in all_docs.items() if doc not in docs}

def boolean_operation(docs1, docs2, op):
    if op == 'and':
        return {doc: min(docs1.get(doc, 0), docs2.get(doc, 0)) for doc in set(docs1) & set(docs2)}
    elif op == 'or':
        return {doc: max(docs1.get(doc, 0), docs2.get(doc, 0)) for doc in set(docs1) | set(docs2)}

def evaluate_query(expression, index, all_docs):
    stack = []
    for term in expression:
        if term in {'and', 'or', 'not'}:
            if not stack:
                return {}
            b = stack.pop()
            if term == 'not':
                stack.append(not_operation(b, all_docs))
            else:
                if not stack:
                    return {}
                a = stack.pop()
                stack.append(boolean_operation(a, b, term))
        else:
            stack.append(index.get(term, {}))
    return stack[0] if stack else {}

def extended_boolean_search(query):
    documents = read_documents()
    index = create_index(documents)
    all_docs = {doc: 1 for doc in documents}
    expression = parse_query(query)
    result_docs = evaluate_query(expression, index, all_docs)

    highlighted_results = []
    context_size = 100  # number of characters before and after the match to include in the snippet
    query_words = preprocess(query)

    for doc in result_docs.keys():
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
