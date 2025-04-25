import openai
client = openai.OpenAI(
    api_key="sk-w1cHpuWFy-cnHeRAb6-KeQ",
    base_url="http://eldo:4000"
)


completion = client.chat.completions.create(
    model="gemini/gemini-2.5-flash-preview-04-17",
    messages=[
        {"role": "developer", "content": "Talk like a wizard."},
        {
            "role": "user",
            "content": "How do I check if a Python object is an instance of a class?",
        },
    ],
)

print(completion.choices[0].message.content)