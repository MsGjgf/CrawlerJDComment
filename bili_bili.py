# _*_ coding : utf-8 _*_
# @Time : 2024/10/28 0:15
# @Author : 哥几个佛
# @File : bili_bili
# @Project : CrawlerJDComment
import json
import os
import queue
import re
import subprocess
import sys
import time
import uuid

import requests
from lxml import etree
from tqdm import tqdm

from utils.custom_logger import logger
from utils.thread_pool import start_thread_pool_and_executor_tasks

# 定义非法字符及其替换字符
illegal_chars = {
    '<': '_',
    '>': '_',
    ':': '_',
    '"': '_',
    '/': '_',
    '\\': '_',
    '|': '_',
    '?': '_',
    '*': '_'
}

FFMPEG_PATH = r"E:\AllStudyExe\Python\ffmpeg-2024-10-27\bin\ffmpeg.exe"
FFPROBE_PATH = r"E:\AllStudyExe\Python\ffmpeg-2024-10-27\bin\ffprobe.exe"


def get_video_info(vide_file_path):
    """使用 ffprobe 获取视频信息"""
    command = [
        FFPROBE_PATH,
        '-v', 'quiet',  # 静默模式
        '-print_format', 'json',  # 输出格式为 JSON
        '-show_format',  # 显示格式信息
        '-show_streams',  # 显示流信息
        vide_file_path
    ]

    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8',
                                errors='replace')
        result.check_returncode()  # 检查命令是否成功执行
        video_info = json.loads(result.stdout)
        return video_info
    except subprocess.CalledProcessError as e:
        logger.error(f"调用 ffprobe 时出错: {e}")
        logger.error(f"命令: {' '.join(command)}")
        logger.error(f"返回码: {e.returncode}")
        logger.error(f"标准错误输出: {e.stderr}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"解析 JSON 时出错: {e}")
        return None


def parse_video_info(video_info):
    """解析视频信息"""
    if not video_info:
        return

    format_info = video_info.get('format', {})
    streams = video_info.get('streams', [])

    # 视频文件的基本信息
    logger.info("视频文件基本信息:")
    logger.info(f"文件名: {format_info.get('filename')}")
    logger.info(f"格式: {format_info.get('format_name')}")
    logger.info(f"持续时间: {format_info.get('duration')} 秒")
    logger.info(f"总比特率: {int(format_info.get('bit_rate')) // 1000} kbps")

    # 视频流信息
    for stream in streams:
        if stream['codec_type'] == 'video':
            logger.info("\n视频流信息:")
            logger.info(f"编解码器: {stream.get('codec_name')}")
            logger.info(f"分辨率: {stream.get('width')}x{stream.get('height')}")
            logger.info(f"比特率: {int(stream.get('bit_rate')) // 1000} kbps")
            logger.info(f"帧率: {stream.get('r_frame_rate')}")
            logger.info(f"编码格式: {stream.get('codec_tag_string')}")

        if stream['codec_type'] == 'audio':
            logger.info("\n音频流信息:")
            logger.info(f"编解码器: {stream.get('codec_name')}")
            logger.info(f"采样率: {stream.get('sample_rate')} Hz")
            logger.info(f"比特率: {int(stream.get('bit_rate')) // 1000} kbps")
            logger.info(f"通道数: {stream.get('channels')}")


def merge_files(log_path, video_file_path, audio_file_path, out_file_path, resolution=(1920, 1080), bitrate=6000000):
    """合并音视频并调整视频清晰度"""
    start_time = time.time()
    logger.info(f"开始合并音视频，分辨率: {resolution}，比特率: {bitrate}")

    ffmpeg_command = [
        FFMPEG_PATH,
        '-y',  # 添加此参数，用于在视频文件已存在时覆盖它
        '-i', video_file_path,
        '-i', audio_file_path,
        '-vf', 'scale={}:{}'.format(*resolution),
        '-b:v', '{}'.format(bitrate),
        '-c:v', 'libx264',
        '-c:a', 'aac',
        out_file_path
    ]

    # 启动FFmpeg进程
    process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                               encoding='utf-8')

    # 读取FFmpeg的输出并解析进度信息
    progress_pattern = re.compile(r'time=(\d{2}:\d{2}:\d{2}\.\d{2})')
    total_duration = None
    total_seconds = None

    # 从FFmpeg输出中提取总时长
    for line in process.stdout:
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(line)
            f.flush()  # 立即写入磁盘
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
        logger.info(f"合并音视频完成，分辨率: {resolution}，比特率: {bitrate}，合成执行时间: {execution_time:.2f}秒")


def download_file(url, file_path, headers):
    """下载文件并显示进度条"""
    try:
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()

        # 获取文件大小
        total_size = int(response.headers.get('content-length', 0))

        # 确保目录存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # 初始化进度条
        with tqdm(total=total_size, unit='B', unit_scale=True,
                  desc=f"Downloading {os.path.basename(file_path)}") as pbar:
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:  # 过滤掉保持活动的空chunk
                        f.write(chunk)
                        pbar.update(len(chunk))
    except requests.RequestException as e:
        logger.error(f"下载文件时出错: {e}")
        return False
    return True


def download_video_and_audio(video_url, audio_url, video_file_path, audio_file_path, headers):
    """下载视频和音频文件"""
    logger.info("开始下载视频和音频")

    if not download_file(video_url, video_file_path, headers):
        return False
    if not download_file(audio_url, audio_file_path, headers):
        return False

    logger.info("下载视频和音频完成")
    return True


