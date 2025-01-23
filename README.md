# MV-HEVC to SBS Converter / MV-HEVC转SBS格式转换器

This tool converts MV-HEVC videos to Side-by-Side (SBS) format using FFmpeg.
本工具使用FFmpeg将MV-HEVC视频转换为并排（SBS）格式。

## Features / 功能特性

- Supports both CPU and NVIDIA hardware acceleration
  支持CPU和NVIDIA硬件加速
- For NVIDIA GPUs, supports both HEVC and AV1 encoding:
  对于NVIDIA GPU，支持HEVC和AV1编码：
  - HEVC mode (default):
    HEVC模式（默认）：
    - CQ range: 0-51 (default: 28)
      CQ范围：0-51（默认：28）
    - Presets: p1-p7 (default: p4)
      预设：p1-p7（默认：p4）
  - AV1 mode:
    AV1模式：
    - CQ range: 0-51 (default: 35)
      CQ范围：0-51（默认：35）
    - Presets: p1-p7 (default: p5)
      预设：p1-p7（默认：p5）
    - Additional options: faststart, experimental mode
      额外选项：快速启动，实验模式
- Real-time conversion progress display
  实时转换进度显示
- Stop button for interrupting conversion
  停止按钮可中断转换
- Automatic quality settings adjustment based on selected codec
  根据所选编码器自动调整质量设置

## Requirements / 系统要求

- Python 3.6+
  Python 3.6及以上版本
- FFmpeg with NVIDIA codec support (for hardware acceleration)
  支持NVIDIA编解码器的FFmpeg（用于硬件加速）
- NVIDIA GPU with AV1 encoding support (for AV1 mode)
  支持AV1编码的NVIDIA GPU（用于AV1模式）

## Usage / 使用方法

1. Select FFmpeg executable path
   选择FFmpeg可执行文件路径
2. Choose input MV-HEVC video file
   选择输入的MV-HEVC视频文件
3. Set output file path and name
   设置输出文件路径和名称
4. Select decoder (CPU or NVIDIA)
   选择解码器（CPU或NVIDIA）
5. For NVIDIA decoder:
   对于NVIDIA解码器：
   - Choose codec (HEVC or AV1)
     选择编码器（HEVC或AV1）
   - Adjust quality settings
     调整质量设置
6. Click "Convert" to start conversion
   点击"转换"开始转换
