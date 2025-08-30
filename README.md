# yt_downloader

A simple and modern graphical user interface for downloading YouTube videos using yt-dlp.

## Features

- **Automatic Updates**: Built-in updater to keep yt-dlp.exe current
- **Video Preview**: Shows video thumbnail and title before downloading
- **Custom Download Location**: Choose where to save your downloads
- **Modern Interface**: Clean, responsive GUI built with customtkinter
- **Progress Tracking**: Real-time download progress and status updates

## Requirements

- Python 3.7 or higher
- yt-dlp.exe (must be downloaded from [yt-dlp GitHub repository](https://github.com/yt-dlp/yt-dlp))
- Required Python packages (listed in requirements.txt)

## Setup

1. Download the latest yt-dlp.exe from the [yt-dlp GitHub repository](https://github.com/yt-dlp/yt-dlp)
   - Go to the releases page
   - Download the latest Windows executable (yt-dlp.exe)
   - Place it in the same directory as this application

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Make sure `yt-dlp.exe` is in the same directory as the Python script.

## Usage

1. Run the application:
   ```
   python youtube_downloader.py
   ```

2. **Check for Updates** (Optional):
   - The app automatically checks your yt-dlp version on startup
   - Click "Check for Updates" to manually check for newer versions
   - Updates are downloaded and installed automatically with safety backups

3. Enter the YouTube video URL in the input field.

4. The app will automatically:
   - Load the video preview (thumbnail and title)
   - Display the current yt-dlp version status

5. Select your preferred download location using the Browse button.

6. Click the "Download" button to start the download.

7. Monitor the progress in the progress bar and status label.

## Update System

The application includes an automatic update system for yt-dlp:

- **Automatic Version Check**: On startup, displays current yt-dlp version
- **Manual Update Check**: Click "Check for Updates" to search for newer versions
- **Safe Updates**: Creates backups before updating and can rollback if needed
- **GitHub Integration**: Directly downloads the latest Windows executable from official releases
- **Status Display**: Shows update progress and results in real-time

## Notes

- Downloads will be saved in your selected directory.
- The application uses threading to prevent freezing during downloads.
- Progress updates are shown in real-time.
- yt-dlp.exe is automatically kept up-to-date through the built-in updater.
- The update system creates automatic backups for safety.
- If you prefer manual updates, you can still download yt-dlp.exe manually from the GitHub repository. 