def select_video_stream(info_dict, target_quality=80):
    """选择合适的视频流"""
    video_streams = None
    try:
        """短视频"""
        video_streams = info_dict["data"]["dash"]['video']
    except Exception:
        try:
            """电视剧"""
            video_streams = info_dict["result"]["video_info"]['dash']['video']
        except Exception:
            logger.error(f"视频流为None：{video_streams}")
    for stream in video_streams:
        if stream['id'] == target_quality:
            return stream
    logger.warning(f"没有找到质量为 {target_quality} 的视频流，选择默认的最高质量流")
    return video_streams[0]


def main(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/130.0.0.0 Safari/537.36',
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
    print(res_text)

    tree = etree.HTML(res_text)

    try:
        """短视频"""
        base_info = "".join(tree.xpath("/html/head/script[4]/text()"))[20:]
        print(base_info)
        info_dict = json.loads(base_info)

        # 标题
        title_json = "".join(tree.xpath("/html/head/script[5]/text()"))[25:]
        print(title_json)
        # 去掉多余的字符，只保留 JSON 部分
        json_str = title_json.split(';(function')[0]
        print(json_str)
        data = json.loads(json_str)
        title = data["videoData"]["title"]
    except Exception:
        try:
            """电视剧"""
            base_info = "".join(tree.xpath("/html/head/script[4]/text()"))
            print(base_info)
            match = re.search(r'const\s+playurlSSRData\s*=\s*({[^;]*}}}})', base_info, re.DOTALL | re.MULTILINE)
            info_dict = json.loads(match.group(1))
            print(info_dict)

            # 标题
            title = info_dict["result"]["play_view_business_info"]["episode_info"]["long_title"]
        except Exception:
            logger.error(f"没有该视频类型！")
            return

    # 替换非法字符
    title = ''.join(illegal_chars.get(char, char) for char in title)
    title = f"{title}-{uuid.uuid4()}"
    html_path = fr"static\b\{title}.html"  # html路径
    log_path = fr'static\b\{title}_ffmpeg_output.log'  # 日志路径
    video_file_path = fr"static\b\{title}_video.mp4"  # 视频路径
    audio_file_path = fr"static\b\{title}_audio.mp4"  # 音频路径
    out_file_path = fr"static\b\{title}.mp4"  # 音视频合成路径

    # 判断文件是否已存在，存在则使用uuid再存（所有）
    rand_uuid = str(uuid.uuid4()).replace("-", "")
    file_exists_list = [html_path, log_path, video_file_path, audio_file_path, out_file_path]
    for i, file_exists in enumerate(file_exists_list):
        if os.path.exists(file_exists):
            file_name, file_extension = os.path.splitext(file_exists)
            file_exists_list[i] = f"{file_name}_{rand_uuid}{file_extension}"
            sys.exit('😭')

    # 重新赋值
    html_path = file_exists_list[0]
    log_path = file_exists_list[1]
    video_file_path = file_exists_list[2]
    audio_file_path = file_exists_list[3]
    out_file_path = file_exists_list[4]

    # 记录html
    try:
        with open(html_path, "w", encoding="utf8") as f:
            f.write(res_text)
    except FileNotFoundError:
        directory = os.path.dirname(html_path)
        os.makedirs(directory)
        with open(html_path, "w", encoding="utf8") as f:
            f.write(res_text)

    # 选择合适的视频流
    target_quality = 80  # 可以根据需要调整
    selected_video_stream = select_video_stream(info_dict, target_quality)
    video_url = selected_video_stream["baseUrl"]
    try:
        """短视频"""
        audio_url = info_dict["data"]['dash']['audio'][0]["baseUrl"]
    except Exception:
        try:
            """电视剧"""
            audio_url = info_dict["result"]["video_info"]['dash']['audio'][0]["baseUrl"]
        except Exception:
            logger.error(f"没有该音频url！")
            return

    # 下载视频和音频
    if not download_video_and_audio(video_url, audio_url, video_file_path, audio_file_path, headers):
        return

    # 计算总比特率
    video_bitrate = selected_video_stream["bandwidth"]  # // 1000  # 单位转换为 kbps
    print("视频码率：", video_bitrate)
    try:
        """短视频"""
        audio_bitrate = info_dict["data"]['dash']['audio'][0]["bandwidth"]
    except Exception:
        try:
            """电视剧"""
            audio_bitrate = info_dict["result"]["video_info"]['dash']['audio'][0]["bandwidth"]  # // 1000  # 单位转换为 kbps
        except Exception:
            logger.error(f"没有该音频码率！")
            return
    print("音频码率：", audio_bitrate)
    total_bitrate = video_bitrate + audio_bitrate
    print("总码率：", total_bitrate)

    # 获取分辨率
    width = selected_video_stream.get('width', 1920)
    height = selected_video_stream.get('height', 1080)

    # 合并视频和音频
    merge_files(log_path, video_file_path, audio_file_path, out_file_path, resolution=(width, height),
                bitrate=total_bitrate)


if __name__ == '__main__':
    urls = queue.Queue()
    urls.put(
            f'https://www.bilibili.com/bangumi/play/ep456213?spm_id_from=333.337.0.0&from_spmid=666.25.episode.0')

    # 开启线程池并提交任务
    start_thread_pool_and_executor_tasks(task_queue=urls, target_method=main)
