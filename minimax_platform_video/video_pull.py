import argparse
import asyncio
from minimax_platform_video.reporting.console_workflow_callbacks import ConsoleWorkflowCallbacks
from minimax_platform_video.reporting.runner_callbacks import RunnerCallbacks

import pandas as pd

import os
import sys
import logging.config

from minimax_platform_video.result_task import video_pull_task

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert the image to video')
    parser.add_argument('--task_video_csv', type=str, help='The input excel file')
    parser.add_argument('--output_path', type=str, help='The output path')
    parser.add_argument('--num_threads', type=int, default=2, help='The number of threads ')
    args = parser.parse_args()
    # Load the data
    level_contexts = pd.read_csv(args.task_video_csv)

    video_strategy = {
        "video_task_id_key": "video_task_id",
        "num_threads": 10
    }
    callbacks = RunnerCallbacks(ConsoleWorkflowCallbacks())

    video_pull_report: pd.DataFrame = asyncio.run(video_pull_task(level_contexts=level_contexts,
                                                                  strategy=video_strategy,
                                                                  callbacks=callbacks))

    # Save the video report
    video_pull_report_path = os.path.join(args.output_path, "video_pull_report.csv")
    video_pull_report.to_csv(video_pull_report_path, index=False)
