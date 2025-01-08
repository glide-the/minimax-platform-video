

import pandas as pd

from datashaper import NoopVerbCallbacks, derive_from_rows, AsyncType, VerbCallbacks

from minimax_platform_video.video_pull_runner import VideoResult


async def video_pull_task(
        level_contexts: pd.DataFrame,
        callbacks: VerbCallbacks,
        strategy: dict) -> pd.DataFrame:
    from minimax_platform_video.video_pull_runner import run as runner
    reports: list[VideoResult | None] = []

    async def run_generate(record):
        video_task_id_key = strategy['video_task_id_key']
        result = await runner(
            video_task_id=record[video_task_id_key],
            reporter=callbacks,
            strategy_config=strategy,
        )
        return result

    local_reports = await derive_from_rows(
        level_contexts,
        run_generate,
        callbacks=NoopVerbCallbacks(),
        num_threads=1,
        scheduling_type=AsyncType.AsyncIO,
    )
    reports.extend([lr for lr in local_reports if lr is not None])
    return pd.DataFrame(reports)
