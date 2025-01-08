#### 开放平台视频生成批量操作

#### 项目简介 

本项目是基于开放平台的视频生成批量操作，主要包括视频生成功能，通过本demo你可以快速生成多个一致性高度相同的视频备选素材。

提交包含 input_text, image_path 字段的 level_contexts.xlsx 文件

**input_text**：文本内容

**image_path**: 图片绝对路径

输出结果为视频任务 id 的 csv文件，
#### 快速尝试

#### 使用
 
- 1、安装依赖 python 需要3.10以上版本
```shell
pip install minimax-platform-video -U
```

- 2、设置环境变量

首先，我们需要安装最新版本的智谱AI SDK，只有 > 2.1.4 的SDK版本支持视频生成模型。 同时，我们设定好 API Key。
```shell
export API_KEY="开放平台key" 
```

- 3、准备数据

基础表格里需要准备的数据包含了 **input_text**, **image_path** 字段

**input_text** 为生成提示词，用于控制镜头

**image_path** 为起始帧的图片，这个图片可以不存在，使用 request_img 命令参数控制是否必须采用起始帧，默认必须存在


- 4、运行

> 启动目录为项目根目录

```shell
python -m minimax_platform_video.start --input_excel C:\\Users\\Administrator\\Desktop\\data\\level_contexts.xlsx --output_path C:\\Users\\Administrator\\Desktop\\data\\
```

> 参数说明
> 
> **input_excel**：为包含input_text,image_path字段的的level_contexts.xlsx文件
> 
> **output_path**：为输出文件路径，生成 video_report.csv文件
> 
> 可以断点续传，会自动跳过已经生成的任务, 
> 
> 根据需要配置线程
> 
> **prompt_num_threads**: 提示词线程数,默认2
> 
> **video_num_threads**: 视频生成线程数,默认1
> 

- 5、获取任务结果 

> 启动目录为项目根目录
```shell
python -m minimax_platform_video.video_pull --task_video_csv C:\\Users\\Administrator\\Desktop\\data\\video_report.csv --output_path C:\\Users\\Administrator\\Desktop\\data\\
```
> 参数说明
> 
> **input_excel**： video_report.csv文件
> 
> **output_path**：为输出文件路径 生成video_pull_report.csv文件
> 
> 会自动跳过已经获取的任务, 删除根目录**cache_data/VideoPullGenerator**的文件可以重新获取
> 
> 根据需要配置线程
> 
> **num_threads**: 线程数,默认2
> 


- 6、下载视频 

> 启动目录为项目根目录
```shell
python -m minimax_platform_video.download_video  --csv_file_path  C:\\Users\\renrui\\Desktop\\data\\video_pull_report.csv --output_path C:\\Users\\renrui\\Desktop\\data\\

```
> 参数说明
> 
> **csv_file_path**： video_pull_report.csv文件
> 
> **output_path**：为输出文件路径 视频下载目录
>   
> 
