def chunk_text(text_by_page):
    """
    Splits text into smaller chunks:
    - single lines
    - bullet points
    - paragraphs
    This increases LLM accuracy.
    """
    chunks = []

    for page, text in text_by_page.items():
        lines = [l.strip() for l in text.split("\n") if l.strip()]

        for line in lines:
            # Bullet
            if line.startswith(("-", "•", "*")):
                chunks.append({"page": page, "type": "bullet", "text": line})
                continue

            # Key:Value-like structure
            if ":" in line:
                chunks.append({"page": page, "type": "kv_candidate", "text": line})
                continue

            # Normal line
            chunks.append({"page": page, "type": "line", "text": line})

    return chunks
