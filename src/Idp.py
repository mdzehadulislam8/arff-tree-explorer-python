import os
import tarfile
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from datetime import datetime
import threading

LOG_FILE = "file_secure.log"

class Logger:
    @staticmethod
    def log(message):
        with open(LOG_FILE, "a") as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

class FileUtils:
    @staticmethod
    def get_file_size(path):
        return os.path.getsize(path) if os.path.isfile(path) else sum(
            os.path.getsize(os.path.join(dp, f)) for dp, _, files in os.walk(path) for f in files
        )

    @staticmethod
    def compare_sizes(original, compressed):
        try:
            return round((1 - (compressed / original)) * 100, 2)
        except ZeroDivisionError:
            return 0

class CompressorEncryptor:
    def __init__(self, passphrase, comp_type, cipher_algo):
        self.passphrase = passphrase
        self.comp_type = comp_type
        self.cipher_algo = cipher_algo

    def compress(self, input_path, output_dir):
        base_name = os.path.basename(input_path.rstrip('/'))
        comp_ext, mode = self.comp_type
        archive_path = os.path.join(output_dir, f"{base_name}.tar.{comp_ext}")
        with tarfile.open(archive_path, mode) as tar:
            tar.add(input_path, arcname=base_name)
        return archive_path

    def encrypt(self, archive_path):
        subprocess.run([
            "gpg", "--batch", "--yes", "--passphrase", self.passphrase,
            "-c", "--cipher-algo", self.cipher_algo, archive_path
        ], check=True)
        os.remove(archive_path)
        return archive_path + ".gpg"

    def compress_and_encrypt(self, input_path, output_dir):
        archive_path = self.compress(input_path, output_dir)
        Logger.log(f"Compressed '{input_path}' to '{archive_path}'")
        encrypted_path = self.encrypt(archive_path)
        Logger.log(f"Encrypted '{archive_path}' to '{encrypted_path}'")
        return encrypted_path

class DecryptorDecompressor:
    def __init__(self, passphrase):
        self.passphrase = passphrase

    def decrypt(self, enc_file):
        output_file = enc_file[:-4]
        subprocess.run([
            "gpg", "--batch", "--yes", "--passphrase", self.passphrase,
            "--output", output_file, "--decrypt", enc_file
        ], check=True)
        return output_file

    def decompress(self, archive_path):
        with tarfile.open(archive_path) as tar:
            tar.extractall()
        os.remove(archive_path)

    def decrypt_and_decompress(self, enc_file):
        decrypted_path = self.decrypt(enc_file)
        Logger.log(f"Decrypted '{enc_file}' to '{decrypted_path}'")
        self.decompress(decrypted_path)
        Logger.log(f"Decompressed '{decrypted_path}'")

class FileViewer:
    @staticmethod
    def preview_file(file_path):
        try:
            with open(file_path, 'rb') as f:
                content = f.read(1024)
            return content.hex(), content.decode(errors='replace')
        except Exception as e:
            return f"Error: {e}", ""

class SecureFileUtilityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure File Utility Pro")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self.root)
        self.tab_encrypt = ttk.Frame(notebook, padding=10)
        self.tab_decrypt = ttk.Frame(notebook, padding=10)
        self.tab_logs = ttk.Frame(notebook, padding=10)
        self.tab_preview = ttk.Frame(notebook, padding=10)

        notebook.add(self.tab_encrypt, text="Compress & Encrypt")
        notebook.add(self.tab_decrypt, text="Decrypt & Decompress")
        notebook.add(self.tab_logs, text="Logs")
        notebook.add(self.tab_preview, text="Preview File")
        notebook.pack(expand=1, fill="both")

        self.setup_encrypt_tab()
        self.setup_decrypt_tab()
        self.setup_logs_tab()
        self.setup_preview_tab()

    def setup_encrypt_tab(self):
        frame = self.tab_encrypt

        ttk.Label(frame, text="Input file or folder:").grid(row=0, column=0, sticky="w")
        self.input_path_entry = ttk.Entry(frame, width=50)
        self.input_path_entry.grid(row=0, column=1, padx=5)
        ttk.Button(frame, text="Browse", command=self.browse_input_path).grid(row=0, column=2)

        ttk.Label(frame, text="Output directory:").grid(row=1, column=0, sticky="w", pady=10)
        self.output_dir = tk.StringVar()
        self.output_path_entry = ttk.Entry(frame, textvariable=self.output_dir, width=50)
        self.output_path_entry.grid(row=1, column=1, padx=5)
        ttk.Button(frame, text="Browse", command=self.browse_output_dir).grid(row=1, column=2)

        ttk.Label(frame, text="Compression Type:").grid(row=2, column=0, sticky="w", pady=10)
        self.comp_type = tk.StringVar(value="gz")
        ttk.Combobox(frame, textvariable=self.comp_type, values=["gz", "bz2", "xz"]).grid(row=2, column=1, sticky="w")

        ttk.Label(frame, text="Cipher Algorithm:").grid(row=3, column=0, sticky="w", pady=10)
        self.cipher_algo = tk.StringVar(value="AES256")
        ttk.Combobox(frame, textvariable=self.cipher_algo, values=["AES256", "AES192", "AES128"]).grid(row=3, column=1, sticky="w")

        ttk.Label(frame, text="Passphrase:").grid(row=4, column=0, sticky="w", pady=10)
        self.pass_entry = ttk.Entry(frame, show="*")
        self.pass_entry.grid(row=4, column=1, sticky="w")

        ttk.Button(frame, text="Compress and Encrypt", command=self.run_encrypt_thread).grid(row=5, column=1, pady=20)
        self.status_label = ttk.Label(frame, text="", foreground="green")
        self.status_label.grid(row=6, column=0, columnspan=3)

    def setup_decrypt_tab(self):
        frame = self.tab_decrypt

        ttk.Label(frame, text="Encrypted File (.gpg):").grid(row=0, column=0, sticky="w")
        self.decrypt_entry = ttk.Entry(frame, width=50)
        self.decrypt_entry.grid(row=0, column=1, padx=5)
        ttk.Button(frame, text="Browse", command=self.browse_encrypted_file).grid(row=0, column=2)

        ttk.Label(frame, text="Passphrase:").grid(row=1, column=0, sticky="w", pady=10)
        self.decrypt_pass = ttk.Entry(frame, show="*")
        self.decrypt_pass.grid(row=1, column=1)

        ttk.Button(frame, text="Decrypt and Decompress", command=self.run_decrypt_thread).grid(row=2, column=1, pady=20)

    def setup_logs_tab(self):
        self.log_text = scrolledtext.ScrolledText(self.tab_logs, wrap=tk.WORD)
        self.log_text.pack(expand=True, fill="both")
        self.refresh_logs()

    def setup_preview_tab(self):
        frame = self.tab_preview

        ttk.Label(frame, text="Select file to preview:").grid(row=0, column=0, sticky="w")
        self.preview_entry = ttk.Entry(frame, width=50)
        self.preview_entry.grid(row=0, column=1, padx=5)
        ttk.Button(frame, text="Browse", command=self.browse_preview_file).grid(row=0, column=2)

        self.hex_text = scrolledtext.ScrolledText(frame, height=10)
        self.hex_text.grid(row=1, column=0, columnspan=3, pady=5)
        self.text_text = scrolledtext.ScrolledText(frame, height=10)
        self.text_text.grid(row=2, column=0, columnspan=3, pady=5)

        ttk.Button(frame, text="Preview", command=self.preview_file).grid(row=3, column=1, pady=10)

    def browse_input_path(self):
        path = filedialog.askopenfilename() or filedialog.askdirectory()
        if path:
            self.input_path_entry.delete(0, tk.END)
            self.input_path_entry.insert(0, path)

    def browse_output_dir(self):
        path = filedialog.askdirectory()
        if path:
            self.output_path_entry.delete(0, tk.END)
            self.output_path_entry.insert(0, path)

    def browse_encrypted_file(self):
        path = filedialog.askopenfilename(filetypes=[("GPG Files", "*.gpg")])
        if path:
            self.decrypt_entry.delete(0, tk.END)
            self.decrypt_entry.insert(0, path)

    def browse_preview_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.preview_entry.delete(0, tk.END)
            self.preview_entry.insert(0, path)

    def preview_file(self):
        file_path = self.preview_entry.get()
        hex_view, text_view = FileViewer.preview_file(file_path)
        self.hex_text.delete(1.0, tk.END)
        self.hex_text.insert(tk.END, hex_view)
        self.text_text.delete(1.0, tk.END)
        self.text_text.insert(tk.END, text_view)

    def refresh_logs(self):
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE) as f:
                self.log_text.delete(1.0, tk.END)
                self.log_text.insert(tk.END, f.read())

    def run_encrypt_thread(self):
        threading.Thread(target=self.compress_and_encrypt, daemon=True).start()

    def compress_and_encrypt(self):
        input_path = self.input_path_entry.get()
        output_dir = self.output_dir.get()
        comp_ext = self.comp_type.get()
        passphrase = self.pass_entry.get()
        cipher = self.cipher_algo.get()
        comp_map = {"gz": "w:gz", "bz2": "w:bz2", "xz": "w:xz"}

        if not all([input_path, output_dir, passphrase]):
            messagebox.showerror("Error", "All fields are required.")
            return

        comp_obj = CompressorEncryptor(passphrase, (comp_ext, comp_map[comp_ext]), cipher)
        try:
            orig_size = FileUtils.get_file_size(input_path)
            encrypted_file = comp_obj.compress_and_encrypt(input_path, output_dir)
            enc_size = FileUtils.get_file_size(encrypted_file)
            saved = FileUtils.compare_sizes(orig_size, enc_size)
            self.status_label.config(text=f"Encrypted file saved at: {encrypted_file} | Space saved: {saved}%")
            messagebox.showinfo("Success", f"File encrypted and saved.\nSpace saved: {saved}%")
        except Exception as e:
            Logger.log(f"Encrypt error: {e}")
            messagebox.showerror("Error", str(e))

    def run_decrypt_thread(self):
        threading.Thread(target=self.decrypt_and_decompress, daemon=True).start()

    def decrypt_and_decompress(self):
        enc_file = self.decrypt_entry.get()
        passphrase = self.decrypt_pass.get()
        if not all([enc_file, passphrase]):
            messagebox.showerror("Error", "Encrypted file and passphrase are required.")
            return
        try:
            dec = DecryptorDecompressor(passphrase)
            dec.decrypt_and_decompress(enc_file)
            messagebox.showinfo("Success", "File decrypted and decompressed successfully.")
        except Exception as e:
            Logger.log(f"Decrypt error: {e}")
            messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    app = SecureFileUtilityApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
