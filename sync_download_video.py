import json
import os
import re
import subprocess

import requests
from requests.cookies import RequestsCookieJar


save_file = []

if "ffmpeg" in os.environ.keys():
    os.environ.setdefault("ffmpeg", "ffmpeg-7.0.1-full_build\\ffmpeg-7.0.1-full_build\\bin")    


def get_response(url):
    cookies = "buvid3=F6349542-0179-1707-5327-843F67B3883566783infoc; b_nut=1714478366; _uuid=46C473FE-E486-1E910-75E9-8BEBFC74592967093infoc; enable_web_push=DISABLE; buvid4=460070C8-EAD2-167A-3F8B-2C88452A644868656-024043011-3%2BO7QFQeGyVSd3CLiFbw1A%3D%3D; rpdid=|(JYYRYkYmRY0J'u~uRR~)~|J; buvid_fp_plain=undefined; DedeUserID=488647888; DedeUserID__ckMd5=f3d15b29010fde6a; header_theme_version=CLOSE; PVID=1; CURRENT_FNVAL=4048; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjA2ODQ0NjMsImlhdCI6MTcyMDQyNTIwMywicGx0IjotMX0.ibIkMw4eyRm6nezPgOvGpdzW1wcEPEaiUQ0cJuM3tsY; bili_ticket_expires=1720684403; SESSDATA=b9bb4fe2%2C1735981186%2Cb2d31%2A72CjCXaKiGnZA_k3XneoB4MSoulwvAlpy5HtWRZoT7aUqF-zHUqgADIgHlScGH0mGLvroSVmFidGFTZ25LbzBHazBRN1FmbmlicFYzMEFkUTNJMXdIa1lCbVlLYmo1czBnSlBmdUdHX2tVSnprRFVSQm5HVS1sZ1lmYmRBWVpvd1pyMWRadGt6d21nIIEC; bili_jct=01a22b5d086876aba5080dcf10f59b47; CURRENT_QUALITY=80; bp_t_offset_488647888=952432770531983360; b_lsid=E8937427_1909CC4278E; sid=8ldj3lfo; fingerprint=c3c0883f732378eb8098ef27c34f77b5; buvid_fp=c3c0883f732378eb8098ef27c34f77b5; bsource=search_bing; home_feed_column=5; browser_resolution=1498-269"
    jar = RequestsCookieJar(cookies)
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

def merge_videos(input_files, output_file):
    print(f"Start merge video {input_files[1]}")
    command = f"ffmpeg -i {input_files[1]} -i {input_files[0]} -c:v copy -c:a aac -strict experimental -safe 0 -y {output_file}output.mp4"
    subprocess.run(command, shell=True)  
    subprocess.run(command, shell=True)
    print(f"successfully merge video {output_file}output.mp4")
    os.remove(input_files[0])
    os.remove(input_files[1])


def main(url, file):
    audio_url, video_url, title = get_video_info(url)
    try:
        with open(f"{file}\\{title}output.mp4", "rb"):
            pass
    except FileNotFoundError:
        # 若有异常，说明没有下载
        if not os.path.isdir(f"{file}\\"):
            os.makedirs(f"{file}\\")
        save(audio_url, video_url, title, file=f"D:\\b站学习资料\\{file}\\")
        merge_videos([f"{file}\\{title}.mp3", 
                      f"{file}\\{title}.mp4"], 
                      f"{file}\\{title}.mp4")
        pass
    except:
        pass
    else:
        # 反之，则已有文件，不必下载
        print(f"{title}曾经下载过，不再下载")
