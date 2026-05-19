import yt_dlp
import os

class YouTubeDownloader:
    def __init__(self, progress_callback=None, logger_callback=None):
        self.progress_callback = progress_callback
        self.logger_callback = logger_callback

    def log(self, message):
        if self.logger_callback:
            self.logger_callback(message)
        else:
            print(message)

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%').replace('%','')
            try:
                percent = float(p)
                if self.progress_callback:
                    self.progress_callback(percent / 100)
            except ValueError:
                pass
        elif d['status'] == 'finished':
            self.log("다운로드 완료. 파일 병합 중...")

    def download(self, url, save_path, file_format='mp4'):
        # 저장 경로 생성
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # FFmpeg 경로 수동 지정 (winget 설치 경로)
        ffmpeg_path = r'C:\Users\user\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin'
        
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
            'merge_output_format': file_format,
            'progress_hooks': [self.progress_hook],
            'logger': self,
            'ffmpeg_location': ffmpeg_path, # FFmpeg 위치 강제 지정
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.log(f"정보 가져오는 중: {url}")
                ydl.download([url])
            self.log("모든 작업이 성공적으로 완료되었습니다.")
            return True
        except Exception as e:
            self.log(f"에러 발생: {str(e)}")
            return False

    # Logger interface for yt-dlp
    def debug(self, msg):
        if not msg.startswith('[debug]'):
            self.log(msg)
    
    def warning(self, msg):
        self.log(f"경고: {msg}")

    def error(self, msg):
        self.log(f"에러: {msg}")
