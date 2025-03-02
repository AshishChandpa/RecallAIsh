def chunk_text(text: str, chunk_size: int = 200, chunk_overlap: int = 50) -> list:
    """
    Splits text into overlapping chunks based on a word count.
    """
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i : i + chunk_size])
        chunks.append(chunk)
        i += max(chunk_size - chunk_overlap, 1)
    return chunks
