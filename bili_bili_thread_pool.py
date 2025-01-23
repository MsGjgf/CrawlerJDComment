import json
import re
import subprocess
import threading
import time
import uuid

import requests
from lxml import etree
from tqdm import tqdm

from utils.custom_logger import logger

FFMPEG_PATH = r"E:\AllStudyExe\Python\ffmpeg-2024-10-27\bin\ffmpeg.exe"


def pi_pei():
    url = 'https://www.bilibili.com/bangumi/play/ss33626?t=1242&spm_id_from=333.788.top_right_bar_window_history.content.click'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'Referer': url,
        'Cookie': "buvid3=1C1BC5B2-006E-1A59-5713-886DA7A228EB42937infoc; b_nut=1712835742; "
                  "_uuid=8D1022CF1-6AED-AC76-1F8A-6B5A1107105610B43285infoc; "
                  "buvid4=468FA1FA-CBB4-5C9F-7F54-FEE3EABEA88443901-024041111-QNkT6TeeovUOz7Mw4HO0hw%3D%3D; "
                  "DedeUserID=213793137; DedeUserID__ckMd5=9b15a941ec0fce66; CURRENT_BLACKGAP=0; rpdid=|("
                  "k)~lmllmuu0J'u~uk)Jl~~Y; enable_web_push=ENABLE; iflogin_when_web_push=1; "
                  "header_theme_version=CLOSE; FEED_LIVE_VERSION=V_WATCHLATER_PIP_WINDOW3; buvid_fp_plain=undefined; "
                  "LIVE_BUVID=AUTO4617154310584985; home_feed_column=5; is-2022-channel=1; "
                  "fingerprint=500cd5faf91ce13e34cd2eec02e56a47; "
                  "SESSDATA=b9609e2b%2C1743670368%2C8667a%2Aa1CjD-L1nP279Je-bAPRzQ-2P_HBj5pFHzyvu5E"
                  "-JaVU2RnWZvTSTvwiZHsijfrZXFbUsSVmVCbmt3dExXaXQ0dmwwMk1kOXRWSzFEZzgwX01FbjNQOE5LWldFak9Td0gwUWt2d19nR1JnTW01S1F1aXdrRERUdmJlVGJleWpJbkdIZ0Q0Q0JQUG9nIIEC; bili_jct=98c05b382e6e2852e57ae41190859c9e; PVID=1; buvid_fp=500cd5faf91ce13e34cd2eec02e56a47; hit-dyn-v2=1; CURRENT_FNVAL=4048; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzAyMjQyODEsImlhdCI6MTcyOTk2NTAyMSwicGx0IjotMX0.hj5YKXRA7EHj8AO_l4MpwP9QeoQoZqmMrGBeLK9eSLE; bili_ticket_expires=1730224221; sid=5ebbo7ef; browser_resolution=1550-745; b_lsid=FD810A910D_192D3DB0FF1; bp_t_offset_213793137=993397709039730688; CURRENT_QUALITY=80"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"请求视频页面时出错: {e}")
        return

    res_text = response.text
    with open(r"static\b.html", "w", encoding="utf8") as f:
        f.write(res_text)

    tree = etree.HTML(res_text)
    scripts = tree.xpath("//script")

    playurlSSRData = None
    for script in scripts:
        if script.text:
            script_content = script.text.strip()
            if 'const playurlSSRData' in script_content:
                print(script_content)
                match = re.search(r'const\s+playurlSSRData\s*=\s*({[^;]*}}}})', script_content,
                                  re.DOTALL | re.MULTILINE)
                print(match.group(0))
                if match:
                    print("匹配到的内容: %s", match.group(0))
                    print("匹配到的组: %s", match.group(1))
                    json_str = match.group(1)
                    try:
                        playurlSSRData = json.loads(json_str)
                        print("Parsed playurlSSRData object:")
                        print(playurlSSRData)
                        video_list = playurlSSRData["result"]["video_info"]["dash"]["video"]
                        for i in range(len(video_list)):
                            print(video_list[i])
                        audio_list = playurlSSRData["result"]["video_info"]["dash"]["audio"]
                        for i in range(len(audio_list)):
                            print(audio_list[i])
                    except json.JSONDecodeError as e:
                        logger.error(f"解析 JSON 时出错: {e}")
                        logger.error(f"尝试解析的 JSON 字符串: {json_str}")
                    break  # 找到后退出循环

    if playurlSSRData is None:
        logger.info("未找到 playurlSSRData 对象")


