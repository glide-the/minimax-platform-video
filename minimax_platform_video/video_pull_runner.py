import os
import traceback
from typing import Any, TypedDict, List
import logging
from datashaper import VerbCallbacks

from minimax_platform_video.cache import load_cache
from minimax_platform_video.rate_limiter import RateLimiter
from minimax_platform_video.utils import create_hash_key

log = logging.getLogger(__name__)


class VideoData(TypedDict):
    file_id: str
    video_width: str
    video_height: str
    base_resp: dict


class VideoResult(TypedDict):
    video_task_id: str

    result: VideoData
    task_status: str


def _get_video_result(video_task_id: str) -> dict:
    import requests
    import json

    api_key = os.environ.get("API_KEY")

    url = f"http://api.minimax.chat/v1/query/video_generation?task_id={video_task_id}"

    payload = {}
    headers = {
        'authorization': f'Bearer {api_key}',
        'content-type': 'application/json',
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()


class VideoPullGenerator:
    def __init__(
            self,
    ):
        pass

    async def __call__(self, inputs: dict[str, Any]) -> VideoResult:
        """Call method definition."""
        output = None
        try:
            output = _get_video_result(inputs["video_task_id"])

        except Exception as e:
            log.exception("error VideoPullGenerator")
            output = {}

        return VideoResult(
            video_task_id=output["task_id"],
            result=VideoData(file_id=output["file_id"],
                             video_width=output["video_width"],
                             video_height=output["video_height"],
                             base_resp=output["base_resp"]),
            task_status=output["status"],
        )


async def run(
        video_task_id: str,
        reporter: VerbCallbacks,
        strategy_config: dict[str, Any],
) -> VideoResult | None:
    return await _run_extractor(video_task_id, reporter, strategy_config)


async def _run_extractor(
        video_task_id: str,
        reporter: VerbCallbacks,
        strategy_config: dict[str, Any],
) -> VideoResult | None:
    # RateLimiter
    rate_limiter = RateLimiter(rate=1, per=60)
    generator = VideoPullGenerator()

    try:
        await rate_limiter.acquire()

        cache_key = create_hash_key("VideoPullGenerator",
                                    {
                                        "video_task_id": video_task_id,
                                    })
        _cache = load_cache(root_dir="cache_data", base_dir="VideoPullGenerator")

        cached_result = await _cache.get(cache_key)

        if cached_result:
            return cached_result
        reporter.log(f"VideoPullGenerator:{cache_key}", {"video_task_id": video_task_id})
        generator_output = await generator({"video_task_id": video_task_id})
        if generator_output:
            await _cache.set(
                cache_key,
                generator_output,
                {
                    "video_task_id": video_task_id,
                },
            )
        return generator_output
    except Exception as e:
        log.exception("Error processing video_task_id: %s", video_task_id)
        reporter.error("input_text Error", e, traceback.format_exc())
        return None
