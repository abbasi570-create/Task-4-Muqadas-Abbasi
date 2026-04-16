from PIL import Image, ImageTk
import pytesseract
import tkinter as tk
from tkinter import filedialog, Text, Scrollbar, messagebox

# 👉 Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# ---------------- OPEN IMAGE ----------------
def open_image():
    global img_display

    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.png *.jpg *.jpeg")]
    )

    if file_path:
        # Load image
        image = Image.open(file_path)

        # Resize for display
        image = image.resize((250, 250))
        img_display = ImageTk.PhotoImage(image)

        image_label.config(image=img_display)
        image_label.image = img_display

        # OCR extract
        text = pytesseract.image_to_string(image)

        result_box.delete("1.0", tk.END)
        result_box.insert(tk.END, text if text.strip() else "No text found 😕")


# ---------------- SAVE TEXT ----------------
def save_text():
    text = result_box.get("1.0", tk.END)

    if text.strip():
        file = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text files", "*.txt")])
        if file:
            with open(file, "w", encoding="utf-8") as f:
                f.write(text)
            messagebox.showinfo("Saved", "Text saved successfully!")
    else:
        messagebox.showwarning("Empty", "No text to save!")


# ---------------- GUI WINDOW ----------------
window = tk.Tk()
window.title("AI Image OCR App")
window.geometry("700x600")

# Button frame
btn_frame = tk.Frame(window)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="📂 Open Image", command=open_image, bg="lightblue").grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="💾 Save Text", command=save_text, bg="lightgreen").grid(row=0, column=1, padx=10)

# Image display
image_label = tk.Label(window)
image_label.pack(pady=10)

# Scrollable text box
scroll = Scrollbar(window)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

result_box = Text(window, wrap=tk.WORD, yscrollcommand=scroll.set, height=15)
result_box.pack(expand=True, fill="both", padx=10)

scroll.config(command=result_box.yview)

# Run app
window.mainloop()