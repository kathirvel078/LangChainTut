import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"

# -------------------------------
# INPUT GUARDRAILS
# -------------------------------

BLOCKED_WORDS = [
    "hack",
    "virus",
    "malware",
    "steal passwords"
]


def input_guardrail(user_prompt):
    """
    Check if prompt contains blocked words
    """

    for word in BLOCKED_WORDS:
        if word.lower() in user_prompt.lower():
            return False

    return True


# -------------------------------
# OLLAMA CALL
# -------------------------------

def call_ollama(prompt):

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    return response.json()["response"]


# -------------------------------
# OUTPUT GUARDRAILS
# -------------------------------

def output_guardrail(response):
    """
    Simple output validation
    """

    blocked_output = [
        "password",
        "credit card",
        "ssn"
    ]

    for word in blocked_output:
        if word.lower() in response.lower():
            return False

    return True


# -------------------------------
# MAIN APP
# -------------------------------

def main():

    user_prompt = input("Enter your prompt: ")

    # STEP 1: INPUT VALIDATION
    if not input_guardrail(user_prompt):
        print("\n❌ BLOCKED BY INPUT GUARDRAIL")
        return

    print("\n✅ Input passed guardrail")

    # STEP 2: LLM CALL
    ai_response = call_ollama(user_prompt)

    print("\n🤖 AI RESPONSE:\n")
    print(ai_response)

    # STEP 3: OUTPUT VALIDATION
    if not output_guardrail(ai_response):
        print("\n❌ OUTPUT BLOCKED BY GUARDRAIL")
        return

    print("\n✅ OUTPUT PASSED GUARDRAIL")
    print("\n🎉 FINAL SAFE RESPONSE:\n")
    print(ai_response)


if __name__ == "__main__":
    main()