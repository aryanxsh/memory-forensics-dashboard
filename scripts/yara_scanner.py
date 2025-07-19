import tkinter as tk
from tkinter import filedialog, messagebox
import os
from datetime import datetime
import yara

# Compile all YARA rules from a folder, skipping invalid ones
def load_yara_rules(rule_path="./rules"):
    valid_rule_files = {}
    index = 0

    for root, _, files in os.walk(rule_path):
        for f in files:
            if f.endswith(".yar") or f.endswith(".yara"):
                rule_file_path = os.path.join(root, f)
                try:
                    # Try compiling it individually
                    yara.compile(filepath=rule_file_path)
                    valid_rule_files[f"rule_{index}"] = rule_file_path
                    index += 1
                except yara.SyntaxError as e:
                    print(f"[!] Skipping invalid rule {f}: {e}")
                except Exception as e:
                    print(f"[!] Error compiling rule {f}: {e}")

    if not valid_rule_files:
        raise RuntimeError("No valid YARA rules could be compiled.")

    # Compile all valid rules together
    return yara.compile(filepaths=valid_rule_files)

# Save result to log
def save_result_log(file_path, result_text):
    os.makedirs("static/yara_output", exist_ok=True)
    with open("static/yara_output/scan_results.txt", "a") as f:
        f.write(f"\n[{datetime.now()}] Scan: {file_path}\n")
        f.write(result_text + "\n")

# Scan single file
def scan_file():
    file_path = filedialog.askopenfilename(title="Choose file to scan")
    if not file_path:
        return
    perform_scan(file_path)

# Scan folder
def scan_folder():
    folder_path = filedialog.askdirectory(title="Choose folder to scan")
    if not folder_path:
        return
    for root, _, files in os.walk(folder_path):
        for name in files:
            file_path = os.path.join(root, name)
            perform_scan(file_path)

# Scan logic
def perform_scan(file_path):
    try:
        matches = rules.match(file_path)
        if matches:
            result = f"🚨 MALWARE DETECTED in {os.path.basename(file_path)} 🚨\n\nMatched rules:\n" + \
                     "\n".join([m.rule for m in matches])
        else:
            result = f"✅ {os.path.basename(file_path)} is clean. No YARA rule matched."

        messagebox.showinfo("Scan Result", result)
        save_result_log(file_path, result)
    except Exception as e:
        messagebox.showerror("Scan Error", f"Failed to scan file:\n{e}")

# Load rules at startup
try:
    rules = load_yara_rules("./scripts/rules")
except Exception as e:
    print("Error loading YARA rules:", e)
    tk.Tk().withdraw()  # Hide extra window
    messagebox.showerror("YARA Rule Error", f"Failed to load valid YARA rules:\n\n{e}")
    exit()

# GUI Setup
root = tk.Tk()
root.title("🛡️ YARA GUI Malware Scanner")
root.geometry("460x260")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

label = tk.Label(frame, text="🛡️ Scan any file or folder using YARA malware rules", font=("Arial", 12))
label.pack(pady=10)

btn_file = tk.Button(frame, text="📁 Scan Single File", command=scan_file, bg="green", fg="white", width=25)
btn_file.pack(pady=5)

btn_folder = tk.Button(frame, text="📂 Scan Entire Folder", command=scan_folder, bg="blue", fg="white", width=25)
btn_folder.pack(pady=5)

note = tk.Label(frame, text="Results saved to scan_results.txt", font=("Arial", 9), fg="gray")
note.pack(pady=10)

root.mainloop()