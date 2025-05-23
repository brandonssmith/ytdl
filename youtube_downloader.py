import customtkinter as ctk
import subprocess
import os
from PIL import Image, ImageTk
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import json
import io
import sys

class YouTubeDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Get the directory where the script is located
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.ytdlp_path = os.path.join(self.script_dir, "yt-dlp.exe")

        # Check if yt-dlp.exe exists
        if not os.path.exists(self.ytdlp_path):
            messagebox.showerror(
                "Error",
                "yt-dlp.exe not found! Please download it from https://github.com/yt-dlp/yt-dlp and place it in the same directory as this script."
            )
            sys.exit(1)

        # Configure window
        self.title("YouTube Video Downloader")
        self.geometry("800x600")  # Increased window size
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="YouTube Video Downloader",
            font=("Helvetica", 24, "bold")
        )
        self.title_label.grid(row=0, column=0, pady=20)

        # URL Entry
        self.url_frame = ctk.CTkFrame(self.main_frame)
        self.url_frame.grid(row=1, column=0, pady=10, padx=20, sticky="ew")
        self.url_frame.grid_columnconfigure(1, weight=1)

        self.url_label = ctk.CTkLabel(self.url_frame, text="Video URL:")
        self.url_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.url_entry = ctk.CTkEntry(self.url_frame, placeholder_text="Enter YouTube URL here...")
        self.url_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.url_entry.bind('<KeyRelease>', self.on_url_change)

        # Preview Frame
        self.preview_frame = ctk.CTkFrame(self.main_frame)
        self.preview_frame.grid(row=2, column=0, pady=10, padx=20, sticky="nsew")
        self.preview_frame.grid_columnconfigure(0, weight=1)
        self.preview_frame.grid_rowconfigure(0, weight=1)

        self.preview_label = ctk.CTkLabel(self.preview_frame, text="Video Preview")
        self.preview_label.grid(row=0, column=0, padx=5, pady=5)

        self.preview_image = ctk.CTkLabel(self.preview_frame, text="")
        self.preview_image.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Download Location
        self.location_frame = ctk.CTkFrame(self.main_frame)
        self.location_frame.grid(row=3, column=0, pady=10, padx=20, sticky="ew")
        self.location_frame.grid_columnconfigure(1, weight=1)

        self.location_label = ctk.CTkLabel(self.location_frame, text="Save Location:")
        self.location_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.location_entry = ctk.CTkEntry(self.location_frame, placeholder_text="Select download location...")
        self.location_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.browse_button = ctk.CTkButton(
            self.location_frame,
            text="Browse",
            command=self.browse_location
        )
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)

        # Download Button
        self.download_button = ctk.CTkButton(
            self.main_frame,
            text="Download",
            command=self.start_download
        )
        self.download_button.grid(row=4, column=0, pady=20)

        # Progress Frame
        self.progress_frame = ctk.CTkFrame(self.main_frame)
        self.progress_frame.grid(row=5, column=0, pady=10, padx=20, sticky="ew")
        self.progress_frame.grid_columnconfigure(0, weight=1)

        self.progress_label = ctk.CTkLabel(self.progress_frame, text="")
        self.progress_label.grid(row=0, column=0, padx=5, pady=5)

        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.progress_bar.set(0)

        # Set default download location
        self.download_location = os.path.expanduser("~/Downloads")
        self.location_entry.insert(0, self.download_location)

    def browse_location(self):
        folder = filedialog.askdirectory(initialdir=self.download_location)
        if folder:
            self.download_location = folder
            self.location_entry.delete(0, tk.END)
            self.location_entry.insert(0, folder)

    def on_url_change(self, event=None):
        url = self.url_entry.get()
        if url:
            thread = threading.Thread(target=self.update_preview, args=(url,))
            thread.daemon = True
            thread.start()

    def update_preview(self, url):
        try:
            # Get video info for thumbnail and title
            info_command = [
                self.ytdlp_path,
                "--dump-json",
                url
            ]
            
            info_process = subprocess.Popen(
                info_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            info_output, info_error = info_process.communicate()
            
            if info_process.returncode == 0:
                video_info = json.loads(info_output)
                thumbnail_url = video_info.get('thumbnail')
                
                if thumbnail_url:
                    # Download thumbnail
                    response = requests.get(thumbnail_url)
                    if response.status_code == 200:
                        # Convert to PIL Image
                        image = Image.open(io.BytesIO(response.content))
                        
                        # Resize image to fit preview frame
                        preview_size = (400, 225)  # 16:9 aspect ratio
                        image.thumbnail(preview_size, Image.Resampling.LANCZOS)
                        
                        # Convert to PhotoImage
                        photo = ImageTk.PhotoImage(image)
                        
                        # Update preview
                        self.preview_image.configure(image=photo)
                        self.preview_image.image = photo  # Keep a reference
                        
                        # Update title if available
                        title = video_info.get('title', '')
                        if title:
                            self.preview_label.configure(text=title)
                
        except Exception as e:
            self.preview_label.configure(text=f"Preview error: {str(e)}")
            print(f"Error details: {str(e)}")  # For debugging

    def start_download(self):
        url = self.url_entry.get()
        if not url:
            self.progress_label.configure(text="Please enter a URL")
            return

        # Verify download location exists
        if not os.path.exists(self.download_location):
            try:
                os.makedirs(self.download_location)
            except Exception as e:
                messagebox.showerror("Error", f"Could not create download directory: {str(e)}")
                return

        # Disable the download button while downloading
        self.download_button.configure(state="disabled")
        self.progress_label.configure(text="Starting download...")
        self.progress_bar.set(0)

        # Start download in a separate thread
        thread = threading.Thread(target=self.download_video, args=(url,))
        thread.daemon = True
        thread.start()

    def download_video(self, url):
        try:
            # Ensure the download location path is properly formatted
            output_template = os.path.join(self.download_location, "%(title)s.%(ext)s")
            
            command = [
                self.ytdlp_path,
                "-o", output_template,
                "--no-check-certificates",  # Add this to handle some SSL issues
                url
            ]

            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.progress_label.configure(text=output.strip())
                    self.update()

            if process.returncode == 0:
                self.progress_label.configure(text=f"Download completed successfully! Saved to: {self.download_location}")
            else:
                error_output = process.stderr.read()
                self.progress_label.configure(text=f"Download failed: {error_output}")

        except Exception as e:
            self.progress_label.configure(text=f"Error: {str(e)}")
        finally:
            self.download_button.configure(state="normal")
            self.progress_bar.set(1)

if __name__ == "__main__":
    app = YouTubeDownloader()
    app.mainloop() 