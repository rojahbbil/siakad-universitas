import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


def get_db_connection():
    """Membuat koneksi ke database siakad"""
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",           
            database="siakad"
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Gagal koneksi ke database:\n{err}")
        return None


# ==================== BASE FORM ====================
class BaseForm(tk.Frame):
    def __init__(self, parent, role, close_callback, title):
        super().__init__(parent, bg="#f5f6fa")
        self.role = role
        self.close_callback = close_callback
        self.title = title
        self.pack(fill="both", expand=True)
        self.setup_ui()

    def create_top_bar(self):
        top_bar = tk.Frame(self, bg="#f5f6fa")
        top_bar.pack(side="top", fill="x", padx=15, pady=10)
        tk.Label(top_bar, text=self.title, font=("Arial", 14, "bold"), 
                bg="#f5f6fa", fg="#2c3e50").pack(side="left")
        tk.Button(top_bar, text="✕ Tutup", command=self.close_callback,
                 bg="#95a5a6", fg="white", bd=0, padx=12, pady=6, 
                 font=("Arial", 10, "bold")).pack(side="right")


# ==================== MAHASISWA FORM ====================
class MahasiswaForm(BaseForm):
    def __init__(self, parent, role, close_callback):
        super().__init__(parent, role, close_callback, "MANAJEMEN DATA MAHASISWA")

    def setup_ui(self):
        self.create_top_bar()
        center_frame = tk.Frame(self, bg="#f5f6fa")
        center_frame.pack(side="top", anchor="nw", padx=15, pady=10)

        form_frame = tk.LabelFrame(center_frame, text="Form Input", padx=15, pady=15, bg="white")
        form_frame.pack(side="left", fill="y", anchor="n", padx=(0, 20))

        tk.Label(form_frame, text="NIM:", bg="white", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=6)
        self.ent_nim = tk.Entry(form_frame, width=28)
        self.ent_nim.grid(row=0, column=1, pady=6)

        tk.Label(form_frame, text="Nama Lengkap:", bg="white", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=6)
        self.ent_nama = tk.Entry(form_frame, width=28)
        self.ent_nama.grid(row=1, column=1, pady=6)

        tk.Label(form_frame, text="Program Studi:", bg="white", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=6)
        self.ent_prodi = tk.Entry(form_frame, width=28)
        self.ent_prodi.grid(row=2, column=1, pady=6)

        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)

        tk.Button(btn_frame, text="Tambah", command=self.simpan_data, width=8, bg="#27ae60", fg="white").pack(side="left", padx=4)
        self.btn_edit = tk.Button(btn_frame, text="Edit", command=self.edit_data, width=8, bg="#f39c12", fg="black")
        self.btn_edit.pack(side="left", padx=4)
        if self.role != "Admin":
            self.btn_edit.config(state="disabled")
        tk.Button(btn_frame, text="Hapus", command=self.hapus_data, width=8, bg="#e74c3c", fg="white").pack(side="left", padx=4)
        tk.Button(btn_frame, text="Clear", command=self.bersihkan_form, width=8).pack(side="left", padx=4)

        self.tree = ttk.Treeview(center_frame, columns=("NIM", "Nama", "Prodi"), show="headings", height=18)
        self.tree.heading("NIM", text="NIM")
        self.tree.heading("Nama", text="Nama Mahasiswa")
        self.tree.heading("Prodi", text="Program Studi")
        self.tree.column("NIM", width=110, anchor="center")
        self.tree.column("Nama", width=240, anchor="w")
        self.tree.column("Prodi", width=200, anchor="w")
        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.bind("<ButtonRelease-1>", self.isi_form_dari_tabel)

        self.refresh_table()

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nim, nama, prodi FROM mahasiswa ORDER BY nim")
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
            cursor.close()
            conn.close()

    def bersihkan_form(self):
        self.ent_nim.config(state="normal")
        self.ent_nim.delete(0, tk.END)
        self.ent_nama.delete(0, tk.END)
        self.ent_prodi.delete(0, tk.END)

    def isi_form_dari_tabel(self, event):
        selected = self.tree.selection()
        if not selected: return
        data = self.tree.item(selected[0])['values']
        self.bersihkan_form()
        self.ent_nim.insert(0, data[0])
        self.ent_nama.insert(0, data[1])
        self.ent_prodi.insert(0, data[2])
        self.ent_nim.config(state="disabled")

    def simpan_data(self):
        nim = self.ent_nim.get().strip()
        nama = self.ent_nama.get().strip()
        prodi = self.ent_prodi.get().strip()
        if not (nim and nama and prodi):
            messagebox.showwarning("Peringatan", "Semua field harus diisi!")
            return
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO mahasiswa VALUES (%s, %s, %s)", (nim, nama, prodi))
                conn.commit()
                messagebox.showinfo("Sukses", "Data mahasiswa berhasil ditambahkan!")
                self.refresh_table()
                self.bersihkan_form()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal: {e}")
            finally:
                cursor.close()
                conn.close()

    def edit_data(self):
        self.ent_nim.config(state="normal")
        nim = self.ent_nim.get().strip()
        nama = self.ent_nama.get().strip()
        prodi = self.ent_prodi.get().strip()
        self.ent_nim.config(state="disabled")
        if not (nim and nama and prodi):
            messagebox.showwarning("Peringatan", "Pilih data yang akan diedit!")
            return
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE mahasiswa SET nama=%s, prodi=%s WHERE nim=%s", (nama, prodi, nim))
                conn.commit()
                messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
                self.refresh_table()
                self.bersihkan_form()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal: {e}")
            finally:
                cursor.close()
                conn.close()

    def hapus_data(self):
        self.ent_nim.config(state="normal")
        nim = self.ent_nim.get().strip()
        self.ent_nim.config(state="disabled")
        if not nim or not messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus data ini?"):
            return
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM mahasiswa WHERE nim=%s", (nim,))
                conn.commit()
                messagebox.showinfo("Sukses", "Data berhasil dihapus!")
                self.refresh_table()
                self.bersihkan_form()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal: {e}")
            finally:
                cursor.close()
                conn.close()


