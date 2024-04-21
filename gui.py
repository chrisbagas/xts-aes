import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from xts_aes_runner import XTSAES_RUNNER
import os

ENCRYPTION = 'encryption'
DECRYPTION = 'decryption'

TEXT_TYPES = {
    ENCRYPTION: 'plaintext',
    DECRYPTION: 'ciphertext',
}
xtsaes_runner = XTSAES_RUNNER()
class FileEncryptorApp:
    def __init__(self, root, encryptor : XTSAES_RUNNER):
        self.encryptor = encryptor
        self.root = root
        self.root.title("File Encryptor")
        self.root.geometry("340x400")
        self.root.resizable(False, False)

        # Configure light mode and dark mode colors
        self.light_mode_bg = "#FFFFFF"
        self.light_mode_fg = "#000000"
        self.light_mode_button_bg = "#E0E0E0"
        self.light_mode_button_fg = "#000000"
        self.dark_mode_bg = "#121212"
        self.dark_mode_fg = "#FFFFFF"
        self.dark_mode_button_bg = "#37474F"
        self.dark_mode_button_fg = "#FFFFFF"

        # Default to light mode
        self.bg_color = self.light_mode_bg
        self.fg_color = self.light_mode_fg
        self.button_bg_color = self.light_mode_button_bg
        self.button_fg_color = self.light_mode_button_fg

        # Add mode selector
        self.mode_var = tk.IntVar()
        self.mode_var.set(0)  # Default to light mode
        self.mode_selector = tk.Checkbutton(root, text="Dark Mode", variable=self.mode_var, command=self.toggle_mode)
        self.mode_selector.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # Create widgets
        self.title_label = tk.Label(root, text="XTS AES Encryptor and Decryptor", font=("Helvetica", 14, "bold"), bg=self.bg_color, fg=self.fg_color)
        self.select_file_button = tk.Button(root, text="Select File", command=self.select_file, width=20, height=2, bg=self.button_bg_color, fg=self.button_fg_color, activebackground=self.button_bg_color, activeforeground=self.button_fg_color)
        self.select_key_button = tk.Button(root, text="Select Key", command=self.select_key, width=20, height=2, bg=self.button_bg_color, fg=self.button_fg_color, activebackground=self.button_bg_color, activeforeground=self.button_fg_color)
        self.encrypt_button = tk.Button(root, text="Encrypt", command=self.encrypt_file, width=20, height=2, bg=self.button_bg_color, fg=self.button_fg_color, activebackground=self.button_bg_color, activeforeground=self.button_fg_color)
        self.decrypt_button = tk.Button(root, text="Decrypt", command=self.decrypt_file, width=20, height=2, bg=self.button_bg_color, fg=self.button_fg_color, activebackground=self.button_bg_color, activeforeground=self.button_fg_color)
        self.download_button = tk.Button(root, text="Download Output", command=self.download_output, width=20, height=2, bg=self.button_bg_color, fg=self.button_fg_color, activebackground=self.button_bg_color, activeforeground=self.button_fg_color)

        # Load lock icon
        self.lock_image = Image.open("lock_icon.png")
        self.lock_image = self.lock_image.resize((50, 50))
        self.lock_icon = ImageTk.PhotoImage(self.lock_image)

        # Create labels
        self.select_file_label = tk.Label(root, text="No file selected", font=("Helvetica", 10), bg=self.bg_color, fg=self.fg_color)
        self.select_key_label = tk.Label(root, text="No key file selected", font=("Helvetica", 10), bg=self.bg_color, fg=self.fg_color)
        self.lock_icon_label = tk.Label(root, image=self.lock_icon, bg=self.bg_color)

        # Layout widgets
        self.title_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.select_file_button.grid(row=2, column=0, padx=10, pady=10)
        self.select_file_label.grid(row=2, column=1, padx=10, pady=10)
        self.select_key_button.grid(row=3, column=0, padx=10, pady=10)
        self.select_key_label.grid(row=3, column=1, padx=10, pady=10)
        self.encrypt_button.grid(row=4, column=0, padx=10, pady=10)
        self.decrypt_button.grid(row=4, column=1, padx=10, pady=10)
        self.download_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        self.lock_icon_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        # Apply light mode theme
        self.apply_theme()

    def select_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.select_file_label.config(text=os.path.basename(self.file_path))
            self.file_type = self.file_path.split('.')[1]

    def select_key(self):
        self.key_file_path = filedialog.askopenfilename()
        if self.key_file_path:
            self.select_key_label.config(text=os.path.basename(self.key_file_path))
            

    def encrypt_file(self):
        if not hasattr(self, 'file_path'):
            messagebox.showerror("Error", "Please select a file first.")
            return
        
        if not hasattr(self, 'key_file_path'):
            messagebox.showerror("Error", "Please select a key file first.")
            return
        
        self.encryptor.mode = 'encryption'
        self.encryptor.inverse_mode = 'decryption'

        try:
            print(self.encryptor)
            self.result, self.file_output = self.encryptor.run(self.file_path, self.file_type, self.key_file_path)
            messagebox.showinfo("Success", "File encrypted successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def decrypt_file(self):
        if not hasattr(self, 'file_path'):
            messagebox.showerror("Error", "Please select a file first.")
            return

        if not hasattr(self, 'key_file_path'):
            messagebox.showerror("Error", "Please select a key file first.")
            return

        self.encryptor.mode = 'decryption'
        self.encryptor.inverse_mode = 'encryption'
        try:
            self.result, self.file_output = self.encryptor.run(self.file_path, self.file_type, self.key_file_path)
            messagebox.showinfo("Success", "File decrypted successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def download_output(self):
        if not hasattr(self, 'result'):
            messagebox.showerror("Error", "No output data to download.")
            return

        # Prompt user to choose a download location
        download_path = filedialog.askdirectory()
        print(download_path)
        print(self.file_output)
        print(download_path+self.file_output)
        if download_path:
            try:
                with open(download_path+'/'+self.file_output, "wb") as file:
                    file.write(self.result)
                messagebox.showinfo("Success", "Output file downloaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error while saving file: {str(e)}")
        else:
            messagebox.showinfo("Info", "Download canceled.")


    def toggle_mode(self):
        if self.mode_var.get() == 1:
            # Switch to dark mode
            self.bg_color = self.dark_mode_bg
            self.fg_color = self.dark_mode_fg
            self.button_bg_color = self.dark_mode_button_bg
            self.button_fg_color = self.dark_mode_button_fg
        else:
            # Switch to light mode
            self.bg_color = self.light_mode_bg
            self.fg_color = self.light_mode_fg
            self.button_bg_color = self.light_mode_button_bg
            self.button_fg_color = self.light_mode_button_fg

        # Apply the chosen theme
        self.apply_theme()

    def apply_theme(self):
        # Apply colors to all widgets
        self.root.config(bg=self.bg_color)  # Update root background color
        self.mode_selector.config(bg=self.bg_color, fg=self.fg_color)
        self.title_label.config(bg=self.bg_color, fg=self.fg_color)
        self.select_file_button.config(bg=self.button_bg_color, fg=self.button_fg_color, activebackground=self.button_bg_color, activeforeground=self.button_fg_color)
        self.select_key_button.config(bg=self.button_bg_color, fg=self.button_fg_color, activebackground=self.button_bg_color, activeforeground=self.button_fg_color)
        self.encrypt_button.config(bg=self.button_bg_color, fg=self.button_fg_color, activebackground=self.button_bg_color, activeforeground=self.button_fg_color)
        self.decrypt_button.config(bg=self.button_bg_color, fg=self.button_fg_color, activebackground=self.button_bg_color, activeforeground=self.button_fg_color)
        self.download_button.config(bg=self.button_bg_color, fg=self.button_fg_color, activebackground=self.button_bg_color, activeforeground=self.button_fg_color)
        self.select_file_label.config(bg=self.bg_color, fg=self.fg_color)
        self.select_key_label.config(bg=self.bg_color, fg=self.fg_color)
        self.lock_icon_label.config(bg=self.bg_color)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileEncryptorApp(root,xtsaes_runner)
    root.mainloop()
