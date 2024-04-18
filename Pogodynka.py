import streamlit as st
from langchain.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain.chat_models import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain.utilities.dataforseo_api_search import DataForSeoAPIWrapper
from decouple import config
from langchain_core.messages import AIMessage, HumanMessage
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents import AgentExecutor
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
import os
import requests


os.environ["DATAFORSEO_LOGIN"] = config("DATAFORSEO_LOGIN")
os.environ["DATAFORSEO_PASSWORD"] = config("DATAFORSEO_PASSWORD")

model = ChatOpenAI(openai_api_key=config("OPENAI_API_KEY"))

prompt = ChatPromptTemplate.from_messages([("system",
    """Answer only to question abaut Polish weather in cities. If the question is not about weather in cities return only "Pytanie nie dotyczy pogody o Polskich miastach." \
        Use the provided context to answer the user question always more than one sentence.\
        your response should be in the language specified.\ 
        you should demostrate in your response. Of course, conversation histories that do not include the context contained in chat_history are also included.
        If you couldn't find information in context, weather has current information about the weather in cities in Poland.
       
    Language: {language}
    
    Human: {question}
    
    Context: {context}
    
    chat_history: {chat_history}
    
    weather:{weather}
    
    AI:"""),MessagesPlaceholder(variable_name="agent_scratchpad")])

question_creation_prompt = ChatPromptTemplate.from_messages([("system",
    """Your task is to create a question based on the question. If question does contain the name of the city, return the question you were asked.
    If the question does not contain the name of the city,
    check whether you can create a new question abaut weather in this city with its name based on chat_history and the question, for example the 
    question is "Will it be warmer tomorrow?"? Based on chat_history,
    you were able to deduce form chat_history that this is about Lublin, so you return for example "What's the weather like in Lublin?". 
    etc.Also analyze cases where questions compare weather in cities, e.g. Is will be hoter in Bydgoszcz?
    Then you also need to deduce from chat_history what city is being compared and return, for example, "What's the weather like in Bydgoszcz and Lublin".
    etc If you can't figure it out from the context, return the question you were asked. You create questions only in Polish. \ 
       
    Language: {language}
    
    Human: {question}
    
    chat_history: {chat_history}
    
    AI:"""),MessagesPlaceholder(variable_name="agent_scratchpad")])

tools = []

agent = (
    {
        "context": lambda x: x["context"],
        "agent_scratchpad": lambda x: format_to_openai_function_messages(x["intermediate_steps"]),
        "chat_history": lambda x: x["chat_history"],
        "question": lambda x: x["question"],
        "language": lambda x: x["language"],
        "weather": lambda x: x["weather"]
    }
    | prompt
    | model
    | OpenAIFunctionsAgentOutputParser()
)

repair_question_agent = (
    {
        "agent_scratchpad": lambda x: format_to_openai_function_messages(x["intermediate_steps"]),
        "chat_history": lambda x: x["chat_history"],
        "question": lambda x: x["question"],
        "language": lambda x: x["language"]
    }
    | question_creation_prompt
    | model
    | OpenAIFunctionsAgentOutputParser()
)

def generate_ai_reponse(
     user_prompt: str) -> str:
    try:
        
        history =""
        
        for message in st.session_state.chat_history:
            if isinstance(message, AIMessage):
                with st.chat_message("AI"):
                   history = history + message.content
                   
        repair_question_agent_executor = AgentExecutor(agent=repair_question_agent, tools=tools, verbose=True, handle_parsing_errors=True)
        
        response = repair_question_agent_executor.invoke({"question": user_prompt, "language": "Polish",  "chat_history":  history})
        
        json_wrapper = DataForSeoAPIWrapper(
            top_count=3,
            json_result_fields=["title", "description", "text"],
        )
        context = json_wrapper.results(response['output'])
        
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True,handle_parsing_errors=True)
        
        api_weather=get_data_from_weather_api()
        
        response = agent_executor.invoke(
            {"question": user_prompt, "context": context, "language": "Polish",  "chat_history":  history, "weather":api_weather})
        
        return response['output'], context
    except Exception as e:
        print(e)
        return "", {}

def get_data_from_weather_api():
    url="https://danepubliczne.imgw.pl/api/data/synop"
    response_API = requests.get(url)
    return response_API.text

search_history=""

user_prompt = st.chat_input("Tutaj wpisz swoje pytanie!")
st.title("Chat pogodowy")

if user_prompt is not None and user_prompt != "":
    ai_response, context = generate_ai_reponse(
                user_prompt=user_prompt,)
    if ai_response == "":
        ai_response="Błąd połączenia z internetem spróbuj zresetować aplikację"
    st.session_state.chat_history.append(HumanMessage(content=user_prompt))
    st.session_state.chat_history.append(AIMessage(content=ai_response))
    search_history=""
    if(ai_response!="Pytanie nie dotyczy pogody o Polskich miastach."):
        search_history=context
        
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Witaj jestem twoim virtualnym assystentem wiem wszystko na temat pogody śmiało pytaj!"),
    ]

for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)    
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)
            
js = f"""
<script>
    function scroll(dummy_var_to_force_repeat_execution){{
        var textAreas = parent.document.querySelectorAll('section.main');
        for (let index = 0; index < textAreas.length; index++) {{
            textAreas[index].style.color = 'red'
            textAreas[index].scrollTop = textAreas[index].scrollHeight;
        }}
    }}
    scroll({len(st.session_state.chat_history)})
</script>
"""


st.components.v1.html(js)