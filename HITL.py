import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"


def call_ollama(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    return response.json()["response"]


def human_in_the_loop(response):
    print("\n🤖 AI Response:\n")
    print(response)

    print("\n--- HUMAN REVIEW REQUIRED ---")
    decision = input("Approve (a) / Reject (r) / Edit (e): ").strip().lower()

    if decision == "a":
        return response

    elif decision == "r":
        return None

    elif decision == "e":
        edited = input("✏️ Enter your corrected response:\n")
        return edited

    else:
        print("Invalid choice. Auto-rejecting.")
        return None


def main():
    user_input = input("Enter your prompt: ")

    # Step 1: AI call
    ai_response = call_ollama(user_input)

    # Step 2: Human review
    final_output = human_in_the_loop(ai_response)

    # Step 3: Final result
    if final_output:
        print("\n✅ FINAL OUTPUT APPROVED:\n")
        print(final_output)
    else:
        print("\n❌ Response rejected by human.")


if __name__ == "__main__":
    main()