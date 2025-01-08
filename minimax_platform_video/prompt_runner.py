import logging
import traceback
from typing import Any, TypedDict

# from langchain_core.prompts import ChatPromptTemplate
# from langchain_glm import Chatminimax

from datashaper import VerbCallbacks

from minimax_platform_video.cache import load_cache
from minimax_platform_video.rate_limiter import RateLimiter
from minimax_platform_video.utils import create_hash_key

log = logging.getLogger(__name__)


class PromptReport(TypedDict):
    input_text: str
    video_prompt: str


# class VideoStrategyPrompt:
#     def __init__(
#             self,
#     ):
#         pass
#
#     async def __call__(self, inputs: dict[str, Any]) -> str:
#         """Call method definition."""
#         output = None
#         try:
#             chat_template = ChatPromptTemplate.from_messages(
#                 [
#                     ("system", "帮我用中文详细描述下面这个场景动作"),
#                     ("human", "{input_text}"),
#                 ]
#             )
#             chat = Chatminimax(model="glm-4-air")
#             messages = chat_template.format_messages(input_text=inputs["input_text"])
#
#             output = await chat.ainvoke(messages)
#
#         except Exception as e:
#             log.exception("error VideoStrategyPrompt")
#             output = {}
#
#         return output.content


async def run(
        input_text: str,
        reporter: VerbCallbacks,
        strategy_config: dict[str, Any],
) -> PromptReport | None:
    return await _run_extractor(input_text, reporter, strategy_config)


async def _run_extractor(
        input_text: str,
        reporter: VerbCallbacks,
        strategy_config: dict[str, Any],
) -> PromptReport | None:
    # RateLimiter
    rate_limiter = RateLimiter(rate=1, per=60)
    # generator = VideoStrategyPrompt()

    try:
        await rate_limiter.acquire()
        cache_key = create_hash_key("VideoStrategyPrompt", {"input_text": input_text})
        _cache = load_cache(root_dir="cache_data", base_dir="VideoStrategyPrompt")
        cached_result = await _cache.get(cache_key)

        if cached_result:

            return PromptReport(input_text=input_text,
                                video_prompt=cached_result,
                                )
        reporter.log(f"Running VideoStrategyPrompt:{cache_key}")
        # video_prompt = await generator({"input_text": input_text})
        video_prompt = input_text
        if video_prompt:
            await _cache.set(
                cache_key,
                video_prompt,
                {
                    "input_text": input_text
                },
            )
        return PromptReport(input_text=input_text,
                            video_prompt=video_prompt,
                            )
    except Exception as e:
        log.exception("Error processing input_text: %s", input_text)
        reporter.error("input_text Error", e, traceback.format_exc())
        return None
