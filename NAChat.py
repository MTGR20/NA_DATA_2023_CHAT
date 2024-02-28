from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader, LLMPredictor, ServiceContext, StorageContext, load_index_from_storage
# from langchain import OpenAI
from langchain_community.llms import OpenAI
# from langchain.chat_models import ChatOpenAI
# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
import gradio
import os
import setting

os.environ["OPENAI_API_KEY"] = setting.apiKeyChatGPT;


def construct_index(directory_path):

    num_outputs = 256 # 토큰 수 제한

    llm = ChatOpenAI(temperature=0.5, model_name="gpt-3.5-turbo", max_tokens=num_outputs)
    _llm_predictor = LLMPredictor(llm)
    service_context = ServiceContext.from_defaults(llm_predictor=_llm_predictor)
    docs = SimpleDirectoryReader(directory_path).load_data()
    index = GPTVectorStoreIndex.from_documents(docs, service_context=service_context)

    index.storage_context.persist(persist_dir="indexes") # index 저장 위치

    return index


def chatbot(input_text):
    
    storage_context = StorageContext.from_defaults(persist_dir="indexes") # storage context 재빌드
    query_engne = load_index_from_storage(storage_context).as_query_engine() # storage_context를 이용해 index 로드 

    response = query_engne.query(input_text)

    return response.response




# 데이터가 추가로 업데이트 되었을 경우만 학습(인덱스 생성)
# index = construct_index("trainingData")

# inputs = "Where will I stay during my time in regensburg?"
inputs = "IAEA는 뭐하는 곳이야?"
outputs = chatbot(inputs)
print(outputs)

# 제공되지 않은 정보에 대한 답변 처리하기




# # Creating the web UIusing gradio
# iface = gradio.Interface(fn=chatbot,
#                          inputs=gradio.inputs.Textbox(lines=5, label="Enter your question here"),
#                          outputs="text",
#                          title="Custom-trained AI Chatbot")
#
# # Constructing indexes based on the documents in traininData folder
# # This can be skipped if you have already trained your app and need to re-run it
# index = construct_index("trainingData")
#
# # launching the web UI using gradio
# iface.launch(share=True)