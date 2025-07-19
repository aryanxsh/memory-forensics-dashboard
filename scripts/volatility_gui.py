import os
import subprocess
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

# ============ Volatility Plugin List ============
plugins = [
    "windows.callbacks",
    "windows.shimcachemem",
    "windows.cmdline",
    "windows.svcscan",
    "windows.sessions",
    "windows.vadinfo",
    "windows.filescan",
    "windows.registry.userassist",
    "windows.dlllist",
    "windows.pslist",
    "windows.pstree",
    "windows.psscan",
    "windows.driverscan",
    "windows.malfind",
    "windows.registry.hivelist",
    "windows.ldrmodules",
    "windows.joblinks",
    "windows.handles"
]

# ============ GUI to Select Memory Dump ============
def browse_file():
    filepath = filedialog.askopenfilename(title="Select Memory Dump File")
    if filepath:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, filepath)

# ============ Install Volatility3 (Optional) ============
def install_volatility3():
    if not os.path.exists("volatility3"):
        subprocess.call("git clone https://github.com/volatilityfoundation/volatility3.git", shell=True)
    os.chdir("volatility3")
    subprocess.call("pip install -r requirements.txt", shell=True)

# ============ Run Plugins ============
def run_plugins():
    mem_file = entry_file.get()
    if not os.path.exists(mem_file):
        messagebox.showerror("Error", "Memory dump file not found!")
        return

    # Set the correct output path
    base_output_dir = "static/volatility_output"
    output_dir = os.path.join(base_output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # Move to volatility3 folder temporarily just to execute vol.py
    volatility_dir = "volatility3"
    if not os.path.exists(volatility_dir):
        try:
            subprocess.call(f"git clone https://github.com/volatilityfoundation/volatility3.git", shell=True)
            subprocess.call(f"pip install -r {volatility_dir}/requirements.txt", shell=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to install Volatility3: {e}")
            return

    # Check if vol.py exists
    vol_py_path = os.path.join(volatility_dir, "vol.py")
    if not os.path.exists(vol_py_path):
        messagebox.showerror("Error", f"Volatility3 not found at: {vol_py_path}")
        return

    for plugin in plugins:
        print(f"Running plugin: {plugin}")
        try:
            result = subprocess.run(
                ["python", vol_py_path, "-f", mem_file, plugin],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            out = result.stdout

            if out.strip() == "":
                continue

            csv_path = os.path.join(output_dir, f"{plugin.replace('.', '_')}.csv")
            html_path = os.path.join(output_dir, f"{plugin.replace('.', '_')}.html")

            # Try to split output into rows/columns
            lines = out.strip().split("\n")
            headers = lines[0].split()
            data = [line.split(None, len(headers)-1) for line in lines[1:] if line.strip()]

            # Safe write to CSV/HTML
            df = pd.DataFrame(data, columns=headers)
            df.to_csv(csv_path, index=False)
            df.to_html(html_path, index=False)
        except Exception as e:
            print(f"[!] Failed to process plugin {plugin}: {e}")

    messagebox.showinfo("Done", f"Plugin outputs saved to folder:\n{output_dir}")


# ============ GUI Layout ============
root = tk.Tk()
root.title("Volatility3 Memory Forensics Tool")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

label_file = tk.Label(frame, text="Select Memory Dump:")
label_file.grid(row=0, column=0, sticky="w")

entry_file = tk.Entry(frame, width=50)
entry_file.grid(row=1, column=0, padx=5, pady=5)

btn_browse = tk.Button(frame, text="Browse", command=browse_file)
btn_browse.grid(row=1, column=1, padx=5)

btn_run = tk.Button(frame, text="Run Volatility Plugins", command=run_plugins, bg="green", fg="white")
btn_run.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
