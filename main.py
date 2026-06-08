import gradio as gr
import os
from groq import Groq # שינינו ל-Groq
from dotenv import load_dotenv

load_dotenv()
# הגדרת הלקוח של Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are a Windows CLI expert. Return ONLY the command.

RULES:
1. FORBIDDEN COMMANDS: If the user asks for 'format' or 'shutdown', return: "BLOCKED: Forbidden dangerous command."
2. RISK ASSESSMENT: If the user asks to delete (del) or modify files (ren/move), you must wrap the command like this: "REQUIRES_USER_CONFIRMATION: [the command]".
3. SAFE COMMANDS: For any other command (dir, ipconfig, cls, etc.), return ONLY the raw command string.
4. NO EXPLANATIONS: Strictly no text other than the command or the security messages above.
"""

def translate_to_cli(user_input):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile", # מודל חזק וחינמי של Groq
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"שגיאה: {str(e)}"

demo = gr.Interface(
    fn=translate_to_cli,
    inputs=gr.Textbox(label="מה תרצה לעשות? (עברית)"),
    outputs=gr.Textbox(label="פקודת CLI"),
    title="CLI Agent - Groq Version"
)

if __name__ == "__main__":
    demo.launch()