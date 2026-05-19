import customtkinter as ctk
from tkinter import filedialog, messagebox
from downloader import YouTubeDownloader
import threading
import os

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("YouTube HD Downloader")
        self.geometry("600x450")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # UI 구성
        self.create_widgets()
        
        # 다운로더 엔진 초기화
        self.downloader = YouTubeDownloader(
            progress_callback=self.update_progress,
            logger_callback=self.update_log
        )

    def create_widgets(self):
        # 중앙 프레임
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # 제목
        self.label_title = ctk.CTkLabel(self.main_frame, text="YouTube Video Downloader", font=("Inter", 24, "bold"))
        self.label_title.pack(pady=(10, 20))

        # URL 입력 섹션
        self.url_label = ctk.CTkLabel(self.main_frame, text="YouTube URL:")
        self.url_label.pack(anchor="w", padx=20)
        self.url_entry = ctk.CTkEntry(self.main_frame, placeholder_text="https://www.youtube.com/watch?v=...", width=500)
        self.url_entry.pack(padx=20, pady=(0, 10))

        # 저장 경로 섹션
        self.path_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.path_frame.pack(fill="x", padx=20, pady=10)
        
        self.path_entry = ctk.CTkEntry(self.path_frame, placeholder_text="저장 경로 선택...", width=380)
        self.path_entry.insert(0, os.path.join(os.path.expanduser("~"), "Downloads"))
        self.path_entry.pack(side="left")
        
        self.path_button = ctk.CTkButton(self.path_frame, text="폴더 선택", width=100, command=self.browse_folder)
        self.path_button.pack(side="left", padx=(10, 0))

        # 형식 선택 섹션
        self.format_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.format_frame.pack(fill="x", padx=20, pady=10)
        
        self.format_label = ctk.CTkLabel(self.format_frame, text="형식:")
        self.format_label.pack(side="left")
        self.format_option = ctk.CTkOptionMenu(self.format_frame, values=["mp4", "mkv", "webm"])
        self.format_option.pack(side="left", padx=(10, 0))

        # 프로그레스 바
        self.progress_bar = ctk.CTkProgressBar(self.main_frame)
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", padx=20, pady=20)

        # 시작 버튼
        self.download_button = ctk.CTkButton(self.main_frame, text="다운로드 시작", font=("Inter", 16, "bold"), height=40, command=self.start_download_thread)
        self.download_button.pack(pady=10)

        # 로그 영역
        self.log_text = ctk.CTkTextbox(self.main_frame, height=100)
        self.log_text.pack(fill="both", padx=20, pady=(10, 10))
        self.log_text.configure(state="disabled")

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, folder)

    def update_progress(self, value):
        self.progress_bar.set(value)

    def update_log(self, message):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def start_download_thread(self):
        url = self.url_entry.get().strip()
        path = self.path_entry.get().strip()
        fmt = self.format_option.get()

        if not url:
            messagebox.showwarning("경고", "유튜브 URL을 입력해주세요.")
            return

        self.download_button.configure(state="disabled")
        self.update_progress(0)
        
        # 스레드 생성 및 시작
        thread = threading.Thread(target=self.run_download, args=(url, path, fmt))
        thread.daemon = True
        thread.start()

    def run_download(self, url, path, fmt):
        try:
            success = self.downloader.download(url, path, fmt)
            if success:
                messagebox.showinfo("성공", "다운로드가 완료되었습니다!")
            else:
                messagebox.showerror("실패", "다운로드 중 오류가 발생했습니다. 로그를 확인하세요.")
        finally:
            self.download_button.configure(state="normal")

if __name__ == "__main__":
    app = App()
    app.mainloop()
