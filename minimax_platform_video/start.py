# -*- coding: utf-8 -*-
import argparse
import asyncio

from minimax_platform_video.reporting.console_workflow_callbacks import ConsoleWorkflowCallbacks
from minimax_platform_video.reporting.runner_callbacks import RunnerCallbacks
from minimax_platform_video.task import convert_image_to_video, convert_text_generator
import pandas as pd
import os
import sys
import logging.config


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)])


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Convert the image to video')
    parser.add_argument('--input_excel', type=str, help='The input excel file')
    parser.add_argument('--output_path', type=str, help='The output path')
    parser.add_argument('--prompt_num_threads', type=int, default=2, help='The number of threads for prompt')
    parser.add_argument('--video_num_threads', type=int, default=1, help='The number of threads for video')
    parser.add_argument('--request_img', type=str, default="true", help='Whether to request the image')

    args = parser.parse_args()
    # Load the data
    level_contexts = pd.read_excel(args.input_excel)

    text_generator_strategy = {
        "input_text_key": "input_text",
        "num_threads": args.prompt_num_threads
    }
    callbacks = RunnerCallbacks(ConsoleWorkflowCallbacks())

    # Convert the image to video
    prompt_report: pd.DataFrame = asyncio.run(convert_text_generator(level_contexts=level_contexts,
                                                                     callbacks=callbacks,
                                                                     strategy=text_generator_strategy))
    # 合并level_contexts、prompt_report两个表格，重复字段会自动去重
    merged_report = pd.merge(level_contexts, prompt_report, on="input_text", how="left")
    # Save the video report
    prompt_report_path = os.path.join(args.output_path, "prompt_report.csv")
    merged_report.to_csv(prompt_report_path, index=False)
    image_to_video_strategy = {
        "image_path_key": "image_path",
        "video_prompt_key": "video_prompt",
        "num_threads": args.video_num_threads,
        "request_img": args.request_img == "true",
    }
    # Convert the image to video
    video_report: pd.DataFrame = asyncio.run(convert_image_to_video(level_contexts=merged_report,
                                                                    callbacks=callbacks,
                                                                    strategy=image_to_video_strategy))
    # Save the video report
    video_report_path = os.path.join(args.output_path, "video_report.csv")
    video_report.to_csv(video_report_path, index=False)
