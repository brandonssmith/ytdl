# YouTube Video Downloader GUI

A simple and modern graphical user interface for downloading YouTube videos using yt-dlp in Windows. I suppose that it could work in another OS but I specifically built it for the Windows compatible command line app.

## Requirements

- Python 3.7 or higher
- yt-dlp.exe - you can find that at the actual yt-dlp page here: https://github.com/yt-dlp/yt-dlp
- Required Python packages (listed in requirements.txt)

## Setup

1. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

2. Make sure `yt-dlp.exe` is in the same directory as the Python script.

## Usage

1. Run the application:
   ```
   python youtube_downloader.py
   ```

2. Enter the YouTube video URL in the input field.

3. Select your preferred download format:
   - `best`: Best quality (default)
   - `bestvideo+bestaudio`: Best video and audio quality (may download separately)
   - `bestvideo`: Best video quality only
   - `bestaudio`: Best audio quality only

4. Click the "Download" button to start the download.

5. Monitor the progress in the progress bar and status label.

## Notes

- Downloads will be saved in the same directory as the script.
- The application uses threading to prevent freezing during downloads.
- Progress updates are shown in real-time. 
