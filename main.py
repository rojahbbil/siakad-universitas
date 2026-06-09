import tkinter as tk
from tkinter import messagebox
from forms import (
    MahasiswaForm, 
    DosenForm, 
    MatakuliahForm, 
    ProdiForm, 
    get_db_connection
)


class SiakadApp:
    """Kelas utama aplikasi SIAKAD - Sistem Informasi Akademik"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("SIAKAD - Sistem Informasi Akademik")
        self.root.geometry("1120x700")
        self.root.configure(bg="#f0f2f5")
        self.root.resizable(True, True)

        # Variabel sesi user
        self.current_user = None
        self.current_role = None

        # Container utama
        self.container = tk.Frame(self.root, bg="#f0f2f5")
        self.container.pack(fill="both", expand=True)

        self.show_login_page()

    # ==================== LOGIN PAGE ====================
    def show_login_page(self):
        """Menampilkan halaman login"""
        self.clear_container()

        login_frame = tk.Frame(self.container, padx=50, pady=60, bg="white", relief="raised", bd=3)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(login_frame, text="SIAKAD", font=("Arial", 32, "bold"), 
                bg="white", fg="#2c3e50").pack(pady=(10, 5))
        tk.Label(login_frame, text="Sistem Informasi Akademik", 
                font=("Arial", 14), bg="white", fg="#7f8c8d").pack(pady=(0, 40))

        # Username
        tk.Label(login_frame, text="Username", bg="white", font=("Arial", 11)).pack(anchor="w", padx=10)
        self.ent_username = tk.Entry(login_frame, width=35, font=("Arial", 12))
        self.ent_username.pack(pady=8, padx=10, ipadx=5)

        # Password
        tk.Label(login_frame, text="Password", bg="white", font=("Arial", 11)).pack(anchor="w", padx=10)
        self.ent_password = tk.Entry(login_frame, width=35, show="*", font=("Arial", 12))
        self.ent_password.pack(pady=8, padx=10, ipadx=5)

        # Tombol Login
        tk.Button(login_frame, text="LOGIN", width=30, height=2, bg="#3498db", fg="white",
                 font=("Arial", 12, "bold"), command=self.proses_login).pack(pady=30)

    def proses_login(self):
        """Proses autentikasi"""
        username = self.ent_username.get().strip()
        password = self.ent_password.get().strip()

        if not username or not password:
            messagebox.showwarning("Peringatan", "Username dan Password harus diisi!")
            return

        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT role FROM users WHERE username = %s AND password = %s", 
                             (username, password))
                result = cursor.fetchone()

                if result:
                    self.current_user = username
                    self.current_role = result[0]
                    messagebox.showinfo("Login Berhasil", 
                                      f"Selamat datang, {username}!\nRole: {self.current_role}")
                    self.show_main_page()
                else:
                    messagebox.showerror("Login Gagal", "Username atau Password salah!")
            except Exception as e:
                messagebox.showerror("Error", f"Terjadi kesalahan:\n{e}")
            finally:
                cursor.close()
                conn.close()

    # ==================== MAIN PAGE ====================
    def show_main_page(self):
        """Halaman utama setelah login"""
        self.clear_container()

        # Footer
        footer = tk.Frame(self.container, bg="#2c3e50", height=55)
        footer.pack(side="bottom", fill="x")

        tk.Label(footer, text=f"User aktif: {self.current_user}   |   Role: {self.current_role}",
                bg="#2c3e50", fg="white", font=("Arial", 10)).pack(side="left", padx=20, pady=15)
        
        tk.Button(footer, text="Logout", command=self.show_login_page,
                 bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), 
                 padx=25, pady=8).pack(side="right", padx=20)

        # Workspace
        self.workspace = tk.Frame(self.container, bg="#f5f6fa")
        self.workspace.pack(fill="both", expand=True)

        welcome = tk.Label(self.workspace, 
                          text="Selamat Datang di SIAKAD\nSilakan pilih menu pada bagian atas",
                          font=("Arial", 18, "bold"), bg="#f5f6fa", fg="#2c3e50", justify="center")
        welcome.pack(expand=True)

        self.setup_menu()

    def setup_menu(self):
        """Membuat menu berdasarkan role user"""
        menubar = tk.Menu(self.root)
        data_menu = tk.Menu(menubar, tearoff=0)

        if self.current_role in ["Admin", "Operator"]:
            data_menu.add_command(label="Data Mahasiswa", command=self.load_mahasiswa_form)
            data_menu.add_command(label="Data Dosen", command=self.load_dosen_form)
            data_menu.add_command(label="Data Program Studi", command=self.load_prodi_form)

        if self.current_role in ["Admin", "Operator", "Mahasiswa"]:
            data_menu.add_command(label="Data Mata Kuliah", command=self.load_matakuliah_form)

        menubar.add_cascade(label="Kelola Data", menu=data_menu)
        self.root.config(menu=menubar)

    # ==================== HELPER METHODS ====================
    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def clear_workspace(self):
        for widget in self.workspace.winfo_children():
            widget.destroy()

    def load_mahasiswa_form(self):
        self.clear_workspace()
        MahasiswaForm(self.workspace, self.current_role, self.show_main_page)

    def load_dosen_form(self):
        self.clear_workspace()
        DosenForm(self.workspace, self.current_role, self.show_main_page)

    def load_matakuliah_form(self):
        self.clear_workspace()
        MatakuliahForm(self.workspace, self.current_role, self.show_main_page)

    def load_prodi_form(self):
        self.clear_workspace()
        ProdiForm(self.workspace, self.current_role, self.show_main_page)


if __name__ == "__main__":
    root = tk.Tk()
    app = SiakadApp(root)
    root.mainloop()