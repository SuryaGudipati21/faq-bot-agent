from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()
api_key = os.getenv("Groq_API_Key")
client = OpenAI(
    api_key = api_key,
    base_url = "https://api.groq.com/openai/v1"
)
model = "openai/gpt-oss-120b"
faq_database = {
    "reset_password": {
        "question": "How do I reset my password?",
        "answer": "Go to Settings > Account > Reset Password. You'll receive a reset link via email."
    },
    "warranty_period": {
        "question": "What is the warranty period for the SmartHome Hub?",
        "answer": "The SmartHome Hub comes with a 12-month limited warranty covering manufacturing defects."
    },
    "device_pairing": {
        "question": "How do I pair my device with the hub?",
        "answer": "Open the app, tap 'Add Device', and hold the pairing button on your hub for 5 seconds until the LED blinks blue."
    },
    "return_policy": {
        "question": "What is your return policy?",
        "answer": "You can return any unused product within 30 days of purchase for a full refund."
    },
    "wifi_issues": {
        "question": "Why won't my hub connect to WiFi?",
        "answer": "Ensure you're using a 2.4GHz network. Restart the hub by holding the power button for 10 seconds, then retry setup."
    },
    "firmware_update": {
        "question": "How do I update the firmware?",
        "answer": "Firmware updates are pushed automatically when your hub is connected to WiFi and plugged in. You can check the current version under Settings > About."
    },
    "subscription_cancel": {
        "question": "How do I cancel my subscription?",
        "answer": "Go to Settings > Subscription > Cancel Plan. Your plan remains active until the end of the billing cycle."
    },
    "supported_devices": {
        "question": "Which smart devices are compatible with the hub?",
        "answer": "The hub supports Zigbee, Z-Wave, and WiFi-based smart devices from major brands like Philips Hue, TP-Link, and Nest."
    }
}

def search_faq(query: str) -> str:
    query_lower = query.lower()
    
    best_score = 0
    best_match = None

    for entry in faq_database.values():
        question_lower = entry["question"].lower()

        score = sum(1 for word in query_lower.split() if word in question_lower)

        if score>best_score:
            best_score = score
            best_match = entry["answer"]
    return best_match if best_match and best_score>=2 else "Not Found"
            

tools = [
    {
        "type" : "function",
        "function" : {
            "name" : "search_faq",
            "description" : "Search the product FAQ database for an answer to a product-related question.",
            "parameters" : {
                "type" : "object",
                "properties" : {
                    "query" : {
                        "type" : "string",
                        "description" : "The user's question"
                    }
                },
                "required" : ["query"]
            }
        }
    }
]

available_tools = {"search_faq" : search_faq}

def run_agent(user_message : str):
    messages = [
        {"role" : "system", "content" : "You are a helpful assistant. use tools when needed."},
        {"role" : "user", "content" : user_message}
    ]
    response = client.chat.completions.create(
        model = model,
        tools = tools,
        messages = messages
    )

    if response.choices[0].finish_reason == "tool_calls":
        print("[DEBUG] Tool call triggered")
        message = response.choices[0].message
        tool_call = message.tool_calls[0]
        function = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(f"[DEBUG] Calling: {function}({arguments})")

        result = available_tools[function](**arguments)
        print(f"[DEBUG] Tool result: {result}")

        if result != "Not Found":
            messages.append({
                "role" : "assistant", 
                "content" : message.content,
                "tool_calls" : [
                    {
                        "id" : tool_call.id,
                        "type" : "function",
                        "function" : {
                            "name" : tool_call.function.name,
                            "arguments" : tool_call.function.arguments
                        }
                    }
                ]
            })
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })

            final_response = client.chat.completions.create(
                model = model,
                tools = tools,
                messages = messages
            )
            answer = final_response.choices[0].message.content
            print("Agent: ",answer)
        else:
            print("Agent: I couldn't find an answer to that in our FAQ. Please contact support for further assistance")
    else:
        print("[DEBUG] Answered directly, no tool used")
        answer = response.choices[0].message.content
        print("Agent: ",answer)

if __name__ == "__main__":
    print("===============FAQ BOT===============")
    print("Type 'exit' to quit.\n")
    while True:
        query = input("You: ")
        if query.lower() == "exit":
            print("Agent: Goodbye!")
            break
        run_agent(query)
        print("\n\n")