# ==================== DOSEN FORM ====================
class DosenForm(BaseForm):
    def __init__(self, parent, role, close_callback):
        super().__init__(parent, role, close_callback, "MANAJEMEN DATA DOSEN")

    def setup_ui(self):
        self.create_top_bar()
        center_frame = tk.Frame(self, bg="#f5f6fa")
        center_frame.pack(side="top", anchor="nw", padx=15, pady=10)

        form_frame = tk.LabelFrame(center_frame, text="Form Input", padx=15, pady=15, bg="white")
        form_frame.pack(side="left", fill="y", anchor="n", padx=(0, 20))

        tk.Label(form_frame, text="NIDN:", bg="white").grid(row=0, column=0, sticky="w", pady=6)
        self.ent_nidn = tk.Entry(form_frame, width=28)
        self.ent_nidn.grid(row=0, column=1, pady=6)

        tk.Label(form_frame, text="Nama Dosen:", bg="white").grid(row=1, column=0, sticky="w", pady=6)
        self.ent_nama = tk.Entry(form_frame, width=28)
        self.ent_nama.grid(row=1, column=1, pady=6)

        tk.Label(form_frame, text="Program Studi:", bg="white").grid(row=2, column=0, sticky="w", pady=6)
        self.ent_prodi = tk.Entry(form_frame, width=28)
        self.ent_prodi.grid(row=2, column=1, pady=6)

        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)

        tk.Button(btn_frame, text="Tambah", command=self.simpan_data, width=8, bg="#27ae60", fg="white").pack(side="left", padx=4)
        self.btn_edit = tk.Button(btn_frame, text="Edit", command=self.edit_data, width=8, bg="#f39c12", fg="black")
        self.btn_edit.pack(side="left", padx=4)
        if self.role != "Admin":
            self.btn_edit.config(state="disabled")
        tk.Button(btn_frame, text="Hapus", command=self.hapus_data, width=8, bg="#e74c3c", fg="white").pack(side="left", padx=4)
        tk.Button(btn_frame, text="Clear", command=self.bersihkan_form, width=8).pack(side="left", padx=4)

        self.tree = ttk.Treeview(center_frame, columns=("NIDN", "Nama", "Prodi"), show="headings", height=18)
        self.tree.heading("NIDN", text="NIDN")
        self.tree.heading("Nama", text="Nama Dosen")
        self.tree.heading("Prodi", text="Program Studi")
        self.tree.column("NIDN", width=120, anchor="center")
        self.tree.column("Nama", width=260, anchor="w")
        self.tree.column("Prodi", width=200, anchor="w")
        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.bind("<ButtonRelease-1>", self.isi_form_dari_tabel)

        self.refresh_table()

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nidn, nama, prodi FROM dosen ORDER BY nama")
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
            cursor.close()
            conn.close()

    def bersihkan_form(self):
        self.ent_nidn.config(state="normal")
        self.ent_nidn.delete(0, tk.END)
        self.ent_nama.delete(0, tk.END)
        self.ent_prodi.delete(0, tk.END)

    def isi_form_dari_tabel(self, event):
        selected = self.tree.selection()
        if not selected: return
        data = self.tree.item(selected[0])['values']
        self.bersihkan_form()
        self.ent_nidn.insert(0, data[0])
        self.ent_nama.insert(0, data[1])
        self.ent_prodi.insert(0, data[2])
        self.ent_nidn.config(state="disabled")

    def simpan_data(self):
        nidn = self.ent_nidn.get().strip()
        nama = self.ent_nama.get().strip()
        prodi = self.ent_prodi.get().strip()
        if not (nidn and nama and prodi):
            messagebox.showwarning("Peringatan", "Semua field harus diisi!")
            return
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO dosen VALUES (%s, %s, %s)", (nidn, nama, prodi))
                conn.commit()
                messagebox.showinfo("Sukses", "Data dosen berhasil ditambahkan!")
                self.refresh_table()
                self.bersihkan_form()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal: {e}")
            finally:
                cursor.close()
                conn.close()

    def edit_data(self):
        self.ent_nidn.config(state="normal")
        nidn = self.ent_nidn.get().strip()
        nama = self.ent_nama.get().strip()
        prodi = self.ent_prodi.get().strip()
        self.ent_nidn.config(state="disabled")
        if not (nidn and nama and prodi):
            messagebox.showwarning("Peringatan", "Pilih data yang akan diedit!")
            return
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE dosen SET nama=%s, prodi=%s WHERE nidn=%s", (nama, prodi, nidn))
                conn.commit()
                messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
                self.refresh_table()
                self.bersihkan_form()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal: {e}")
            finally:
                cursor.close()
                conn.close()

    def hapus_data(self):
        self.ent_nidn.config(state="normal")
        nidn = self.ent_nidn.get().strip()
        self.ent_nidn.config(state="disabled")
        if not nidn or not messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus?"):
            return
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM dosen WHERE nidn=%s", (nidn,))
                conn.commit()
                messagebox.showinfo("Sukses", "Data berhasil dihapus!")
                self.refresh_table()
                self.bersihkan_form()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal: {e}")
            finally:
                cursor.close()
                conn.close()


