from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values 
import os
import tempfile
import time
import traceback

env_vars = dotenv_values(os.path.join(os.path.dirname(__file__), "../.env"))

Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")


if not all([Username, Assistantname, GroqAPIKey]):
    raise ValueError("Missing environment variables. Please ensure .env contains Username, Assistantname, and GroqAPIKey.")


client = Groq(api_key=GroqAPIKey)


messages = []


System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""
SystemChatBot = [
    {"role": "system", "content": System}
]
data_folder = os.path.join(os.path.dirname(__file__), "../Data")
chat_log_path = os.path.join(data_folder, "ChatLog.json")


try:
    with open(chat_log_path, "r") as f:
        
        if f.read(1):
            f.seek(0)  
            messages = load(f)  
        else:
            messages = [] 
except FileNotFoundError:
    
    os.makedirs(data_folder, exist_ok=True)  
    # create file atomically to avoid partial writes
    tmp = chat_log_path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        dump([], f)
    os.replace(tmp, chat_log_path)
    messages = [] 
def RealtimeInformation():
    current_date_time = datetime.datetime.now()  
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d") 
    month = current_date_time.strftime("%B")  
    year = current_date_time.strftime("%Y")  
    hour = current_date_time.strftime("%H")  
    minute = current_date_time.strftime("%M")  
    second = current_date_time.strftime("%S")  
    
    data = f"Please use the real-time information if needed,\n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} Hours: {minute} Minutes: {second} second.\n"
    return data


def AnswerModifier(Answer):
    import re
    Answer = re.sub(r'\*+', ' ', Answer)

    # Split into lines and remove extra spaces/empty lines
    lines = Answer.split('\n')
    non_empty_lines = [line.strip() for line in lines if line.strip()]

    # Join cleaned lines back
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer
    # lines = Answer.split('\n') 
    # non_empty_lines = [line for line in lines if line.strip()]
    # modified_answer = '\n'.join(non_empty_lines)
    # return modified_answer

def ChatBot(Query):
    """This function sends the user's query to the chatbot and returns the API response"""
    try:
        with open(chat_log_path, "r") as f:
          
            if f.read(1): 
                f.seek(0)  
                messages = load(f)  
            else:
                messages = [] 
        messages.append({"role": "user", "content": f"{Query}"})
        
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",  
            messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,
            max_tokens=1024, 
            temperature=0.7, 
            top_p=1, 
            stream=True, 
            stop=None
        )

        Answer = "" 

        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "") 

        
        messages.append({"role": "assistant", "content": Answer})

        # Write chat log atomically to avoid corrupting/clearing on errors
        tmp = chat_log_path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            dump(messages, f, indent=4, ensure_ascii=False)
        os.replace(tmp, chat_log_path)

        return AnswerModifier(Answer=Answer)

    except Exception as e:
        # Print full traceback for debugging
        print(f"Error: {e}")
        traceback.print_exc()

        # Do NOT clear the chat log on error. If it's a rate-limit error, retry a few times with backoff.
        err_text = str(e).lower()
        if 'rate limit' in err_text or 'rate_limit' in err_text or '429' in err_text:
            max_retries = 3
            for attempt in range(1, max_retries + 1):
                wait = attempt * 2
                print(f"Rate limit detected — retrying in {wait}s (attempt {attempt}/{max_retries})...")
                time.sleep(wait)
                try:
                    return ChatBot(Query)
                except Exception as e2:
                    print(f"Retry {attempt} failed: {e2}")
            # after retries, return an informative message (without clearing file)
            return "Error: rate limit reached. Please try again in a few seconds."
        # For other exceptions, return the error string and preserve existing file
        return f"Error: {e}"

if __name__ == '__main__':
    while True:
        user_input = input("\nEnter Your Question: ")
        print(ChatBot(user_input))


