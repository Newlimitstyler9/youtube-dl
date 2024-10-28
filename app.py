from flask import Flask, request, jsonify, send_file
from yt_dlp import YoutubeDL
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/download-audio', methods=['POST'])
def download_audio():
    logging.info("Received a request")
    data = request.get_json()
    youtube_url = data.get("youtube_url")
    
    if not youtube_url:
        logging.error("YouTube URL is missing in the request")
        return jsonify({"error": "YouTube URL is required"}), 400

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '/tmp/%(title)s.%(ext)s',  # Temporary directory
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            audio_file_path = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')

        return send_file(audio_file_path, as_attachment=True)

    except Exception as e:
        logging.error(f"Error downloading audio: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