# ==================== MATAKULIAH FORM ====================
class MatakuliahForm(tk.Frame):
    def __init__(self, parent, role, close_callback):
        super().__init__(parent, bg="#f5f6fa")
        self.role = role
        self.close_callback = close_callback
        self.pack(fill="both", expand=True)
        self.setup_ui()

    def setup_ui(self):
        top_bar = tk.Frame(self, bg="#f5f6fa")
        top_bar.pack(side="top", fill="x", padx=15, pady=10)
        tk.Label(top_bar, text="MANAJEMEN DATA MATAKULIAH", font=("Arial", 14, "bold"), bg="#f5f6fa", fg="#2c3e50").pack(side="left")
        tk.Button(top_bar, text="✕ Tutup", command=self.close_callback, bg="#95a5a6", fg="white", padx=12, pady=6).pack(side="right")

        center_frame = tk.Frame(self, bg="#f5f6fa")
        center_frame.pack(side="top", anchor="nw", padx=15, pady=10)

        if self.role != "Mahasiswa":
            form_frame = tk.LabelFrame(center_frame, text="Form Input", padx=15, pady=15, bg="white")
            form_frame.pack(side="left", fill="y", anchor="n", padx=(0, 20))

            tk.Label(form_frame, text="Kode MK:", bg="white").grid(row=0, column=0, sticky="w", pady=6)
            self.ent_kode = tk.Entry(form_frame, width=28)
            self.ent_kode.grid(row=0, column=1, pady=6)

            tk.Label(form_frame, text="Nama Matakuliah:", bg="white").grid(row=1, column=0, sticky="w", pady=6)
            self.ent_nama = tk.Entry(form_frame, width=28)
            self.ent_nama.grid(row=1, column=1, pady=6)

            tk.Label(form_frame, text="SKS:", bg="white").grid(row=2, column=0, sticky="w", pady=6)
            self.ent_sks = tk.Entry(form_frame, width=28)
            self.ent_sks.grid(row=2, column=1, pady=6)

            btn_frame = tk.Frame(form_frame, bg="white")
            btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
            tk.Button(btn_frame, text="Tambah", command=self.simpan_data, bg="#27ae60", fg="white", width=8).pack(side="left", padx=4)
            self.btn_edit = tk.Button(btn_frame, text="Edit", command=self.edit_data, bg="#f39c12", fg="black", width=8)
            self.btn_edit.pack(side="left", padx=4)
            if self.role != "Admin":
                self.btn_edit.config(state="disabled")
            tk.Button(btn_frame, text="Hapus", command=self.hapus_data, bg="#e74c3c", fg="white", width=8).pack(side="left", padx=4)
            tk.Button(btn_frame, text="Clear", command=self.bersihkan_form, width=8).pack(side="left", padx=4)

        self.tree = ttk.Treeview(center_frame, columns=("Kode", "Nama", "SKS"), show="headings", height=18)
        self.tree.heading("Kode", text="Kode MK")
        self.tree.heading("Nama", text="Nama Matakuliah")
        self.tree.heading("SKS", text="SKS")
        self.tree.column("Kode", width=100, anchor="center")
        self.tree.column("Nama", width=320, anchor="w")
        self.tree.column("SKS", width=80, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)

        if self.role != "Mahasiswa":
            self.tree.bind("<ButtonRelease-1>", self.isi_form_dari_tabel)

        self.refresh_table()

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT kode_mk, nama_mk, sks FROM matakuliah ORDER BY kode_mk")
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
            cursor.close()
            conn.close()

    def bersihkan_form(self):
        if hasattr(self, 'ent_kode'):
            self.ent_kode.config(state="normal")
            self.ent_kode.delete(0, tk.END)
            self.ent_nama.delete(0, tk.END)
            self.ent_sks.delete(0, tk.END)

    def isi_form_dari_tabel(self, event):
        selected = self.tree.selection()
        if not selected: return
        data = self.tree.item(selected[0])['values']
        self.bersihkan_form()
        self.ent_kode.insert(0, data[0])
        self.ent_nama.insert(0, data[1])
        self.ent_sks.insert(0, data[2])
        self.ent_kode.config(state="disabled")

    def simpan_data(self):
        kode = self.ent_kode.get().strip()
        nama = self.ent_nama.get().strip()
        sks = self.ent_sks.get().strip()
        if not (kode and nama and sks):
            messagebox.showwarning("Peringatan", "Semua field harus diisi!")
            return
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO matakuliah VALUES (%s, %s, %s)", (kode, nama, int(sks)))
                conn.commit()
                messagebox.showinfo("Sukses", "Mata kuliah berhasil ditambahkan!")
                self.refresh_table()
                self.bersihkan_form()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal: {e}")
            finally:
                cursor.close()
                conn.close()

    def edit_data(self):
        self.ent_kode.config(state="normal")
        kode = self.ent_kode.get().strip()
        nama = self.ent_nama.get().strip()
        sks = self.ent_sks.get().strip()
        self.ent_kode.config(state="disabled")
        if not (kode and nama and sks):
            messagebox.showwarning("Peringatan", "Pilih data yang akan diedit!")
            return
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE matakuliah SET nama_mk=%s, sks=%s WHERE kode_mk=%s", (nama, int(sks), kode))
                conn.commit()
                messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
                self.refresh_table()
                self.bersihkan_form()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal: {e}")
            finally:
                cursor.close()
                conn.close()

    def hapus_data(self):
        self.ent_kode.config(state="normal")
        kode = self.ent_kode.get().strip()
        self.ent_kode.config(state="disabled")
        if not kode or not messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus?"):
            return
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM matakuliah WHERE kode_mk=%s", (kode,))
                conn.commit()
                messagebox.showinfo("Sukses", "Data berhasil dihapus!")
                self.refresh_table()
                self.bersihkan_form()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal: {e}")
            finally:
                cursor.close()
                conn.close()


