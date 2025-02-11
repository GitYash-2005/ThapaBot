import openai

openai.api_key = "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"

def chat_with_gpt(prompt):
    
    response = openai.ChatCompletion.create(
        
        model = "gpt-4o-mini",
        messages = [{"role": "user" , "content" : prompt}]
    )
    
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit" , "exit" , "bye"]:
            break
        
        response = chat_with_gpt(user_input)
        
        print("ChatBot: " , response)
        
        