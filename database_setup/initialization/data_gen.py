from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_KEY'))

f = open('database_setup/initialization/complete_db.json')

data = json.load(f)


for o in data['origin']:
    for m in o['missions']:
        for s in m['specimens']:
            print(s)
    
            completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant who is going to only generate whole numbers based on the provided info."},
                {"role": "user", "content": f"Based on this specimen:\n{s}\ngenerate a numeric height in cm for it. If there Generate one whole number only."}
            ]
            )
            c = completion.choices[0].message.content
            print(c)
            s['height'] = int(c)

f.close()