import ollama


def generate_answer(
    question,
    chunks
):

    context = "\n\n".join(chunks)

    prompt = f"""
You are a helpful contract analysis assistant.

Use ONLY the context below to answer the question.

Context:
{context}

Question:
{question}

Answer:
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]