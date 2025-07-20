from openai import OpenAI
from anthropic import Anthropic
from google import genai

import os 
from dotenv import load_dotenv

load_dotenv()



#### "Setup" functions
#
#
#
#
# OpenAI
def chatgpt_load():
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    client = OpenAI(
    project=os.getenv('OPENAI_PROJECT'),
    api_key=OPENAI_API_KEY
    )
    
    return client

# Google
def gemini_load():
    client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))
    return client


# xAI
def grok_load():
    xAI_API_KEY = os.getenv('xAI_API_KEY')

    client = OpenAI(
    base_url="https://api.x.ai/v1",
    api_key=xAI_API_KEY
    )
    
    return client

# Anthropic
def claude_load():
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

    client = Anthropic(api_key=ANTHROPIC_API_KEY)
    return client



#### Functions to call different APIs
#
#
#
#
# OpenAI 
def chatgpt_request(model, message, prob_only=False):  
    if prob_only:
        messages=[ {'role':'system', 'content': "Provide your answer in the form of a percentage with no other text. Do not provide a range of probabilities, provide a single value"},
                   {"role": "user", 'content': message} ]

    else:
        messages=[ {"role": "user", 'content': message} ]

    return model.chat.completions.create(
            model='gpt-4o',
            messages=messages
        ).choices[0].message.content

# Google
def gemini_request(model, message, prob_only=False):
    if prob_only:
        sys_instruct = "Provide your answer in the form of a percentage with no other text. Do not provide a range of probabilities, provide a single value"
        
        response = model.models.generate_content(
            model="gemini-2.0-flash", contents=message,
            config=genai.types.GenerateContentConfig(
            system_instruction=sys_instruct)
        )
    else: 
                
        response = model.models.generate_content(
            model="gemini-2.0-flash", contents=message,
            config=genai.types.GenerateContentConfig(
            system_instruction=sys_instruct)
        )
    return response.text


# xAI 
def grok_request(model, message, prob_only=False):  
    if prob_only:
        messages=[ {'role':'system', 'content': "Provide your answer in the form of a percentage with no other text. Do not provide a range of probabilities, provide a single value"},
                   {"role": "user", 'content': message} ]

    else:
        messages=[ {"role": "user", 'content': message} ]


    return model.chat.completions.create(
            model="grok-2-latest",
            messages=messages
        ).choices[0].message.content

# Anthropic
def claude_request(model, message, prob_only=False):  
    if prob_only:
        messages = [{"role": "user", 'content': [{'type': 'text', 'text': message}]}]
    
        response = model.messages.create(
                model="claude-3-5-sonnet-20241022",
                temperature=1.0,
                max_tokens=4096,
                messages=messages,
                system="Provide your answer in the form of a percentage with no other text. Do not provide a range of probabilities, provide a single value"
            ).content[0].text

    else:        
        response = model.messages.create(
                model="claude-3-5-sonnet-20241022",
                temperature=1.0,
                max_tokens=4096,
                messages=messages,
            ).content[0].text
        
    return response