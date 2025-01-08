import os

from minimax_platform_video.prompt_runner import PromptReport
from minimax_platform_video.video_runner import VideoReport
from datashaper import (
    AsyncType,
    VerbCallbacks,
    derive_from_rows,
)

import pandas as pd


async def convert_image_to_video(level_contexts: pd.DataFrame,
                                 callbacks: VerbCallbacks,
                                 strategy: dict) -> pd.DataFrame:
    from minimax_platform_video.video_runner import run as runner
    reports: list[VideoReport | None] = []

    async def run_generate(record):
        video_prompt_key = strategy['video_prompt_key']
        image_path_key = strategy['image_path_key']
        result = await runner(
            video_prompt=record[video_prompt_key],
            image_path=record[image_path_key] if strategy.get("request_img", True) else None,
            reporter=callbacks,
            strategy_config=strategy,
        )
        return result

    local_reports = await derive_from_rows(
        level_contexts,
        run_generate,
        callbacks=callbacks,
        num_threads=1,
        scheduling_type=AsyncType.AsyncIO,
    )
    reports.extend([lr for lr in local_reports if lr is not None])
    return pd.DataFrame(reports)


async def convert_text_generator(
        level_contexts: pd.DataFrame,
        callbacks: VerbCallbacks,
        strategy: dict) -> pd.DataFrame:
    from minimax_platform_video.prompt_runner import run as runner
    reports: list[PromptReport | None] = []

    async def run_generate(record):
        input_text_key = strategy['input_text_key']
        result = await runner(
            input_text=record[input_text_key],
            reporter=callbacks,
            strategy_config=strategy,
        )
        return result

    local_reports = await derive_from_rows(
        level_contexts,
        run_generate,
        callbacks=callbacks,
        num_threads=strategy.get("num_threads", 1),
        scheduling_type=AsyncType.AsyncIO,
    )
    reports.extend([lr for lr in local_reports if lr is not None])
    return pd.DataFrame(reports)
