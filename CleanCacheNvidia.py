import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sys
import ctypes
import threading

# === ĐƯỜNG DẪN ===
CACHE_DIR = os.path.expanduser(r"~\AppData\Local\NVIDIA\DXCache")
TASK_NAME = "NVIDIA_DXCache_Cleaner"
VBS_FILE = os.path.join(os.getenv("TEMP"), "dxcache_cleaner.vbs")
PS1_FILE = os.path.join(os.getenv("TEMP"), "dxcache_cleaner.ps1")  # MỚI
LOG_FILE = os.path.join(os.getenv('TEMP'), "dxcache_log.txt")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

class DXCacheUltimate:
    def __init__(self, root):
        self.root = root
        self.root.title("DXCache Cleaner Ultimate - ẨN 100% (PS1 + VBS)")
        self.root.geometry("820x780")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a1a")
        self.total_minutes = 30
        self.setup_ui()
        self.load_existing_task()
        self.update_display()

    def setup_ui(self):
        # [Giữ nguyên toàn bộ UI như cũ - không thay đổi]
        title = tk.Label(self.root, text="NVIDIA DXCache Cleaner", font=("Segoe UI", 20, "bold"), fg="#00ff88", bg="#1a1a1a")
        title.pack(pady=20)

        path_frame = tk.Frame(self.root, bg="#1a1a1a")
        path_frame.pack(pady=10, fill="x", padx=40)
        tk.Label(path_frame, text="Thư mục cache:", font=("Consolas", 10), fg="#cccccc", bg="#1a1a1a").pack(anchor="w")
        path_lbl = tk.Label(path_frame, text=CACHE_DIR, font=("Consolas", 10), fg="#00ccff", bg="#1a1a1a", cursor="hand2", wraplength=500)
        path_lbl.pack(anchor="w", pady=(2,0))
        def open_cache_folder(e=None):
            try: os.startfile(os.path.dirname(CACHE_DIR))
            except: messagebox.showerror("Lỗi", "Không mở được thư mục.")
        path_lbl.bind("<Button-1>", open_cache_folder)

        log_info = tk.Label(self.root, text=f"Log: {LOG_FILE}", font=("Consolas", 9), fg="#ffaa00", bg="#1a1a1a", cursor="hand2")
        log_info.pack(pady=(0,10))
        log_info.bind("<Button-1>", lambda e: self.open_log())

        self.task_info_label = tk.Label(self.root, text="Task: Chưa tạo", font=("Segoe UI", 10, "bold"), fg="#ff6666", bg="#1a1a1a")
        self.task_info_label.pack(pady=5)

        input_frame = tk.LabelFrame(self.root, text=" Thời gian lặp lại (phút/giờ) ", font=("Segoe UI", 12, "bold"), fg="#ffffff", bg="#2d2d2d", padx=20, pady=15)
        input_frame.pack(pady=15, fill="x", padx=40)

        slider_frame = tk.Frame(input_frame, bg="#2d2d2d")
        slider_frame.pack(pady=10)
        self.slider_var = tk.IntVar(value=30)
        self.slider = ttk.Scale(slider_frame, from_=1, to=60, variable=self.slider_var, orient="horizontal", length=480, command=self.on_slider)
        self.slider.pack()

        entry_unit_frame = tk.Frame(input_frame, bg="#2d2d2d")
        entry_unit_frame.pack(pady=8)
        self.entry = tk.Entry(entry_unit_frame, font=("Consolas", 12), width=8, justify="center", bg="#111111", fg="#00ff88", insertbackground="#00ff88")
        self.entry.pack(side="left", padx=5)
        self.entry.insert(0, "30")
        self.entry.bind("<KeyRelease>", self.on_entry)

        unit_frame = tk.Frame(entry_unit_frame, bg="#2d2d2d")
        unit_frame.pack(side="left", padx=10)
        self.unit_var = tk.StringVar(value="phút")
        for text in ["phút", "giờ"]:
            rb = tk.Radiobutton(unit_frame, text=text, variable=self.unit_var, value=text, fg="#cccccc", bg="#2d2d2d", selectcolor="#00ff88", command=self.on_unit_change)
            rb.pack(side="left", padx=15)

        self.display_label = tk.Label(input_frame, text="", font=("Segoe UI", 14, "bold"), fg="#00ff88", bg="#2d2d2d")
        self.display_label.pack(pady=10)

        btn_frame = tk.Frame(self.root, bg="#1a1a1a")
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="TẠO TASK (ẨN 100%)", font=("Segoe UI", 12, "bold"), bg="#00ff44", fg="black", width=22, height=2,
                  command=lambda: threading.Thread(target=self.create_task, daemon=True).start()).pack(side="left", padx=10)
        tk.Button(btn_frame, text="XÓA TASK", font=("Segoe UI", 12, "bold"), bg="#ff4444", fg="white", width=15, height=2,
                  command=lambda: threading.Thread(target=self.delete_task, daemon=True).start()).pack(side="left", padx=10)
        tk.Button(btn_frame, text="TEST NGAY", font=("Segoe UI", 10, "bold"), bg="#ffaa00", fg="black", width=12, height=2, command=self.test_now).pack(side="left", padx=10)
        tk.Button(btn_frame, text="XEM LOG", font=("Segoe UI", 10, "bold"), bg="#44aaff", fg="white", width=12, height=2, command=self.open_log).pack(side="left", padx=10)

        self.status_label = tk.Label(self.root, text="Sẵn sàng", font=("Segoe UI", 11), fg="#aaaaaa", bg="#1a1a1a")
        self.status_label.pack(pady=5)

        log_frame = tk.LabelFrame(self.root, text=" Nhật ký ứng dụng ", font=("Segoe UI", 10, "bold"), fg="#ffffff", bg="#2d2d2d", padx=10, pady=8)
        log_frame.pack(pady=10, fill="both", expand=True, padx=40)
        self.log_text = tk.Text(log_frame, height=9, bg="#0a0a0a", fg="#00ff88", font=("Consolas", 9))
        scrollbar = tk.Scrollbar(log_frame, command=self.log_text.yview)
        self.log_text.config(yscrollcommand=scrollbar.set)
        self.log_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.log("ỨNG DỤNG KHỞI ĐỘNG - DÙNG .PS1 + .VBS (ỔN ĐỊNH 100%)")

    def log(self, msg):
        t = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{t}] {msg}\n")
        self.log_text.see("end")

    def open_log(self):
        try: os.startfile(LOG_FILE)
        except: subprocess.run(['notepad.exe', LOG_FILE], shell=True)

    def load_existing_task(self):
        if self.check_task_exists():
            self.task_info_label.config(text="Task: Đã tạo & đang chạy", fg="#00ff88")
            self.log("Phát hiện task hiện có")
        else:
            self.task_info_label.config(text="Task: Chưa tạo", fg="#ff6666")

    def update_total_minutes(self):
        try:
            val = int(self.entry.get() or "1")
            if val < 1: val = 1
            if val > 60: val = 60
            self.entry.delete(0, tk.END)
            self.entry.insert(0, str(val))
            self.slider_var.set(val)
            unit = self.unit_var.get()
            self.total_minutes = val if unit == "phút" else val * 60
        except: pass

    def on_slider(self, *args):
        val = int(self.slider_var.get())
        self.entry.delete(0, tk.END)
        self.entry.insert(0, str(val))
        self.update_total_minutes()
        self.update_display()

    def on_entry(self, *args):
        self.update_total_minutes()
        self.update_display()
        if int(self.entry.get() or "0") >= 60 and self.unit_var.get() == "phút":
            self.unit_var.set("giờ")
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "1")

    def on_unit_change(self):
        self.update_total_minutes()
        self.update_display()

    def update_display(self):
        self.update_total_minutes()
        hrs = self.total_minutes // 60
        mins = self.total_minutes % 60
        parts = []
        if hrs: parts.append(f"{hrs} giờ")
        if mins: parts.append(f"{mins} phút")
        self.display_label.config(text=" + ".join(parts) if parts else "1 phút")

    def check_task_exists(self):
        try:
            result = subprocess.run(['schtasks', '/query', '/tn', TASK_NAME], capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False

    # TẠO FILE .PS1 RIÊNG
    def create_ps_script(self):
        content = f'''# DXCache Cleaner Script - Auto delete after 100s
    $Log = "{LOG_FILE}"
    $Cache = "{CACHE_DIR}"

    Add-Content -Path $Log -Value "[$(Get-Date)] START CLEANING DXCACHE"

    if (Test-Path $Cache) {{
        Remove-Item $Cache -Recurse -Force -ErrorAction SilentlyContinue
        Add-Content -Path $Log -Value "[$(Get-Date)] DXCACHE DELETED SUCCESSFULLY"
    }} else {{
        Add-Content -Path $Log -Value "[$(Get-Date)] CACHE FOLDER NOT FOUND"
    }}

    Add-Content -Path $Log -Value "[$(Get-Date)] CLEANING FINISHED"

    Start-Sleep -Seconds 100
    if (Test-Path $Log) {{
        Remove-Item $Log -Force -ErrorAction SilentlyContinue
    }}
    '''
        try:
            with open(PS1_FILE, "w", encoding="utf-8", errors="ignore") as f:
                f.write(content)
            return PS1_FILE
        except Exception as e:
            self.log(f"Lỗi tạo .ps1: {e}")
            return None
        


    # TẠO .VBS GỌI .PS1 ẨN HOÀN TOÀN
    def create_vbs_launcher(self):
        ps_file = self.create_ps_script()
        if not ps_file:
            return None

        vbs_content = f'''Set WshShell = CreateObject("WScript.Shell")
    WshShell.Run "powershell -ExecutionPolicy Bypass -File ""{ps_file}""", 0, False
    Set WshShell = Nothing'''

        try:
            with open(VBS_FILE, "w", encoding="utf-8") as f:
                f.write(vbs_content)
            return VBS_FILE
        except Exception as e:
            self.log(f"Lỗi tạo .vbs: {e}")
            return None

    def create_task(self):
        if not is_admin():
            messagebox.showerror("Quyền hạn", "Chạy bằng quyền Administrator!")
            return

        if self.check_task_exists():
            if not messagebox.askyesno("Xác nhận", "Task đã tồn tại. Ghi đè?"):
                return
            self.delete_task(silent=True)

        vbs_file = self.create_vbs_launcher()
        if not vbs_file:
            return

        mins = max(1, self.total_minutes)

        cmd = [
            'schtasks', '/create', '/f', '/tn', TASK_NAME,
            '/tr', f'wscript.exe "{vbs_file}"',
            '/sc', 'minute', '/mo', str(mins),
            '/rl', 'HIGHEST'
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            self.log(f"TASK TẠO THÀNH CÔNG! Mỗi {mins} phút - ẨN 100%")
            self.load_existing_task()
            messagebox.showinfo("Thành công",
                f"Task đã tạo!\n"
                f"Mỗi: {self.display_label.cget('text')}\n"
                f"Không flash CMD/PS\n"
                f"Dùng .ps1 riêng (ổn định)\n"
                f"Log tự xóa sau 100s")
        except Exception as e:
            self.log(f"Lỗi: {e}")
            messagebox.showerror("Lỗi", "Chạy bằng Admin!")

    def delete_task(self, silent=False):
        try:
            subprocess.run(['schtasks', '/delete', '/tn', TASK_NAME, '/f'], check=True, capture_output=True)
            for file in [VBS_FILE, PS1_FILE]:
                if os.path.exists(file):
                    try: os.remove(file)
                    except: pass
            if not silent:
                self.log("TASK + FILE .VBS/.PS1 ĐÃ XÓA")
                self.load_existing_task()
                messagebox.showinfo("Xong", "Task và file tạm đã xóa!")
        except:
            if not silent: messagebox.showerror("Lỗi", "Không xóa được")

    def test_now(self):
        vbs_file = self.create_vbs_launcher()
        if not vbs_file:
            return
        try:
            subprocess.Popen(['wscript.exe', vbs_file], creationflags=subprocess.CREATE_NO_WINDOW)
            self.log("TEST: Đang xóa cache (ẩn hoàn toàn)...")
            messagebox.showinfo("Test", "Đã chạy thử! (Không thấy gì là đúng)")
        except Exception as e:
            self.log(f"Test lỗi: {e}")

if __name__ == "__main__":
    if os.name != "nt":
        messagebox.showerror("Lỗi", "Chỉ Windows!")
    else:
        root = tk.Tk()
        app = DXCacheUltimate(root)
        root.mainloop()