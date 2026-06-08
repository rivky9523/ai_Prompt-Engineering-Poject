import gradio as gr
import os
import subprocess # הוספנו את זה כדי שנוכל להריץ פקודות במחשב
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# הוספנו רק את חוק מספר 5 כדי למנוע המצאת פקודות בשיחות סרק
SYSTEM_PROMPT = """
You are a Windows CLI expert. Return ONLY the command.

RULES:
1. FORBIDDEN COMMANDS: If the user asks for 'format' or 'shutdown', return: "BLOCKED: Forbidden dangerous command."
2. RISK ASSESSMENT: If the user asks to delete (del) or modify files (ren/move), you must wrap the command like this: "REQUIRES_USER_CONFIRMATION: [the command]".
3. SAFE COMMANDS: For any other command (dir, ipconfig, cls, etc.), return ONLY the raw command string.
4. NO EXPLANATIONS: Strictly no text other than the command or the security messages above.
5. OUT OF SCOPE: If the user asks a conversational question (like hello, how are you), return: "ERROR: Not a system command."
"""

# הפונקציה המקורית שלך - נשארה ללא שום שינוי!
def translate_to_cli(user_input):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"שגיאה: {str(e)}"

# תוספת 1: פונקציה חדשה שמריצה את הפקודה ב-Docker
def run_and_get_output(user_input):
    # קורא לפונקציה המקורית שלך כדי לקבל את הפקודה
    cli_command = translate_to_cli(user_input)
    
    # בודק אם הפקודה בטוחה להרצה
    if "BLOCKED" in cli_command or "REQUIRES" in cli_command or "ERROR" in cli_command:
        sandbox_output = "❌ לא הורץ בגלל הגבלות בטיחות או פקודה לא חוקית."
    else:
        # מריץ את פקודת הבונוס ב-Docker
        try:
            result = subprocess.run(
                ["docker", "run", "--rm", "cli-sandbox", cli_command], 
                capture_output=True, text=True, timeout=10
            )
            sandbox_output = result.stdout if result.stdout else result.stderr
        except Exception as e:
            sandbox_output = f"שגיאת Sandbox: {str(e)}"
            
    # מחזיר גם את הפקודה וגם את התוצאה לממשק
    return cli_command, sandbox_output

# הממשק המקורי שלך - רק הוספנו לו פלט נוסף בשביל התוצאה
demo = gr.Interface(
    fn=run_and_get_output, # שינינו לפונקציה שעושה גם וגם
    inputs=gr.Textbox(label="מה תרצה לעשות? (עברית)"),
    outputs=[
        gr.Textbox(label="פקודת CLI"), 
        gr.Textbox(label="תוצאת הרצה מתוך ה-Docker Sandbox") # התווספה תיבה שנייה
    ],
    title="CLI Agent - Groq Version"
)

if __name__ == "__main__":
    demo.launch()