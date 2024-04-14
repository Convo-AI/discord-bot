from openai import AsyncOpenAI
import os


API_KEY = os.getenv('CONVOAI_API_KEY')

openai_client = AsyncOpenAI(       
  api_key=API_KEY,        
  base_url="https://api.convoai.tech/v1/"
)

async def generate_image(prompt, model):
  response = await openai_client.images.generate(
      model=model,
      prompt=prompt,
      n=1,
      size="1024x1024",
  )
  return response.data[0].url or None

async def generate_chat(messages, model):
  chat_completion = await openai_client.chat.completions.create(
      model=model,
      messages=messages,
  )
  return chat_completion.choices[0].message.content or None