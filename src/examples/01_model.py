import os
import warnings
warnings.filterwarnings("ignore")
from dotenv import load_dotenv
load_dotenv()

# model usecase without using langchain
from openai import OpenAI
client = OpenAI()
client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": "Please tell me about the Major League Baseball"
        },
    ]
)

# model usecase with using langchain openai library
from langchain_openai import ChatOpenAI
chat = ChatOpenAI(model="gpt-3.5-turbo")
chat.invoke("Please tell me about the Major League Baseball") # send msg via invoke() method