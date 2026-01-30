import tkinter as tk
from tkinter import ttk, font

ANSI_STYLES = {
    # Regular
    "Black":  {"code": "0;30", "fg": "#000000"},
    "Red":    {"code": "0;31", "fg": "#cc3333"},
    "Green":  {"code": "0;32", "fg": "#33cc33"},
    "Yellow": {"code": "0;33", "fg": "#cccc33"},
    "Blue":   {"code": "0;34", "fg": "#3366cc"},
    "Purple": {"code": "0;35", "fg": "#9933cc"},
    "Cyan":   {"code": "0;36", "fg": "#33cccc"},
    "White":  {"code": "0;37", "fg": "#eeeeee"},

    # Bold
    "Bold Black":  {"code": "1;30", "fg": "#555555"},
    "Bold Red":    {"code": "1;31", "fg": "#ff5555"},
    "Bold Green":  {"code": "1;32", "fg": "#55ff55"},
    "Bold Yellow": {"code": "1;33", "fg": "#ffff55"},
    "Bold Blue":   {"code": "1;34", "fg": "#5599ff"},
    "Bold Purple": {"code": "1;35", "fg": "#cc66ff"},
    "Bold Cyan":   {"code": "1;36", "fg": "#55ffff"},
    "Bold White":  {"code": "1;37", "fg": "#ffffff"},

    # Bright
    "Bright Black":  {"code": "0;90", "fg": "#777777"},
    "Bright Red":    {"code": "0;91", "fg": "#ff4444"},
    "Bright Green":  {"code": "0;92", "fg": "#44ff44"},
    "Bright Yellow": {"code": "0;93", "fg": "#ffff44"},
    "Bright Blue":   {"code": "0;94", "fg": "#4488ff"},
    "Bright Purple": {"code": "0;95", "fg": "#ff44ff"},
    "Bright Cyan":   {"code": "0;96", "fg": "#44ffff"},
    "Bright White":  {"code": "0;97", "fg": "#ffffff"},

    # Bold Bright
    "Bold Bright Black":  {"code": "1;90", "fg": "#999999"},
    "Bold Bright Red":    {"code": "1;91", "fg": "#ff6666"},
    "Bold Bright Green":  {"code": "1;92", "fg": "#66ff66"},
    "Bold Bright Yellow": {"code": "1;93", "fg": "#ffff66"},
    "Bold Bright Blue":   {"code": "1;94", "fg": "#66aaff"},
    "Bold Bright Purple": {"code": "1;95", "fg": "#ff66ff"},
    "Bold Bright Cyan":   {"code": "1;96", "fg": "#66ffff"},
    "Bold Bright White":  {"code": "1;97", "fg": "#ffffff"},
}

