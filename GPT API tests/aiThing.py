from openai import OpenAI
import pandas as pd
import sys

import base64

import requests
import random
client = OpenAI(api_key="null")

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
#585354866

def get_embedding(text, model="text-embedding-3-small"):
  cool = client.embeddings.create(model, input=[text], encoding_format="float")
  

def get_new_response(mes, see):
  
  responsers = client.responses.create(
    model="gpt-4.1-2025-04-14",
    input=mes,
    #stream=True,
    #tools=[{"type": "file_search", "vector_store_ids": ["vs_67e6272c2e708191bb56591608ebc0e5"], "max_num_results":10}],
    )
  
  
  #print("fart")
  print(responsers.output_text)
  response = responsers.output_text
  '''
  for chunk in responsers:
    if(chunk.type == "response.output_text.delta"):
      print(chunk.delta, end="")
      response += chunk.delta
  #print(responsers.output_text)
  #print("farter")
  '''
  return response


def get_response(mes, see):
    # load & inspect dataset
    #a = get_embedding("hi")
    #gpt-4o-2024-11-20 less expensive and just ok
    #gpt-4.1-2025-04-14
    #o1-mini
    
    
    awesome = client.chat.completions.create(
        model="gpt-4.1-nano-2025-04-14",
        messages=mes,
        stream=True)
    
    response = ""
    for chunk in awesome:

        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
            response += chunk.choices[0].delta.content
            
    return response

def get_image():
  a = client.images.generate(
    model="dall-e-3",
    prompt="Make a photo of a guy thats really angry. The head of this person should be flying off like an angry emoji and steam out of the ears and stuff.",
    n=1,
    size="1024x1024",
    response_format="b64_json"
  )
  print(a.data[0].revised_prompt)
  print(a.data[0].b64_json[:50])
  


def main():

    se = random.randint(0, 10000000000)
    print(se)

    messages = []
    
    while True:
        inp = input("\n")
        messages.append({"role": "user", "content": inp})
        
        response = get_new_response(messages, se)
        messages.append({"role": "assistant", "content": response})
        
    
        
    
        
        
        
 


if __name__ == "__main__":
    main()
