import os
import warnings

warnings.filterwarnings("ignore")
from dotenv import load_dotenv
load_dotenv()

# RunnablePassThrough : 주어진 텍스트, 객체를 그대로 통과시킴
from langchain_core.runnables import RunnablePassthrough
RunnablePassthrough().invoke("Hi")
RunnablePassthrough.assign(multi=lambda x: x["num"]*3).invoke({"num": 3})
# -> {'num' : 3, 'multi' : 9}

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
prompt = ChatPromptTemplate.from_template("""please translate this sentence to french. {sentence}
French translation: (print from here)""")
model = ChatOpenAI(model="gpt-4o-mini")
output_parser = StrOutputParser()
runnable_chain = {"sentence": RunnablePassthrough()} | prompt | model | output_parser
runnable_chain.invoke({"sentence": "thank you so much"})


# RunnableParallel : 주어진 여러개의 실행로직들을 병렬적으로 실행한다
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
runnable = RunnableParallel(
    extra = RunnablePassthrough.assign(multi=lambda x: x["num"]*3),
    modified=lambda x: x["num"] + 1,
)
runnable.invoke({"num": 1})
#-> {'extra' : {'num' : 1, 'multi' : 3}, 'modified' : 2}


# RunnableLambda : 사용자가 정의한 임의의 함수에 runnable 객체의 기능을 넣어 주는 것
from langchain_core.runnables import RunnableLambda
def add_smile(x):
    return x + " ^^"
add_smile_runnable = RunnableLambda(add_smile)

from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
prompt_str = "please explain about {topic} in 3 sentences"
prompt = ChatPromptTemplate.from_template(prompt_str)
model = ChatOpenAI(model="gpt-4o-mini")
output_parser = StrOutputParser()
runnable_chain2 = prompt | model | output_parser

def add_thank(x):
    return x + " thank you !!"
add_thank_runnable = RunnableLambda(add_thank)
runnable_chain3 = prompt | model | output_parser | add_thank_runnable
runnable_chain3.invoke("baseball")

# Runnable 복합활용
runnable_complex = RunnableParallel(
    passed=RunnablePassthrough(),
    modified=add_thank_runnable
)
runnable_complex.invoke("Hi")
#-> {'passed' : 'Hi', 'modified' : 'Hi thank you !!'}

# Runnable 복합활용 실전
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser

model_final = ChatOpenAI(model="gpt-4o-mini", max_tokens=128, temperature=0)
history_prompt = ChatPromptTemplate.from_template("{topic} 이 무엇의 약자인가?")
celeb_prompt = ChatPromptTemplate.from_template("{topic} 분야의 유명인사 3명의 이름만 알려줘.")
output_parser = StrOutputParser()

history_chain = history_prompt | model_final | output_parser
celeb_chain = celeb_prompt | model_final | output_parser

map_chain = RunnableParallel(
    history=history_chain,
    celeb=celeb_chain
)
result = map_chain.invoke({"topic": "AI"})
print(result)