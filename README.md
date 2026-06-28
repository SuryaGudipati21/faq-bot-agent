# FAQ Bot Agent

A simple AI agent that answers product-related questions using tool/function calling. The agent decides on its own whether a question needs a lookup (via a `search_faq` tool) or can be answered directly — built as part of the AI/ML course at iHub Vishlesan, IIT Tirupati.

## How It Works

1. The user asks a question.
2. The LLM decides whether the question is product-specific or general.
3. **If product-specific** → the agent calls the `search_faq` tool, retrieves the answer from a mock FAQ database, and generates a clear final response using that information.
4. **If general** → the agent answers directly without calling any tool.
5. **If no match is found** in the FAQ → the agent gracefully tells the user it couldn't find an answer, instead of making something up.

```
User Query → LLM Decision → [Tool Call: search_faq] or [Direct Answer] → Final Response
```

## Features

- Smart routing between tool-use and direct answering
- Keyword-based FAQ matching with a minimum overlap threshold (to reduce false matches)
- Graceful fallback when no FAQ entry matches
- Debug logging to show whether a tool was used for each query
- Simple CLI chat loop (type `exit` to quit)

## Tech Stack

- Python
- [Groq API](https://groq.com/) (OpenAI-compatible endpoint)
- OpenAI Python SDK (`openai`) for function/tool calling
- `python-dotenv` for environment variable management

## Setup

1. Clone the repo
   ```bash
   git clone https://github.com/<your-username>/faq-bot-agent.git
   cd faq-bot-agent
   ```

2. Install dependencies
   ```bash
   pip install openai python-dotenv
   ```

3. Create a `.env` file in the project root
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. Run the bot
   ```bash
   python faq_bot.py
   ```

## Example

```
You: Hi
[DEBUG] Answered directly, no tool used
Agent: Hello! How can I help you today?

You: How do I reset my password
[DEBUG] Tool call triggered
[DEBUG] Calling: search_faq({'query': 'reset password'})
[DEBUG] Tool result: Go to Settings > Account > Reset Password...
Agent: To reset your password, go to Settings > Account > Reset Password...
```

## Possible Improvements

- Replace keyword matching with TF-IDF or embedding-based similarity for better matching on paraphrased questions
- Support multiple tool calls per turn
- Connect to a real FAQ/knowledge base instead of a hardcoded dictionary
- Add unit tests for the routing logic

## Learnings

This project was a hands-on way to understand:
- How LLM tool/function calling works under the hood
- Designing an agent loop: query → model decision → tool execution (if needed) → final response
- Handling "no answer found" cases without letting the model hallucinate

## License

This project is for educational purposes as part of a course assignment.
