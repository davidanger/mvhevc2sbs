import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import os
import threading
import time

class ConversionOutputWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Conversion Progress")
        
        self.text_area = scrolledtext.ScrolledText(self.window, wrap=tk.WORD)
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.stop_button = tk.Button(self.window, text="Stop", command=self.stop_conversion, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.close_button = tk.Button(self.window, text="Close", command=self.window.destroy)
        self.close_button.pack(side=tk.RIGHT, padx=5, pady=5)
        
        self.process = None
        
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.running = True
        
    def append_text(self, text):
        self.text_area.insert(tk.END, text)
        self.text_area.see(tk.END)
        self.text_area.update()
        
    def on_close(self):
        self.running = False
        if self.process:
            self.process.terminate()
        self.window.destroy()
        
    def stop_conversion(self):
        if self.process:
            self.process.terminate()
            self.append_text("\nConversion stopped by user\n")
            self.stop_button.config(state=tk.DISABLED)

class MVHEVCConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("MV-HEVC to SBS Converter")
        
        # FFmpeg path
        tk.Label(root, text="FFmpeg Path:").grid(row=0, column=0, padx=5, pady=5)
        self.ffmpeg_path = tk.Entry(root, width=40)
        self.ffmpeg_path.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(root, text="Browse", command=self.browse_ffmpeg).grid(row=0, column=2, padx=5, pady=5)
        
        # Input file
        tk.Label(root, text="Input MV-HEVC File:").grid(row=1, column=0, padx=5, pady=5)
        self.input_file = tk.Entry(root, width=40)
        self.input_file.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(root, text="Browse", command=self.browse_input).grid(row=1, column=2, padx=5, pady=5)
        
        # Output file
        tk.Label(root, text="Output SBS File:").grid(row=2, column=0, padx=5, pady=5)
        self.output_file = tk.Entry(root, width=40)
        self.output_file.grid(row=2, column=1, padx=5, pady=5)
        tk.Button(root, text="Browse", command=self.browse_output).grid(row=2, column=2, padx=5, pady=5)
        
        # Decoder selection
        tk.Label(root, text="Decoder:").grid(row=3, column=0, padx=5, pady=5)
        self.decoder = tk.StringVar(value="cpu")
        tk.Radiobutton(root, text="CPU", variable=self.decoder, value="cpu", 
                      command=self.update_controls).grid(row=3, column=1, sticky=tk.W)
        tk.Radiobutton(root, text="NVIDIA", variable=self.decoder, value="nvidia",
                      command=self.update_controls).grid(row=3, column=1, sticky=tk.E)
        
        # CPU quality settings
        self.cpu_frame = tk.Frame(root)
        self.cpu_frame.grid(row=4, column=0, columnspan=3, sticky=tk.W)
        
        tk.Label(self.cpu_frame, text="CRF (18-30):").grid(row=0, column=0, padx=5, pady=5)
        self.crf = tk.Scale(self.cpu_frame, from_=18, to=30, orient=tk.HORIZONTAL)
        self.crf.set(28)
        self.crf.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(self.cpu_frame, text="Preset:").grid(row=1, column=0, padx=5, pady=5)
        self.cpu_preset = tk.StringVar(value="medium")
        cpu_presets = ["ultrafast", "superfast", "veryfast", "faster", "fast", 
                      "medium", "slow", "slower", "veryslow"]
        tk.OptionMenu(self.cpu_frame, self.cpu_preset, *cpu_presets).grid(row=1, column=1, padx=5, pady=5)
        
        # NVIDIA quality settings
        self.nvidia_frame = tk.Frame(root)
        self.nvidia_frame.grid(row=4, column=0, columnspan=3, sticky=tk.W)
        
        # Codec selection
        tk.Label(self.nvidia_frame, text="Codec:").grid(row=0, column=0, padx=5, pady=5)
        self.nvidia_codec = tk.StringVar(value="hevc")
        tk.Radiobutton(self.nvidia_frame, text="HEVC", variable=self.nvidia_codec, value="hevc",
                      command=self.update_nvidia_settings).grid(row=0, column=1, sticky=tk.W)
        tk.Radiobutton(self.nvidia_frame, text="AV1", variable=self.nvidia_codec, value="av1",
                      command=self.update_nvidia_settings).grid(row=0, column=1, sticky=tk.E)
        
        # Quality settings
        tk.Label(self.nvidia_frame, text="CQ (0-51):").grid(row=1, column=0, padx=5, pady=5)
        self.cq = tk.Scale(self.nvidia_frame, from_=0, to=51, orient=tk.HORIZONTAL)
        self.cq.set(28)
        self.cq.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(self.nvidia_frame, text="Preset:").grid(row=2, column=0, padx=5, pady=5)
        self.nvidia_preset = tk.StringVar(value="p4")
        nvidia_presets = ["p1", "p2", "p3", "p4", "p5", "p6", "p7"]
        tk.OptionMenu(self.nvidia_frame, self.nvidia_preset, *nvidia_presets).grid(row=2, column=1, padx=5, pady=5)
        
        self.update_controls()
        
        # Convert button
        tk.Button(root, text="Convert", command=self.start_conversion).grid(row=5, column=1, pady=10)
        
    def browse_ffmpeg(self):
        file = filedialog.askopenfilename(title="Select FFmpeg executable")
        if file:
            self.ffmpeg_path.delete(0, tk.END)
            self.ffmpeg_path.insert(0, file)
            
    def browse_input(self):
        file = filedialog.askopenfilename(title="Select MV-HEVC video file")
        if file:
            self.input_file.delete(0, tk.END)
            self.input_file.insert(0, file)
            
    def browse_output(self):
        file = filedialog.asksaveasfilename(title="Save SBS video as",
                                          defaultextension=".mp4",
                                          filetypes=[("MP4 files", "*.mp4")])
        if file:
            self.output_file.delete(0, tk.END)
            self.output_file.insert(0, file)
            
    def update_controls(self):
        if self.decoder.get() == "cpu":
            self.cpu_frame.grid()
            self.nvidia_frame.grid_remove()
        else:
            self.cpu_frame.grid_remove()
            self.nvidia_frame.grid()
            self.update_nvidia_settings()
            
    def update_nvidia_settings(self):
        """Update NVIDIA settings based on selected codec"""
        if self.nvidia_codec.get() == "av1":
            self.cq.set(35)
            self.nvidia_preset.set("p5")
        else:
            self.cq.set(28)
            self.nvidia_preset.set("p4")
            
    def start_conversion(self):
        """开始转换"""
        if not self.validate_inputs():
            return
            
        self.output_window = ConversionOutputWindow(self.root)
        self.conversion_thread = threading.Thread(target=self.run_conversion)
        self.conversion_thread.start()
        
    def run_conversion(self):
        ffmpeg = self.ffmpeg_path.get()
        input_file = self.input_file.get()
        output_file = self.output_file.get()
        
        try:
            if self.decoder.get() == "cpu":
                command = [
                    ffmpeg,
                    '-i', input_file,
                    '-filter_complex', '[0:v:view:0][0:v:view:1]hstack',
                    '-c:v', 'hevc',
                    '-tag:v', 'hvc1',
                    '-crf', str(self.crf.get()),
                    '-preset', self.cpu_preset.get(),
                    output_file
                ]
            else:
                if self.nvidia_codec.get() == "hevc":
                    command = [
                        ffmpeg,
                        '-i', input_file,
                        '-filter_complex', '[0:v:view:0][0:v:view:1]hstack',
                        '-c:v', 'hevc_nvenc',
                        '-preset', self.nvidia_preset.get(),
                        '-cq', str(self.cq.get()),
                        '-tag:v', 'hvc1',
                        output_file
                    ]
                else:  # AV1
                    command = [
                        ffmpeg,
                        '-i', input_file,
                        '-filter_complex', '[0:v:view:0][0:v:view:1]hstack',
                        '-c:v', 'av1_nvenc',
                        '-preset', self.nvidia_preset.get(),
                        '-cq', str(self.cq.get()),
                        '-tag:v', 'av01',
                        '-movflags', '+faststart',
                        '-strict', 'experimental',
                        output_file
                    ]
            
            self.output_window.process = process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                encoding='utf-8',
                errors='replace'
            )
            
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    # 添加时间戳和进度指示
                    self.output_window.append_text(f"[{time.strftime('%H:%M:%S')}] {output}")
                    # 强制刷新GUI
                    self.output_window.text_area.update_idletasks()
                    
            return_code = process.poll()
            
            if return_code == 0:
                self.output_window.append_text("\nConversion completed successfully!\n")
                self.output_window.stop_button.config(state=tk.DISABLED)
            else:
                self.output_window.append_text(f"\nConversion failed with return code {return_code}\n")
                self.output_window.stop_button.config(state=tk.DISABLED)
                
        except Exception as e:
            self.output_window.append_text(f"\nError occurred: {str(e)}\n")
            self.output_window.stop_button.config(state=tk.DISABLED)
            
    def validate_inputs(self):
        """验证输入"""
        if not all([self.ffmpeg_path.get(), self.input_file.get(), self.output_file.get()]):
            messagebox.showerror("错误", "请填写所有字段")
            return False
        return True

if __name__ == "__main__":
    root = tk.Tk()
    app = MVHEVCConverter(root)
    root.mainloop()
