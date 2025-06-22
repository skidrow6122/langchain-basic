import os
import warnings
warnings.filterwarnings("ignore")
from dotenv import load_dotenv
load_dotenv()

# default promptTemplate test
from langchain.prompts import PromptTemplate
prompt = (
    PromptTemplate.from_template(
        """
        You are a highly skilled software architecture.
        Please describe the software architecture in detail for {field}.
        And, please recommend a software architecture for the following software stacks.
        <SW stack>
        {SW_stack}
        """
    )
)

prompt #print
prompt.invoke({"field": "Backend", "SW_stack": "MySQL, MongoDB, Springboot"}) # excution with parameter injection
# StringPromptValue 내부에 파라미터를 string 으로 받아서 완성 & 전달

# prompt usecase with using langchain library ChatPromptTemplate test
from langchain_core.prompts import ChatPromptTemplate
chat_template = ChatPromptTemplate.from_messages(
    [
    # SystemMessage - define the role and name
        ("system", "You are a highly skilled software architecture. Your name is {name}"),
    # HumanMessage - inject conversation pattern
        ("human", "Hi. How`s it going?"),
        ("ai", "Everything is fine. thanks!"),
    # send user input via HumanMessage
        ("human", "{user_input}")
    ]
)

messages = chat_template.format_messages(name="Teddy", user_input="What is your name?")
print(messages)