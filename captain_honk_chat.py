"""
captain_honk_chat.py
Interactive CLI Chatbot for Captain Honk using GroqCloud API.

Session Memory Rules:
1. Loads system prompt context from 'captain_honk_context.txt'.
2. Maintains conversation history in memory ONLY during the active runtime loop.
3. Remembers what the child says during the chat (e.g. name, preferences).
4. Clears all session memory when the script exits (no persistent logs saved).
"""

import os
import sys
from groq import Groq

CONTEXT_FILE = "captain_honk_context.txt"

def load_context(filepath=CONTEXT_FILE):
    """Reads the system prompt and examples from the context file."""
    if not os.path.exists(filepath):
        print(f"Error: Context file '{filepath}' not found.")
        print("Please run setup_context.py first!")
        sys.exit(1)
    
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def main():
    # Initialize Groq client
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY environment variable not set.")
        print("Set it using: export GROQ_API_KEY='your_api_key_here'")
        sys.exit(1)
    
    client = Groq(api_key=api_key)
    
    # 1. Read static system prompt from context file
    system_prompt = load_context()
    
    # 2. In-memory session history initialization
    # Session memory lives in this list only during execution.
    messages = [
        {"role": "system", "content": system_prompt}
    ]
    
    print("=" * 60)
    print("  🦆 Welcome to Captain Honk's Interactive Chat! 🦆")
    print("  Type 'quit' or 'exit' to end the session.")
    print("  (All chat memory will be wiped when this session ends.)")
    print("=" * 60)
    print("\nCaptain Honk: Hello friend! I am Captain Honk! What is your name? honk honk\n")
    
    while True:
        try:
            user_input = input("Child: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ["quit", "exit", "bye", "goodbye"]:
                print("\nCaptain Honk: Goodbye friend! It was so fun talking to you! Have a quack-tastic day! honk honk")
                break
            
            # Append user message to active session memory
            messages.append({"role": "user", "content": user_input})
            
            # Request response from GroqCloud API
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages,
                temperature=0.7,
                max_tokens=300,
            )
            
            bot_reply = completion.choices[0].message.content
            
            # Print response
            print(f"\nCaptain Honk: {bot_reply}\n")
            
            # Append assistant response to active session memory
            messages.append({"role": "assistant", "content": bot_reply})
            
        except KeyboardInterrupt:
            print("\n\nSession interrupted by user.")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}\n")
            break
            
    print("\n[Session Ended: Conversation memory wiped clean. System reset to original context.]")

if __name__ == "__main__":
    main()
