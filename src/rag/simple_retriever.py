import os
import math
from typing import List, Tuple
from collections import Counter

REF_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'references')


def _tokenize(text: str) -> List[str]:
    return [t.lower() for t in ''.join(ch if ch.isalnum() else ' ' for ch in text).split() if t]


def _load_corpus() -> List[Tuple[str, str]]:
    docs: List[Tuple[str, str]] = []
    if not os.path.isdir(REF_DIR):
        return docs
    for name in os.listdir(REF_DIR):
        path = os.path.join(REF_DIR, name)
        if os.path.isfile(path) and name.lower().endswith('.txt'):
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    docs.append((name, f.read()))
            except Exception:
                continue
    return docs


def retrieve(query: str, k: int = 3) -> List[str]:
    corpus = _load_corpus()
    if not corpus:
        return []
    q_tokens = _tokenize(query)
    q_tf = Counter(q_tokens)
    # Build DF
    dfs = Counter()
    doc_tfs = []
    for name, text in corpus:
        tokens = _tokenize(text)
        tf = Counter(tokens)
        doc_tfs.append((name, tf))
        for term in set(tokens):
            dfs[term] += 1
    N = len(corpus)
    # Score
    scores = []
    for (name, tf) in doc_tfs:
        num = 0.0
        dq = 0.0
        dd = 0.0
        for term in set(q_tokens + list(tf.keys())):
            idf = math.log((N + 1) / (1 + dfs.get(term, 0))) + 1.0
            q_w = q_tf.get(term, 0) * idf
            d_w = tf.get(term, 0) * idf
            num += q_w * d_w
            dq += q_w * q_w
            dd += d_w * d_w
        denom = (dq ** 0.5) * (dd ** 0.5)
        score = (num / denom) if denom else 0.0
        scores.append((score, name))
    scores.sort(reverse=True)
    out = []
    for score, name in scores[:k]:
        out.append(f"[REF] {name}")
    return out
