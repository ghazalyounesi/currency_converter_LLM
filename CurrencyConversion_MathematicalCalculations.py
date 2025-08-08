from langgraph.prebuilt import create_react_agent
from langchain_core.tools import StructuredTool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
import requests

class CurrencyInput(BaseModel):
    amount: float = Field(..., description="Amount to convert")
    source: str = Field(..., description="Source currency in ISO code (e.g., USD, EUR)")
    target: str = Field(..., description="Target currency in ISO code (e.g., USD, EUR)")

class CurrencyOutput(BaseModel):
    converted_amount: float = Field(..., description="Converted amount in target currency")

def currency_tool_fn(amount: float, source: str, target: str) -> CurrencyOutput:
    url = f"https://api.frankfurter.app/latest?amount={amount}&from={source}&to={target}"
    resp = requests.get(url).json()
    rate = resp.get("rates", {}).get(target.upper())
    if rate is None:
        raise ValueError(f"Rate for {target} not found.")
    print(f"💱 Currency conversion: {amount} {source} → {rate} {target}")
    return CurrencyOutput(converted_amount=rate)

currency_tool = StructuredTool.from_function(
    func=currency_tool_fn,
    args_schema=CurrencyInput,
    return_schema=CurrencyOutput,
    name="currency_tool",
    description="Convert an amount from one currency to another."
)

class MathInput(BaseModel):
    expression: str = Field(..., description="Math expression to evaluate (e.g., '250 - 10')")

class MathOutput(BaseModel):
    result: float = Field(..., description="Result of the calculation")

def math_tool_fn(expression: str) -> MathOutput:
    try:
        value = eval(expression)
        print(f"🧮 Math calculation: {expression} = {value}")
        return MathOutput(result=float(value))
    except Exception as e:
        raise ValueError(f"Math error: {e}")

math_tool = StructuredTool.from_function(
    func=math_tool_fn,
    args_schema=MathInput,
    return_schema=MathOutput,
    name="math_tool",
    description="Perform a math calculation."
)

class RatioInput(BaseModel):
    value1: float = Field(..., description="First numeric value")
    value2: float = Field(..., description="Second numeric value to divide by")

class RatioOutput(BaseModel):
    ratio: float = Field(..., description="value1 / value2")

def ratio_tool_fn(value1: float, value2: float) -> RatioOutput:
    if value2 == 0:
        raise ValueError("Division by zero is not allowed.")
    ratio = value1 / value2
    print(f"📊 Ratio calculation: {value1} / {value2} = {ratio}")
    return RatioOutput(ratio=ratio)

ratio_tool = StructuredTool.from_function(
    func=ratio_tool_fn,
    args_schema=RatioInput,
    return_schema=RatioOutput,
    name="ratio_tool",
    description="Calculate the ratio of two values."
)

llm = ChatOpenAI(
    model="gpt-4o-mini",
    openai_api_key="aa-Nr1dmDUOmUX4clYkp0mIogkPStDlAOXLJHZbPe4KdK4fEiIX",
    openai_api_base="https://api.avalai.ir/v1"
)

agent = create_react_agent(
    llm,
    tools=[currency_tool, math_tool, ratio_tool]
)

if __name__ == "__main__":
    user_input = input("💬 Enter your question:\n> ")
    result = agent.invoke({"messages": [{"role": "user", "content": user_input}]})

    messages = result.get("messages", [])
    for m in messages:
        if hasattr(m, "content") and m.content:
            print("\nAgent Answer:", m.content)
