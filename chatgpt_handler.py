import openai
from generic_openai_key import API_KEY
openai.api_key = API_KEY
import markdown

def call_chatgpt(prompt,temperature=0.25):
    #TODO add verbose/feedback to stdout
    # make api call
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ], 
        temperature = temperature
    )
        
    # extract response
    trasncript_output = response.choices[0].message.content

    return(trasncript_output)
