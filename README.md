Currency Converter with LLM Agents

This project implements a currency conversion system powered by two collaborating LLM-based agents.
One agent is responsible for mathematical calculations, while the other manages user interaction and response generation.

Features

🔄 Dual-Agent Architecture

Calculation Agent – Handles precise arithmetic operations, such as fetching exchange rates, performing multiplications/divisions, and returning accurate conversion results.

Conversation Agent – Parses user input, delegates computational tasks to the calculation agent, and generates user-friendly, natural language responses.

🧠 LLM-Powered Reasoning – Leverages large language models to interpret requests and produce coherent answers.

🧩 Modular Design – Clear separation of responsibilities between the computational logic and conversational layer.

✅ Extensible & Testable – Easy to extend for new currencies, data sources, or additional features.

Tech Stack

Language: Python

LLM Integration: OpenAI/other compatible LLM APIs

Core Modules:

CurrencyConversion_MathematicalCalculations.py – Business logic & numeric computations

currency_converter_agent.py – User interaction & orchestration

Example Usage
> Convert 150 USD to EUR
Agent: Fetching current exchange rate...
Agent: ✅ 150 USD ≈ 138.45 EUR

Key Learnings

Designing multi-agent systems using LLMs

Combining natural language understanding with deterministic calculations

Clean modular architecture and code readability

Handling real-world scenarios like currency rate lookups and edge cases
