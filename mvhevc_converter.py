import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

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
        
        # Quality settings
        tk.Label(root, text="CRF (18-30):").grid(row=3, column=0, padx=5, pady=5)
        self.crf = tk.Scale(root, from_=18, to=30, orient=tk.HORIZONTAL)
        self.crf.set(28)
        self.crf.grid(row=3, column=1, padx=5, pady=5)
        
        tk.Label(root, text="Preset:").grid(row=4, column=0, padx=5, pady=5)
        self.preset = tk.StringVar(value="medium")
        presets = ["ultrafast", "superfast", "veryfast", "faster", "fast", 
                  "medium", "slow", "slower", "veryslow"]
        tk.OptionMenu(root, self.preset, *presets).grid(row=4, column=1, padx=5, pady=5)
        
        # Convert button
        tk.Button(root, text="Convert", command=self.convert).grid(row=5, column=1, pady=10)
        
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
            
    def convert(self):
        ffmpeg = self.ffmpeg_path.get()
        input_file = self.input_file.get()
        output_file = self.output_file.get()
        crf = self.crf.get()
        preset = self.preset.get()
        
        if not all([ffmpeg, input_file, output_file]):
            messagebox.showerror("Error", "Please fill all fields")
            return
            
        try:
            command = [
                ffmpeg,
                '-i', input_file,
                '-filter_complex', '[0:v:view:0][0:v:view:1]hstack',
                '-c:v', 'hevc',
                '-tag:v', 'hvc1',
                '-crf', str(crf),
                '-preset', preset,
                output_file
            ]
            
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                messagebox.showinfo("Success", "Conversion completed successfully!")
            else:
                messagebox.showerror("Error", f"Conversion failed:\n{stderr.decode()}")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MVHEVCConverter(root)
    root.mainloop()
