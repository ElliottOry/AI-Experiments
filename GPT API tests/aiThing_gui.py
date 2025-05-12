import tkinter as tk
from tkinter import scrolledtext, messagebox
from openai import OpenAI
import os
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Initialize OpenAI client (or set OPENAI_API_KEY in env)
api_key = os.getenv("OPENAI_API_KEY", "null")
client = OpenAI(api_key=api_key)

last_assistant_text = ""

def send_message():
        """Handle send button click: get user input, call API, update GUI."""
        user_input = input_field.get("1.0", tk.END).strip()
        if not user_input:
                return
        # Display user message
        conversation.configure(state='normal')
        conversation.insert(tk.END, f"You: {user_input}\n")
        conversation.configure(state='disabled')

        # Append to message history
        messages.append({"role": "user", "content": user_input})
        input_field.delete("1.0", tk.END)

        # Display assistant label
        conversation.configure(state='normal')
        conversation.insert(tk.END, "Assistant: ")
        conversation.configure(state='disabled')

        # Stream AI response
        assistant_text = ""
        try:
            stream = client.chat.completions.create(
                model="gpt-4o", messages=messages, stream=True
            )
            for chunk in stream:
                delta = chunk.choices[0].delta
                if delta.content:
                    assistant_text += delta.content
                    conversation.configure(state='normal')
                    conversation.insert(tk.END, delta.content)
                    conversation.configure(state='disabled')
                    conversation.yview(tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"OpenAI request failed: {e}")
            return

        # End the assistant line
        conversation.configure(state='normal')
        conversation.insert(tk.END, "\n")
        conversation.configure(state='disabled')

        # Save for LaTeX/raw viewing and history
        global last_assistant_text
        last_assistant_text = assistant_text
        messages.append({"role": "assistant", "content": assistant_text})

def view_latex():
    """Extract and render LaTeX segments from the last assistant response."""
    if not last_assistant_text.strip():
        messagebox.showinfo("No response", "There is no assistant response to display.")
        return
    # Extract LaTeX segments
    segments = []
    segments += re.findall(r"\$\$(.*?)\$\$", last_assistant_text, re.DOTALL)
    segments += re.findall(r"\\\[(.*?)\\\]", last_assistant_text, re.DOTALL)
    segments += re.findall(r"(?<!\$)\$(?!\$)([^$]+)\$(?!\$)", last_assistant_text)
    segments += re.findall(r"\\begin\{.*?\}.*?\\end\{.*?\}", last_assistant_text, re.DOTALL)
    if not segments:
        messagebox.showinfo("No LaTeX", "No LaTeX segments found in the response.")
        return
    # Create popup window to render LaTeX
    win = tk.Toplevel(root)
    win.title("LaTeX Viewer")
    # Build matplotlib figure to render math
    num = len(segments)
    fig = plt.Figure(figsize=(6, max(2, num * 0.8)))
    ax = fig.add_subplot(111)
    ax.axis('off')
    for idx, seg in enumerate(segments):
        y = 1 - (idx + 1) / (num + 1)
        ax.text(0.01, y, f"${seg.strip()}$", fontsize=16, va='center', ha='left')
    canvas = FigureCanvasTkAgg(fig, master=win)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

if __name__ == "__main__":
        messages = [{"role": "system", "content": "You are a helpful assistant."}]

        root = tk.Tk()
        root.title("AI Chat")

        conversation = scrolledtext.ScrolledText(root, state='disabled', wrap=tk.WORD)
        conversation.pack(padx=10, pady=10, expand=True, fill='both')

        input_field = tk.Text(root, height=3, wrap=tk.WORD)
        input_field.pack(padx=10, pady=(0,10), fill='x')

        button_frame = tk.Frame(root)
        button_frame.pack(padx=10, pady=(0,10), fill='x')
        send_btn = tk.Button(button_frame, text="Send", command=send_message)
        send_btn.pack(side=tk.LEFT)
        latex_btn = tk.Button(button_frame, text="View LaTeX", command=view_latex)
        latex_btn.pack(side=tk.LEFT, padx=(5,0))

        root.mainloop()
