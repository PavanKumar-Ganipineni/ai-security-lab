from flask import Flask, request, jsonify, render_template
import requests
import json
import logging
from config import OLLAMA_BASE_URL, OLLAMA_MODEL, SYSTEM_PROMPT, MAX_TOKENS, TEMPERATURE
from tools import execute_tool

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
conversation_history = []

def call_ollama(messages: list) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
        "options": {"temperature": TEMPERATURE, "num_predict": MAX_TOKENS}
    }
    try:
        response = requests.post(f"{OLLAMA_BASE_URL}/api/chat", json=payload, timeout=60)
        response.raise_for_status()
        return response.json()["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error: Could not reach LLM — {str(e)}"

def parse_tool_call(response_text: str) -> tuple:
    if "TOOL_CALL:" in response_text:
        try:
            tool_json_str = response_text.split("TOOL_CALL:")[1].strip()
            tool_call = json.loads(tool_json_str)
            return tool_call.get("tool"), tool_call.get("params", {})
        except (json.JSONDecodeError, IndexError):
            pass
    return None, None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "message field required"}), 400
    user_message = data["message"]
    logging.info(f"USER INPUT: {user_message}")
    conversation_history.append({"role": "user", "content": user_message})
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history
    response_text = call_ollama(messages)
    tool_name, tool_params = parse_tool_call(response_text)
    tool_result = None
    if tool_name:
        logging.info(f"TOOL CALL: {tool_name} with params {tool_params}")
        tool_result = execute_tool(tool_name, tool_params)
        messages.append({"role": "assistant", "content": response_text})
        messages.append({"role": "user", "content": f"TOOL_RESULT: {json.dumps(tool_result)}"})
        response_text = call_ollama(messages)
    conversation_history.append({"role": "assistant", "content": response_text})
    logging.info(f"LLM RESPONSE: {response_text}")
    return jsonify({
        "response": response_text,
        "tool_called": tool_name,
        "tool_result": tool_result,
        "debug": {"model": OLLAMA_MODEL, "history_length": len(conversation_history)}
    })

@app.route("/reset", methods=["POST"])
def reset():
    global conversation_history
    conversation_history = []
    return jsonify({"status": "conversation reset"})

@app.route("/history", methods=["GET"])
def history():
    return jsonify({"history": conversation_history})

if __name__ == "__main__":
    print("\n" + "="*60)
    print("VulnFinBot — Deliberately Vulnerable LLM Application")
    print("FOR EDUCATIONAL PURPOSES ONLY")
    print("="*60 + "\n")
    app.run(debug=True, host="0.0.0.0", port=5001)
