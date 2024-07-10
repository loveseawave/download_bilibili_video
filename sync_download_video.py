import json
import os
import re
import subprocess

import requests
import ffmpeg


save_file = []

if "ffmpeg" in os.environ.keys():
    os.environ.setdefault("ffmpeg", "ffmpeg-7.0.1-full_build\\ffmpeg-7.0.1-full_build\\bin")    


def get_response(url):
    headers = {
        "referer": "https://www.bilibili.com", 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
    }
    response = requests.get(url=url, headers=headers)
    return response


def get_video_info(url):
    response = get_response(url)
    title = re.findall('<h1 data-title="(.*?)"', response.text, re.S)[0]
    html_data = re.findall('<script>window.__playinfo__=(.*?)</script>', 
               response.text, re.S)[0]
    json_data = json.loads(html_data)
    audio_url, video_url = parse_json(json_data)
    return [audio_url, video_url, title]


def parse_json(json):
    audio_url = json['data']['dash']['audio'][0]['base_url']
    video_url = json['data']['dash']['video'][0]['base_url']
    return [audio_url, video_url]


def save(audio_url, video_url, title, file=""):
    global save_file
    save_file = [f"{file}{title}.mp3", f"{file}{title}.mp4"]
    audio_content = get_response(audio_url).content
    video_content = get_response(video_url).content
    with open(save_file[0], "wb") as fp:
        fp.write(audio_content)

    with open(save_file[1], "wb") as fp:
        fp.write(video_content)

    print(f'Successfully download {title}.')


def merge_data(video_name):
    """print(f"Start merge video {video_name}.")
    cmd = f'ffmpeg -i {video_name}.mp4 -i {video_name}.mp3 -c:v copy -c:a aac -strict experimental {video_name}output.mp4'
    subprocess.getoutput("cd ffmpeg-7.0.1-full_build\ffmpeg-7.0.1-full_build\bin")
    subprocess.getoutput(cmd)
    audio_file, video_file = save_file
    os.remove(audio_file)
    os.remove(video_file)
    print(f"Finish merge {video_name}.")"""


def main(url):
    audio_url, video_url, title = get_video_info(url)
    save(audio_url, video_url, title)
    merge_data(title)

# 测试：main("https://www.bilibili.com/video/BV15whXe3ETa/?spm_id_from=333.337.search-card.all.click&vd_source=368b79f1a715cb7a2ebd277c81c0c0f3")