def he_cheng(resolution, bitrate, output_file):
    global total_seconds
    start_time = time.time()
    logger.info(f"开始合并音视频，分辨率: {resolution}，比特率: {bitrate}")

    video_url = 'static/video/《好男人都死哪去了》，你送我鲜花 吃饭却要我刷卡！_video.mp4'
    audio_url = 'static/audio/《好男人都死哪去了》，你送我鲜花 吃饭却要我刷卡！_audio.mp4'

    ffmpeg_command = [
        FFMPEG_PATH,
        '-i', video_url,
        '-i', audio_url,
        '-vf', f'scale={resolution}',
        '-b:v', bitrate,
        '-c:v', 'libx264',
        '-c:a', 'aac',
        output_file
    ]

    # 启动FFmpeg进程
    process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                               encoding='utf-8')

    # 读取FFmpeg的输出并解析进度信息
    progress_pattern = re.compile(r'time=(\d{2}:\d{2}:\d{2}\.\d{2})')
    total_duration = None

    # 从FFmpeg输出中提取总时长
    for line in process.stdout:
        if 'Duration' in line:
            duration_match = re.search(r'Duration: (\d{2}:\d{2}:\d{2}\.\d{2})', line)
            if duration_match:
                total_duration = duration_match.group(1)
                total_seconds = sum(float(x) * 60 ** i for i, x in enumerate(reversed(total_duration.split(':'))))
                break

    # 如果找到了总时长，显示进度条
    if total_duration:
        with tqdm(total=total_seconds, unit='s', desc=f"Processing {resolution} {bitrate}") as pbar:
            for line in process.stdout:
                match = progress_pattern.search(line)
                if match:
                    current_time = match.group(1)
                    current_seconds = sum(
                        float(x) * 60 ** i for i, x in enumerate(reversed(current_time.split(':'))))
                    pbar.update(current_seconds - pbar.n)
                    pbar.set_description(f"Processing {resolution} {bitrate}: {current_time} / {total_duration}")
                    logger.info(f"Progress {resolution} {bitrate}: {current_time} / {total_duration}")

    # 等待FFmpeg进程结束
    process.wait()

    end_time = time.time()
    execution_time = end_time - start_time

    if process.returncode != 0:
        logger.error(f"FFmpeg process for {resolution} {bitrate} failed with return code {process.returncode}")
    else:
        logger.info(f"合并音视频完成，分辨率: {resolution}，比特率: {bitrate}，执行时间: {execution_time:.2f}秒")


def run_threads():
    resolutions = ['1920:1080', '1920:1080']
    bitrates = ['60000k', '6000k']

    threads = []

    for bitrate_index, bitrate in enumerate(bitrates):
        output_file = f'static/video/{uuid.uuid4()}_{bitrate}.mp4'
        thread = threading.Thread(target=he_cheng, args=(resolutions[bitrate_index], bitrate, output_file))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def get_duration(video_path):
    """ 获取视频的总时长 """
    result = subprocess.run([FFMPEG_PATH, '-i', video_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True,encoding='utf-8')
    match = re.search(r'Duration: (\d{2}:\d{2}:\d{2}\.\d{2})', result.stdout)
    if match:
        total_duration = match.group(1)
        total_seconds = sum(float(x) * 60 ** i for i, x in enumerate(reversed(total_duration.split(':'))))
        return total_seconds
    return None



if __name__ == "__main__":
    run_threads()
