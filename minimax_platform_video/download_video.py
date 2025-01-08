import argparse

import csv
import requests


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert the image to video')
    parser.add_argument('--csv_file_path', type=str, help='The input excel file')
    parser.add_argument('--output_path', type=str, help='The output path')
    args = parser.parse_args()

    # 从CSV文件读取数据
    with open(args.csv_file_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            # 获取视频任务ID和下载URL
            video_task_id = row['video_task_id']
            result = eval(row['result'])  # 将字符串转换为字典
            video_url = result[0]['url']

            # 下载视频
            video_response = requests.get(video_url)
            if video_response.status_code == 200:
                video_filename = f"{args.output_path}{video_task_id}.mp4"
                with open(video_filename, 'wb') as video_file:
                    video_file.write(video_response.content)
                print(f"视频已下载: {video_filename}")
            else:
                print(f"视频下载失败: {video_url}")