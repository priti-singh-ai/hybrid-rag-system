import ollama


def generate_answer(question, context, history=None):

    history_text = ""

    if history:
        history_text = str(history)

    prompt = f"""
You are a helpful assistant.

Conversation History:
{history_text}

Context:
{context}

Question:
{question}

Answer:
"""

    response = ollama.chat(
        model="qwen2.5:7b",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]