# ==================== PRODI FORM ====================
class ProdiForm(tk.Frame):
    def __init__(self, parent, role, close_callback):
        super().__init__(parent, bg="#f5f6fa")
        self.role = role
        self.close_callback = close_callback
        self.pack(fill="both", expand=True)
        self.setup_ui()

    def setup_ui(self):
        top_bar = tk.Frame(self, bg="#f5f6fa")
        top_bar.pack(side="top", fill="x", padx=15, pady=10)
        tk.Label(top_bar, text="MANAJEMEN DATA PROGRAM STUDI", 
                font=("Arial", 14, "bold"), bg="#f5f6fa", fg="#2c3e50").pack(side="left")
        tk.Button(top_bar, text="✕ Tutup", command=self.close_callback,
                 bg="#95a5a6", fg="white", padx=12, pady=6, font=("Arial", 10, "bold")).pack(side="right")

        center_frame = tk.Frame(self, bg="#f5f6fa")
        center_frame.pack(side="top", anchor="nw", padx=15, pady=10)

        form_frame = tk.LabelFrame(center_frame, text="Form Input", padx=15, pady=15, bg="white")
        form_frame.pack(side="left", fill="y", anchor="n", padx=(0, 20))

        tk.Label(form_frame, text="ID Prodi:", bg="white").grid(row=0, column=0, sticky="w", pady=6)
        self.ent_id = tk.Entry(form_frame, width=28)
        self.ent_id.grid(row=0, column=1, pady=6)

        tk.Label(form_frame, text="Kode Prodi:", bg="white").grid(row=1, column=0, sticky="w", pady=6)
        self.ent_kode = tk.Entry(form_frame, width=28)
        self.ent_kode.grid(row=1, column=1, pady=6)

        tk.Label(form_frame, text="Nama Prodi:", bg="white").grid(row=2, column=0, sticky="w", pady=6)
        self.ent_nama = tk.Entry(form_frame, width=28)
        self.ent_nama.grid(row=2, column=1, pady=6)

        tk.Label(form_frame, text="Jenjang:", bg="white").grid(row=3, column=0, sticky="w", pady=6)
        self.ent_jenjang = tk.Entry(form_frame, width=28)
        self.ent_jenjang.grid(row=3, column=1, pady=6)

        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)

        tk.Button(btn_frame, text="Tambah", command=self.simpan_data, width=8, bg="#27ae60", fg="white").pack(side="left", padx=4)
        self.btn_edit = tk.Button(btn_frame, text="Edit", command=self.edit_data, width=8, bg="#f39c12", fg="black")
        self.btn_edit.pack(side="left", padx=4)
        if self.role != "Admin":
            self.btn_edit.config(state="disabled")
        tk.Button(btn_frame, text="Hapus", command=self.hapus_data, width=8, bg="#e74c3c", fg="white").pack(side="left", padx=4)
        tk.Button(btn_frame, text="Clear", command=self.bersihkan_form, width=8).pack(side="left", padx=4)

        self.tree = ttk.Treeview(center_frame, columns=("ID", "Kode", "Nama", "Jenjang"), show="headings", height=18)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Kode", text="Kode Prodi")
        self.tree.heading("Nama", text="Nama Prodi")
        self.tree.heading("Jenjang", text="Jenjang")
        self.tree.column("ID", width=70, anchor="center")
        self.tree.column("Kode", width=100, anchor="center")
        self.tree.column("Nama", width=280, anchor="w")
        self.tree.column("Jenjang", width=120, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.bind("<ButtonRelease-1>", self.isi_form_dari_tabel)

        self.refresh_table()

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_prodi, kode_prodi, nama_prodi, jenjang_pendidikan FROM m_program_studi ORDER BY kode_prodi")
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
            cursor.close()
            conn.close()

    def bersihkan_form(self):
        self.ent_id.config(state="normal")
        self.ent_id.delete(0, tk.END)
        self.ent_kode.delete(0, tk.END)
        self.ent_nama.delete(0, tk.END)
        self.ent_jenjang.delete(0, tk.END)

    def isi_form_dari_tabel(self, event):
        selected = self.tree.selection()
        if not selected: return
        data = self.tree.item(selected[0])['values']
        self.bersihkan_form()
        self.ent_id.insert(0, data[0])
        self.ent_kode.insert(0, data[1])
        self.ent_nama.insert(0, data[2])
        self.ent_jenjang.insert(0, data[3])
        self.ent_id.config(state="disabled")

    def simpan_data(self):
        id_prodi = self.ent_id.get().strip()
        kode = self.ent_kode.get().strip()
        nama = self.ent_nama.get().strip()
        jenjang = self.ent_jenjang.get().strip()
        if not (id_prodi and kode and nama and jenjang):
            messagebox.showwarning("Peringatan", "Semua field harus diisi!")
            return
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO m_program_studi (id_prodi, kode_prodi, nama_prodi, jenjang_pendidikan) 
                    VALUES (%s, %s, %s, %s)
                """, (id_prodi, kode, nama, jenjang))
                conn.commit()
                messagebox.showinfo("Sukses", "Program Studi berhasil ditambahkan!")
                self.refresh_table()
                self.bersihkan_form()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal: {e}")
            finally:
                cursor.close()
                conn.close()

    def edit_data(self):
        self.ent_id.config(state="normal")
        id_prodi = self.ent_id.get().strip()
        kode = self.ent_kode.get().strip()
        nama = self.ent_nama.get().strip()
        jenjang = self.ent_jenjang.get().strip()
        self.ent_id.config(state="disabled")
        if not (id_prodi and kode and nama and jenjang):
            messagebox.showwarning("Peringatan", "Pilih data yang akan diedit!")
            return
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE m_program_studi 
                    SET kode_prodi=%s, nama_prodi=%s, jenjang_pendidikan=%s 
                    WHERE id_prodi=%s
                """, (kode, nama, jenjang, id_prodi))
                conn.commit()
                messagebox.showinfo("Sukses", "Data Program Studi berhasil diperbarui!")
                self.refresh_table()
                self.bersihkan_form()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal: {e}")
            finally:
                cursor.close()
                conn.close()

    def hapus_data(self):
        self.ent_id.config(state="normal")
        id_prodi = self.ent_id.get().strip()
        self.ent_id.config(state="disabled")
        if not id_prodi or not messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus?"):
            return
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM m_program_studi WHERE id_prodi=%s", (id_prodi,))
                conn.commit()
                messagebox.showinfo("Sukses", "Data Program Studi berhasil dihapus!")
                self.refresh_table()
                self.bersihkan_form()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal: {e}")
            finally:
                cursor.close()
                conn.close()


if __name__ == "__main__":
    print("forms.py berhasil di-load")