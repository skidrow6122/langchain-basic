import os
import warnings

warnings.filterwarnings("ignore")
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.prompts import HumanMessagePromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

## ChatPromptTemplate 에 System Message 로 모델의 역할, 출력 형태 지정
## 매번 system message를 조작해줘야하는 불편
prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                "You are an expert in programming. please recommend the most famous programming language recently corresponding to the category of the input."
                "ex) Query: Please recommend 3 programming languages / Answer: ['Java','Go','Python']"
            )
        ),
        HumanMessagePromptTemplate.from_template("{input}"),
    ]
)

chain = prompt | model
chain.invoke("I want to know about the backend programming languages.")


## CSV output parser 활용
## langchain 이 CSV 형식대로 잘 파싱할수 있게 wrapping
from langchain.prompts import PromptTemplate
#from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import CommaSeparatedListOutputParser
#from langchain_core.output_parsers import CommaSeparatedListOutputParser

# CSV parser 선언
csv_output_parser = CommaSeparatedListOutputParser()

# CSV parser 작동을 위한 형식 지정 프롬프트 로드
format_instructions = csv_output_parser.get_format_instructions()

# 프롬프트 템플릿의 partial variables 에 CSV 형식지정 프롬프트 주입
prompt2 = PromptTemplate(
    template="List {input}. answer in korean \n{format_instructions}",
    input_variables=["input"],
    partial_variables={"format_instructions": format_instructions}
)

model2 = ChatOpenAI(model="gpt-4o-mini", temperature=0)
chain2 = prompt2 | model2 | csv_output_parser
chain2.invoke({"input": "comic movies"})


## Json output parser 활용
from typing import List
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

# define data structure
class Country(BaseModel):
    continent: str = Field(description="Continent the country is in")
    population: str = Field(description="Country population with Int type")

# Injection parser to the format_instructions
json_output_parser = JsonOutputParser(pydantic_object=Country)
prompt3 = PromptTemplate(
    template="Answer the user query. \n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": json_output_parser.get_format_instructions()}
)

chain3 = model2 | prompt3 | json_output_parser
chain3.invoke({"query": "France?"})

