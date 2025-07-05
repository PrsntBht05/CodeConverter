import tkinter as tk
from tkinter import ttk
from lexer import Lexer, Token
from my_parser import Parser
from codegen import CodeGenerator
from typing import List
import tkinter as tk
from tkinter import ttk
from lexer import Lexer, Token
from my_parser import Parser
from codegen import CodeGenerator
from typing import List
import pyperclip

class ConverterGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("C++ to Python Converter")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        # Main frame
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Input section
        self.input_label = ttk.Label(self.main_frame, text="C++ Code", font=("Helvetica", 12, "bold"))
        self.input_label.pack(anchor="w", pady=5)

        self.input_text = tk.Text(self.main_frame, height=10, width=50, font=("Consolas", 11), wrap="none", bd=2, relief="groove")
        self.input_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.input_scroll = ttk.Scrollbar(self.main_frame, orient=tk.HORIZONTAL, command=self.input_text.xview)
        self.input_scroll.pack(fill=tk.X, padx=5)
        self.input_text.configure(xscrollcommand=self.input_scroll.set)

        # Syntax highlighting tags
        self.input_text.tag_configure("keyword", foreground="blue")
        self.input_text.tag_configure("number", foreground="green")
        self.input_text.tag_configure("operator", foreground="purple")
        self.input_text.tag_configure("identifier", foreground="black")
        self.input_text.bind("<KeyRelease>", self.highlight_syntax)

        # Button frame
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=10)

        self.convert_button = ttk.Button(self.button_frame, text="Convert", style="TButton", command=self.convert)
        self.convert_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ttk.Button(self.button_frame, text="Clear", style="TButton", command=self.clear)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.copy_button = ttk.Button(self.button_frame, text="Copy Output", style="TButton", command=self.copy_to_clipboard)
        self.copy_button.pack(side=tk.LEFT, padx=5)

        # Output section
        self.output_label = ttk.Label(self.main_frame, text="Python Code", font=("Helvetica", 12, "bold"))
        self.output_label.pack(anchor="w", pady=5)

        self.output_text = tk.Text(self.main_frame, height=10, width=50, font=("Consolas", 11), wrap="none", bd=2, relief="groove", state="disabled")
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.output_scroll = ttk.Scrollbar(self.main_frame, orient=tk.HORIZONTAL, command=self.output_text.xview)
        self.output_scroll.pack(fill=tk.X, padx=5)
        self.output_text.configure(xscrollcommand=self.output_scroll.set)

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = ttk.Label(self.main_frame, textvariable=self.status_var, background="#e0e0e0", relief="sunken", anchor="w", padding=5)
        self.status_bar.pack(fill=tk.X, pady=5)

        # Configure ttk button style
        style = ttk.Style()
        style.configure("TButton", padding=5, font=("Arial", 10))

    def highlight_syntax(self, event=None):
        """Apply syntax highlighting to C++ input."""
        self.input_text.tag_remove("keyword", "1.0", tk.END)
        self.input_text.tag_remove("number", "1.0", tk.END)
        self.input_text.tag_remove("operator", "1.0", tk.END)
        self.input_text.tag_remove("identifier", "1.0", tk.END)

        code = self.input_text.get("1.0", tk.END).strip()
        if not code:
            return

        try:
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            for token in tokens:
                start_idx = "1.0"
                while True:
                    start_pos = self.input_text.search(token.value, start_idx, tk.END)
                    if not start_pos:
                        break
                    end_pos = f"{start_pos}+{len(token.value)}c"
                    if token.type == "KEYWORD":
                        self.input_text.tag_add("keyword", start_pos, end_pos)
                    elif token.type == "NUMBER":
                        self.input_text.tag_add("number", start_pos, end_pos)
                    elif token.type == "OP":
                        self.input_text.tag_add("operator", start_pos, end_pos)
                    elif token.type == "ID":
                        self.input_text.tag_add("identifier", start_pos, end_pos)
                    start_idx = end_pos
        except Exception as e:
            self.status_var.set(f"Syntax Highlight Error: {str(e)}")

    def convert(self):
        """Convert C++ to Python."""
        try:
            cpp_code = self.input_text.get("1.0", tk.END).strip()
            if not cpp_code:
                self.status_var.set("Error: Input is empty")
                return
            lexer = Lexer(cpp_code)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            ast = parser.parse()
            codegen = CodeGenerator()
            python_code = codegen.generate(ast)
            self.output_text.configure(state="normal")
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, python_code)
            self.output_text.configure(state="disabled")
            self.status_var.set("Conversion successful")
        except Exception as e:
            self.output_text.configure(state="normal")
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, f"Error: {str(e)}")
            self.output_text.configure(state="disabled")
            self.status_var.set(f"Error: {str(e)}")

    def clear(self):
        """Clear input and output."""
        self.input_text.delete("1.0", tk.END)
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.configure(state="disabled")
        self.status_var.set("Cleared")

    def copy_to_clipboard(self):
        """Copy output to clipboard."""
        python_code = self.output_text.get("1.0", tk.END).strip()
        if python_code:
            pyperclip.copy(python_code)
            self.status_var.set("Output copied to clipboard")
        else:
            self.status_var.set("Error: No output to copy")
class ConverterGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("C++ to Python Converter")
        self.root.geometry("900x700")
        self.root.configure(bg="#e6f3ff")  # Soft blue background

        # Main frame
        self.main_frame = ttk.Frame(self.root, padding=15, style="Main.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Input section
        self.input_frame = ttk.Frame(self.main_frame, style="Input.TFrame")
        self.input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.input_label = ttk.Label(self.input_frame, text="C++ Code", font=("Helvetica", 14, "bold"), foreground="#283593")
        self.input_label.pack(anchor="w", pady=5)

        self.input_text = tk.Text(self.input_frame, height=12, width=60, font=("Consolas", 12), wrap="none", bd=2, relief="groove", bg="#ffffff")
        self.input_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.input_scroll = ttk.Scrollbar(self.input_frame, orient=tk.HORIZONTAL, command=self.input_text.xview)
        self.input_scroll.pack(fill=tk.X, padx=5)
        self.input_text.configure(xscrollcommand=self.input_scroll.set)

        # Syntax highlighting tags
        self.input_text.tag_configure("keyword", foreground="#d81b60")  # Pink
        self.input_text.tag_configure("number", foreground="#388e3c")   # Green
        self.input_text.tag_configure("operator", foreground="#6a1b9a") # Purple
        self.input_text.tag_configure("identifier", foreground="#0288d1") # Blue
        self.input_text.bind("<KeyRelease>", self.highlight_syntax)

        # Button frame
        self.button_frame = ttk.Frame(self.main_frame, style="Main.TFrame")
        self.button_frame.pack(fill=tk.X, pady=15)

        self.convert_button = tk.Button(self.button_frame, text="Convert", font=("Arial", 12), bg="#1976d2", fg="white", relief="flat", command=self.convert)
        self.convert_button.pack(side=tk.LEFT, padx=10)
        self.convert_button.bind("<Enter>", lambda e: self.convert_button.config(bg="#42a5f5"))
        self.convert_button.bind("<Leave>", lambda e: self.convert_button.config(bg="#1976d2"))

        self.clear_button = tk.Button(self.button_frame, text="Clear", font=("Arial", 12), bg="#ff5722", fg="white", relief="flat", command=self.clear)
        self.clear_button.pack(side=tk.LEFT, padx=10)
        self.clear_button.bind("<Enter>", lambda e: self.clear_button.config(bg="#ff8a65"))
        self.clear_button.bind("<Leave>", lambda e: self.clear_button.config(bg="#ff5722"))

        # Output section
        self.output_frame = ttk.Frame(self.main_frame, style="Output.TFrame")
        self.output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.output_label = ttk.Label(self.output_frame, text="Python Code", font=("Helvetica", 14, "bold"), foreground="#283593")
        self.output_label.pack(anchor="w", pady=5)

        self.output_text = tk.Text(self.output_frame, height=12, width=60, font=("Consolas", 12), wrap="none", bd=2, relief="groove", bg="#ffffff", state="disabled")
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.output_scroll = ttk.Scrollbar(self.output_frame, orient=tk.HORIZONTAL, command=self.output_text.xview)
        self.output_scroll.pack(fill=tk.X, padx=5)
        self.output_text.configure(xscrollcommand=self.output_scroll.set)

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = ttk.Label(self.main_frame, textvariable=self.status_var, style="Status.TLabel", anchor="w", padding=8)
        self.status_bar.pack(fill=tk.X, pady=10)

        # Configure styles
        style = ttk.Style()
        style.configure("Main.TFrame", background="#e6f3ff")  # Soft blue
        style.configure("Input.TFrame", background="#f3e6ff")  # Light purple
        style.configure("Output.TFrame", background="#e6ffe6")  # Light green
        style.configure("Status.TLabel", background="#0288d1", foreground="white", font=("Arial", 10))  # Blue

    def highlight_syntax(self, event=None):
        """Apply syntax highlighting to C++ input."""
        self.input_text.tag_remove("keyword", "1.0", tk.END)
        self.input_text.tag_remove("number", "1.0", tk.END)
        self.input_text.tag_remove("operator", "1.0", tk.END)
        self.input_text.tag_remove("identifier", "1.0", tk.END)

        code = self.input_text.get("1.0", tk.END).strip()
        if not code:
            return

        try:
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            for token in tokens:
                start_idx = "1.0"
                while True:
                    start_pos = self.input_text.search(token.value, start_idx, tk.END)
                    if not start_pos:
                        break
                    end_pos = f"{start_pos}+{len(token.value)}c"
                    if token.type == "KEYWORD":
                        self.input_text.tag_add("keyword", start_pos, end_pos)
                    elif token.type == "NUMBER":
                        self.input_text.tag_add("number", start_pos, end_pos)
                    elif token.type == "OP":
                        self.input_text.tag_add("operator", start_pos, end_pos)
                    elif token.type == "ID":
                        self.input_text.tag_add("identifier", start_pos, end_pos)
                    start_idx = end_pos
        except Exception as e:
            self.status_var.set(f"Syntax Highlight Error: {str(e)}")
            self.status_bar.configure(style="Error.TLabel")

    def convert(self):
        """Convert C++ to Python."""
        try:
            cpp_code = self.input_text.get("1.0", tk.END).strip()
            if not cpp_code:
                self.status_var.set("Error: Input is empty")
                self.status_bar.configure(style="Error.TLabel")
                return
            lexer = Lexer(cpp_code)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            ast = parser.parse()
            codegen = CodeGenerator()
            python_code = codegen.generate(ast)
            self.output_text.configure(state="normal")
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, python_code)
            self.output_text.configure(state="disabled")
            self.status_var.set("Conversion successful")
            self.status_bar.configure(style="Success.TLabel")
        except Exception as e:
            self.output_text.configure(state="normal")
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, f"Error: {str(e)}")
            self.output_text.configure(state="disabled")
            self.status_var.set(f"Error: {str(e)}")
            self.status_bar.configure(style="Error.TLabel")

    def clear(self):
        """Clear input and output."""
        self.input_text.delete("1.0", tk.END)
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.configure(state="disabled")
        self.status_var.set("Cleared")
        self.status_bar.configure(style="Status.TLabel")

    def run(self):
        # Configure additional styles for status bar
        style = ttk.Style()
        style.configure("Success.TLabel", background="#4caf50", foreground="white", font=("Arial", 10))  # Green
        style.configure("Error.TLabel", background="#d32f2f", foreground="white", font=("Arial", 10))    # Red
        self.root.mainloop()