from generation.llm import generate_answer

context = """

CUDA is NVIDIA's parallel computing platform.

"""

question = "Explain CUDA."

answer = generate_answer(question, context)

print(answer)