class PromptBuilder(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bash Prompt Builder")
        self.geometry("1000x550")
        self.configure(bg="#2d2d2d")
        
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        # Variables
        self.vars = {
            "user": tk.StringVar(value="Bold Green"),
            "host": tk.StringVar(value="Bold Green"),
            "sep_text": tk.StringVar(value="@"),
            "sep_color": tk.StringVar(value="White"),
            "path": tk.StringVar(value="Bold Blue"),
            "git": tk.StringVar(value="Bright Red"),
            "symbol_text": tk.StringVar(value="$"),
            "symbol_color": tk.StringVar(value="White"),
        }

        self.fonts = {
            "normal": font.Font(family="monospace", size=12),
            "bold": font.Font(family="monospace", size=12, weight="bold")
        }

        self.build_ui()
        self.update_output()

    def get_style_code(self, name):
        return ANSI_STYLES.get(name, ANSI_STYLES["White"])["code"]

    def build_ui(self):
        main_container = ttk.Frame(self, padding=20)
        main_container.pack(fill="both", expand=True)

        left_col = ttk.LabelFrame(main_container, text=" Configuration ", padding=10)
        left_col.pack(side="left", fill="y", padx=(0, 10))

        self.create_setting(left_col, "User Color", self.vars["user"])
        self.create_setting(left_col, "Separator Text", self.vars["sep_text"], is_entry=True)
        self.create_setting(left_col, "Separator Color", self.vars["sep_color"])
        self.create_setting(left_col, "Host Color", self.vars["host"])
        self.create_setting(left_col, "Path Color", self.vars["path"])
        self.create_setting(left_col, "Git Color", self.vars["git"])
        self.create_setting(left_col, "Symbol Text", self.vars["symbol_text"], is_entry=True)
        self.create_setting(left_col, "Symbol Color", self.vars["symbol_color"])

        right_col = ttk.Frame(main_container)
        right_col.pack(side="right", fill="both", expand=True)

        ttk.Label(right_col, text="Live Preview", font=("Arial", 10, "bold")).pack(anchor="w")
        self.preview_box = tk.Frame(right_col, bg="#1e1e1e", padx=10, pady=20, relief="sunken", bd=2)
        self.preview_box.pack(fill="x", pady=(5, 20))

        ttk.Label(right_col, text="Bash Script (Add to .bashrc)", font=("Arial", 10, "bold")).pack(anchor="w")
        self.code_out = tk.Text(right_col, height=15, bg="#252526", fg="#d4d4d4", 
                               insertbackground="white", font=("monospace", 10))
        self.code_out.pack(fill="both", expand=True)
        
        btn_frame = ttk.Frame(right_col)
        btn_frame.pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="📋 Copy Code", command=self.copy_code).pack(side="right")

    def create_setting(self, parent, label, var, is_entry=False):
        ttk.Label(parent, text=label).pack(anchor="w", pady=(5, 0))
        if is_entry:
            widget = ttk.Entry(parent, textvariable=var)
            widget.bind("<KeyRelease>", lambda e: self.update_output())
        else:
            widget = ttk.Combobox(parent, textvariable=var, values=list(ANSI_STYLES.keys()), state="readonly")
            widget.bind("<<ComboboxSelected>>", lambda e: self.update_output())
        widget.pack(fill="x", pady=(0, 5))

    def update_output(self):
        # Correctly mapping the dictionary variables to the Bash string
        bash = f"""function color_my_prompt {{
    local __user="\\[\\033[{self.get_style_code(self.vars['user'].get())}m\\]\\u"
    local __sep="\\[\\033[{self.get_style_code(self.vars['sep_color'].get())}m\\]{self.vars['sep_text'].get()}"
    local __host="\\[\\033[{self.get_style_code(self.vars['host'].get())}m\\]\\h"
    local __cur_location="\\[\\033[{self.get_style_code(self.vars['path'].get())}m\\]\\w"
    local __git_branch_color="\\[\\033[{self.get_style_code(self.vars['git'].get())}m\\]"
    local __git_branch='$(git branch 2>/dev/null | sed -n "s/^* \\(.*\\)$/ (\\1)/p")'
    local __prompt_tail="\\[\\033[{self.get_style_code(self.vars['symbol_color'].get())}m\\]{self.vars['symbol_text'].get()}"
    local __reset="\\[\\033[0m\\]"

    export PS1="$__user$__sep$__host $__cur_location$__git_branch_color$__git_branch $__prompt_tail$__reset "
}}
color_my_prompt
"""
        self.code_out.config(state="normal")
        self.code_out.delete("1.0", tk.END)
        self.code_out.insert(tk.END, bash)
        self.code_out.config(state="disabled")

        # Preview Logic
        for w in self.preview_box.winfo_children():
            w.destroy()

        def add_seg(text, style_name):
            style = ANSI_STYLES[style_name]
            is_bold = style["code"].startswith("1;")
            tk.Label(
                self.preview_box,
                text=text,
                fg=style["fg"],
                bg="#1e1e1e",
                font=self.fonts["bold"] if is_bold else self.fonts["normal"],
                padx=2,
            ).pack(side="left")

        add_seg("zyrotot", self.vars['user'].get())
        add_seg(self.vars['sep_text'].get(), self.vars['sep_color'].get())
        add_seg("debian ", self.vars['host'].get())
        add_seg("~/project ", self.vars['path'].get())
        add_seg("(my_branch) ", self.vars['git'].get())
        add_seg(self.vars['symbol_text'].get(), self.vars['symbol_color'].get())

    def copy_code(self):
        self.clipboard_clear()
        self.clipboard_append(self.code_out.get("1.0", "end-1c"))

if __name__ == "__main__":
    PromptBuilder().mainloop()