from ollama import Client

client = Client(host="http://localhost:11434")

print(client.list())

response = client.chat(
    model="qwen2.5:7b",
    messages=[{"role": "user", "content": "What is CUDA?"}]
)

print(response["message"]["content"])