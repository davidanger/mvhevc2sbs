# mvhevc2sbs
一个用于将MV-HEVC格式视频转换为SBS（Side-by-Side）格式的Python GUI工具。

## 功能特性
- 支持选择FFmpeg可执行文件路径
- 支持选择输入MV-HEVC视频文件
- 支持设置输出文件路径
- 可调节视频质量参数（CRF）
- 可选择编码预设（preset）
- 实时显示转换进度
- 转换完成提示

## 使用说明

### 依赖要求
- Python 3.x
- FFmpeg
- tkinter（通常随Python安装）

### 运行
```bash
python mvhevc2sbs.py
```

### 界面说明
1. 选择FFmpeg可执行文件路径
2. 选择输入MV-HEVC视频文件
3. 设置输出文件路径
4. 调节CRF值（18-30，默认28）
5. 选择编码预设（默认medium）
6. 点击Convert开始转换

## 参数说明
- CRF：恒定质量因子，值越小质量越高（18-30）
- Preset：编码速度与质量预设，从ultrafast到veryslow

## 注意事项
- 确保FFmpeg已正确安装
- 输入文件必须是MV-HEVC格式
- 输出文件路径需包含.mp4扩展名
