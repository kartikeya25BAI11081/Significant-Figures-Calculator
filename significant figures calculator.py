import tkinter as tk
from tkinter import ttk, messagebox
from math import log10, floor
def count_sig_figs(num_str: str) -> int:
    """Count significant figures following standard chemistry/physics rules."""
    s = num_str.strip().lower()
    if 'e' in s:
        s = s.split('e')[0] 
    if s and s[0] in '+-':
        s = s[1:]
    if not s or s == '.':
        return 0   
    sig_count = 0    
    if '.' in s:   
        for c in s:
            if c.isdigit():
                sig_count += 1
    else:
        started = False
        for c in s:
            if c.isdigit():
                if not started and c == '0':
                    continue
                sig_count += 1
                started = True 
    return sig_count
def round_sig_figs(x: float, n: int) -> float:
    """Round to n significant figures."""
    if x == 0 or n <= 0:
        return 0.0
    if n >= 16: 
        return x
    power = floor(log10(abs(x)))
    factor = 10 ** (power - n + 1)
    return round(x / factor) * factor
def decimals_after_point(num_str: str) -> int:
    """Count decimal places (least precise position)."""
    s = num_str.strip()
    if 'e' in s.lower():
        s = s.lower().split('e')[0]
    if '.' not in s:
        return 0
    decimal_part = s.split('.')[1]
    return len(decimal_part.rstrip('0'))
def calculate():
    a_str = entry_a.get().strip()
    b_str = entry_b.get().strip()
    op = op_var.get()
    try:
        a = float(a_str)
        b = float(b_str)
    except ValueError:
        messagebox.showerror("Error", "Enter valid numbers for A and B.")
        return
    try:
        if op == "+":
            raw = a + b
        elif op == "-":
            raw = a - b
        elif op == "×":
            raw = a * b
        elif op == "÷":
            raw = a / b
        else:
            messagebox.showerror("Error", "Select an operation.")
            return
    except ZeroDivisionError:
        messagebox.showerror("Error", "Division by zero.")
        return
    label_raw.config(text=f"Raw result: {raw:.12g}")
    sig_a = count_sig_figs(a_str)
    sig_b = count_sig_figs(b_str)
    if op in ["×", "÷"]:
        sig_result = min(sig_a, sig_b)
        if sig_result > 0:
            rounded = round_sig_figs(raw, sig_result)
            rule_text = (f"Rule: multiplication/division → "
                        f"minimum sig figs between inputs = {sig_result}")
            rounded_str = f"{rounded:.12g} (rounded to {sig_result} sig figs)"
        else:
            rounded = raw
            rule_text = "Rule: Invalid sig figs in inputs"
            rounded_str = str(rounded)
    else:
        dec_a = decimals_after_point(a_str)
        dec_b = decimals_after_point(b_str)
        min_dec = min(dec_a, dec_b)
        rounded = round(raw, min_dec)
        rule_text = f"Rule: addition/subtraction → min decimals = {min_dec}"
        rounded_str = f"{rounded:.12g} (rounded to {min_dec} decimals)"
    label_rule.config(text=rule_text)
    label_rounded.config(text=f"Rounded result: {rounded_str}")
root = tk.Tk()
root.title("Significant Figures Calculator")
main = ttk.Frame(root, padding="10 10 10 10")
main.grid(row=0, column=0, sticky="NSEW")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
ttk.Label(main, text="Number A:").grid(row=0, column=0, sticky="W")
entry_a = ttk.Entry(main, width=20)
entry_a.grid(row=0, column=1, pady=5)
ttk.Label(main, text="Number B:").grid(row=1, column=0, sticky="W")
entry_b = ttk.Entry(main, width=20)
entry_b.grid(row=1, column=1, pady=5)
ttk.Label(main, text="Operation:").grid(row=2, column=0, sticky="W")
op_var = tk.StringVar()
combo_op = ttk.Combobox(main, textvariable=op_var, state="readonly", width=5,
values=["+", "-", "×", "÷"])
combo_op.grid(row=2, column=1, sticky="W", pady=5)
combo_op.current(0)
btn = ttk.Button(main, text="Calculate", command=calculate)
btn.grid(row=3, column=0, columnspan=2, pady=10)
label_raw = ttk.Label(main, text="Raw result: ")
label_raw.grid(row=4, column=0, columnspan=2, sticky="W")
label_rule = ttk.Label(main, text="Rule: ")
label_rule.grid(row=5, column=0, columnspan=2, sticky="W")
label_rounded = ttk.Label(main, text="Rounded result: ")
label_rounded.grid(row=6, column=0, columnspan=2, sticky="W")
root.mainloop()