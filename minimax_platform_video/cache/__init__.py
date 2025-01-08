from minimax_platform_video.cache.json_pipeline_cache import JsonPipelineCache
from minimax_platform_video.storage.file_pipeline_storage import FilePipelineStorage


def load_cache(root_dir: str | None,base_dir: str | None):

    storage = FilePipelineStorage(root_dir).child(base_dir)
    return JsonPipelineCache(storage)