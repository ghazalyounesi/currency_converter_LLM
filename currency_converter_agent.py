from langgraph.graph import StateGraph, END  
from langchain_core.runnables import RunnableLambda  
from langchain_openai import ChatOpenAI  
import requests 
import json 
import re  

llm = ChatOpenAI(
    model="gpt-4o",  
    openai_api_key="aa-19AnaH7P8winIlKZgIQrMyBHQbHpn6dYOhmHfCcS2DRc33NY",  
    openai_api_base="https://api.avalai.ir/v1",  
)

def extract_currency_info(input: dict) -> dict:
    user_input = input.get("user_input")  

    prompt = f"""
You are a currency conversion assistant.

Extract the amount, source currency, and target currency from this user request:
"{user_input}"

Return the result in **standard ISO currency codes** (e.g., USD, EUR, IRR, GBP).

If the user uses local or informal currency names (like 'toman', 'rial', 'lira', 'rupee', etc.), convert them to their correct ISO currency codes.

Return a JSON in this exact format:
{{
  "amount": 100,
  "source": "USD",
  "target": "EUR"
}}

Examples of informal to ISO currency mappings:
- toman → IRR
- rial → IRR
- dollar → USD
- euro → EUR
- pound → GBP
- yen → JPY
- rupee → INR
- lira → TRY

"""

    response = llm.invoke(prompt)
    raw_output = response.content.strip()  

    json_match = re.search(r"{\s*\"amount\".*?}", raw_output, re.DOTALL)
    if not json_match:
       raise ValueError("Model response is not valid JSON:\n" + raw_output)

    clean_output = json_match.group(0)
    try:
        print("Raw model response:", raw_output)
        print("clean code:  ",clean_output)
        info = json.loads(clean_output)
    except json.JSONDecodeError:
        raise ValueError("Model response is not valid JSON:\n" + raw_output)

    return {**input, **info}


def fetch_conversion(input: dict) -> dict:
    url = f"https://api.frankfurter.app/latest?amount={input['amount']}&from={input['source']}&to={input['target']}"
    
    try:
        response = requests.get(url).json()
        print(" Conversion API response:", response)

        target_currency = input["target"].upper()
        rate = response.get("rates", {}).get(target_currency)

        if rate is not None:
            input["result"] = rate
        else:
            input["result"] = None
            input["error"] = f"Rate for {target_currency} not found in response."
            
    except Exception as e:
        input["result"] = None
        input["error"] = f"Request failed: {str(e)}"

    return input

def build_final_answer(input: dict) -> str:
    if input.get("result") is None:
        return " Failed to retrieve the conversion rate. Please check the input currencies or try again later."

    return f"{input['amount']} {input['source']} is {input['result']:.2f} {input['target']} at this time."


builder = StateGraph(dict)  

builder.add_node("extract", RunnableLambda(extract_currency_info))  
builder.add_node("convert", RunnableLambda(fetch_conversion))  
builder.add_node("respond", RunnableLambda(build_final_answer)) 

builder.set_entry_point("extract")  
builder.add_edge("extract", "convert")  
builder.add_edge("convert", "respond")  
builder.set_finish_point("respond")  
graph = builder.compile()

user_question = input("💬 Enter your question (e.g. 'How much Euro is 100 dollars?'):\n> ")

response = graph.invoke({"user_input": user_question})

print("\n Agent:", response)
