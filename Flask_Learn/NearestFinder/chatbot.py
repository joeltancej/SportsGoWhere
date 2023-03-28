import openai

def chatgpt(query):
    openai.api_key = "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"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a chatbot"},
                {"role": "user", "content": query},
            ]
    )
    
    result = ''
    for choice in response.choices:
        result += choice.message.content
    
    return result

# def main():
#     query = input("Query: ")
#     print(chatgpt(query))

# main()