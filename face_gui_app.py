import tkinter as tk
from tkinter import messagebox
import subprocess  #  Add this here

# Create the main window
root = tk.Tk()
root.title("Face Recognition Surveillance")
root.geometry("400x300")
root.config(bg="#f7f7f7")

# Title Label
title = tk.Label(root, text="👮 Face Recognition Surveillance System", font=("Arial", 14, "bold"), bg="#f7f7f7", fg="#333")
title.pack(pady=20)

# Start Button
def start_detection():
    print("🟢 Start button clicked!")
    messagebox.showinfo("Surveillance", "Camera detection will start now!")
    subprocess.Popen(["python", "face_recognition_main.py"])  #  Runs face recognition

start_btn = tk.Button(root, text="🎥 Start Detection", font=("Arial", 12), command=start_detection, bg="#4CAF50", fg="white", width=20)
start_btn.pack(pady=10)

# Quit Button
quit_btn = tk.Button(root, text="❌ Quit", font=("Arial", 12), command=root.destroy, bg="#e74c3c", fg="white", width=20)
quit_btn.pack(pady=10)

#  This must be last
root.mainloop()

