import asyncio
import os

import requests
from bilibili_api import video
from moviepy import VideoFileClip, AudioFileClip

from config.Expection import BiliVideoTimeoutError, BiliVideoDownloadError
from config.regular_setting import regular_settings

SAVE_DIR =regular_settings.bili_local
os.makedirs(SAVE_DIR, exist_ok=True)

def merge_video_audio(video_path, audio_path, output_path):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    final_video = video.with_audio(audio)

    # 保存
    final_video.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac"
    )
    try:
        video.close()
    except:
        pass
    try:
        audio.close()
    except:
        pass
    try:
        final_video.close()
    except:
        pass
    os.remove(video_path)
    os.remove(audio_path)

def _download_file(url, path, headers, desc):
    resp = requests.get(url, headers=headers, stream=True, timeout=30)
    resp.raise_for_status()

    total = int(resp.headers.get("content-length", 0))
    with open(path, "wb") as f:
        for chunk in resp.iter_content(1024 * 1024):
            f.write(chunk)

async def do_download(id,maxd):
    # 获取视频下载地址
    v = video.Video(bvid=id)
    video_data= await v.get_info()
    download_url = await v.get_download_url(cid=video_data["cid"])
    if video_data["duration"]>maxd:
        raise BiliVideoTimeoutError
    dash = download_url["dash"]

    try:
        video_url = max(dash["video"], key=lambda x: x["bandwidth"])["baseUrl"]
        audio_url = max(dash["audio"], key=lambda x: x["bandwidth"])["baseUrl"]
        video_tmp = os.path.join(SAVE_DIR, f"{video_data['bvid']}_video.tmp")
        audio_tmp = os.path.join(SAVE_DIR, f"{video_data['bvid']}_audio.tmp")
        output_mp4 = os.path.join(SAVE_DIR, f"{video_data['bvid']}.mp4")

        headers = {
                "Referer": f"https://www.bilibili.com/video/{video_data['bvid']}",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }

        await asyncio.to_thread(_download_file, video_url, video_tmp, headers, "视频")
        await asyncio.to_thread(_download_file, audio_url, audio_tmp, headers, "音频")
        await asyncio.to_thread(merge_video_audio, video_tmp, audio_tmp, output_mp4)

    except Exception as e:
        raise BiliVideoDownloadError(e)

    return output_mp4
