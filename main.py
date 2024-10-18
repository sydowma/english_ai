from urllib.parse import urlparse, parse_qs

import speech_recognition as sr
from moviepy.editor import VideoFileClip
import openai
import os
import yt_dlp
import whisper

import config

# 设置你的OpenAI API密钥
openai.api_key = config.OPEN_AI_API_KEY


def download_youtube_video(url, output_path) -> tuple[str, str]:
    """从YouTube下载视频"""
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_path, '%(id)s.%(ext)s'),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return os.path.join(output_path, f"{info['id']}.wav"), info['id']
    except Exception as e:
        print(f"Error downloading YouTube video: {e}")
        return None


def transcribe_audio(audio_path: str, youtube_video_id: str, output_path: str):
    audio_txt = os.path.join(output_path, f'{youtube_video_id}.txt')
    if os.path.exists(audio_txt):
        with open(audio_txt, 'r') as file:
            return file.read()
    """使用Whisper将音频转换为文本"""
    print(f"Loading Whisper model..., path = {audio_path}")
    model = whisper.load_model("tiny")  # 可以选择不同大小的模型："tiny", "base", "small", "medium", "large"
    result = model.transcribe(audio_path)
    text = result["text"]
    print(f"Transcription: {text}")
    with open(audio_txt, 'w') as file:
        file.write(text)
    return text


def analyze_text(text):
    """使用OpenAI API分析文本"""

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": "You are a helpful assistant that analyzes essays and speeches. Provide feedback and a score out of 10."},
            {"role": "user",
             "content": f"Please analyze the following text, provide feedback on its structure, content, and language use, and give it a score out of 10:\n\n{text}"}
        ],
    )
    return response.choices[0].message.content


def extract_youtube_id(url):
    # 解析 URL
    parsed_url = urlparse(url)

    # 检查是否是 YouTube 域名
    if 'youtube.com' in parsed_url.netloc:
        # 从查询字符串中获取 'v' 参数
        query = parse_qs(parsed_url.query)
        return query.get('v', [None])[0]
    elif 'youtu.be' in parsed_url.netloc:
        # 短 URL 格式，视频 ID 在路径中
        return parsed_url.path.lstrip('/')
    else:
        return None


def main():
    input_type = input("Enter '1' for YouTube video, '2' for local video file, or '3' for text input: ")

    if input_type == '1':
        youtube_url = input("Enter the YouTube video URL: ")
        output_path = "downloads"
        os.makedirs(output_path, exist_ok=True)

        youtube_video_id = extract_youtube_id(youtube_url)
        absolute_output_path = os.path.abspath(output_path)
        audio_path = os.path.join(absolute_output_path, f'{youtube_video_id}.wav')
        if not os.path.exists(audio_path):
            print("Downloading YouTube video and extracting audio...")
            audio_path, youtube_video_id = download_youtube_video(youtube_url, absolute_output_path)

        print("Transcribing audio to text...")
        text = transcribe_audio(audio_path, youtube_video_id, output_path)

    elif input_type == '2':
        video_path = input("Enter the path to your local video file: ")
        audio_path = "temp_audio.wav"

        print("Extracting audio from video...")
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path)

        print("Transcribing audio to text...")
        text = transcribe_audio(audio_path, '', '')

        os.remove(audio_path)  # 清理临时音频文件
    elif input_type == '3':
        text = input("Enter your essay text: ")
    else:
        print("Invalid input type. Please enter '1', '2', or '3'.")
        return

    if text:
        print("Analyzing text...")
        analysis = analyze_text(text)
        print("\nAnalysis Result:")
        print(analysis)
    else:
        print("No text to analyze.")


if __name__ == "__main__":
    main()