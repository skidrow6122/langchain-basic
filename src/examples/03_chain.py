# with LCEL
import os
import warnings
warnings.filterwarnings("ignore")
from dotenv import load_dotenv
load_dotenv()

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# simple chian
prompt = ChatPromptTemplate.from_template("tell me about the key point about {topic}")
model = ChatOpenAI(model="gpt-4o-mini")
chain = prompt | model | StrOutputParser()
chain.invoke({"topic": "golf"})

# with streaming
prompt_streaming = ChatPromptTemplate.from_template("tell me about history of {topic}")
model_streaming = ChatOpenAI(model="gpt-4o")
chain_streaming = prompt_streaming | model_streaming
for s in chain_streaming.stream({"topic": "golf"}):
    print(s.content, end="", flush=True)
