import os
import ssl
import time
import certifi
from pytube import YouTube
from pytube.cli import on_progress

# 配置全局 SSL 上下文使用 certifi 的证书
ssl._create_default_https_context = ssl._create_unverified_context


def progress_function(stream, chunk, bytes_remaining):
    # 获取视频总大小
    total_size = stream.filesize
    # 已下载大小
    bytes_downloaded = total_size - bytes_remaining

    # 计算下载进度
    percentage_of_completion = bytes_downloaded / total_size * 100
    # 计算下载速度
    elapsed_time = time.time() - progress_function.start_time
    download_speed = bytes_downloaded / elapsed_time if elapsed_time > 0 else 0

    # 打印进度信息
    print(
        f"进度: {percentage_of_completion:.2f}% | 已下载: {bytes_downloaded / 1024 / 1024:.2f} MB / {total_size / 1024 / 1024:.2f} MB | 下载速度: {download_speed / 1024:.2f} KB/s",
        end='\r')


def download_youtube_video(url, save_path):
    try:
        # 创建 YouTube 对象
        yt = YouTube(url, on_progress_callback=progress_function)

        # 获取最高质量的视频流
        stream = yt.streams.get_highest_resolution()

        # 初始化开始时间
        progress_function.start_time = time.time()

        # 下载视频
        stream.download(output_path=save_path)

        print(f"\n视频下载完成: {yt.title}")
    except Exception as e:
        print(f"下载视频出错: {e}")


# 示例用法
video_url = 'https://www.youtube.com/watch?v=jCb5YrmLN70&list=LL'  # 替换为你要下载的视频URL
save_path = '/Users/Desktop'  # 替换为你的 macOS 用户名

download_youtube_video(video_url, save_path)

