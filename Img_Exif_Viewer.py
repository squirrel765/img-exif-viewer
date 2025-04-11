import json
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk

class MetadataViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("SD/ComfyUI Prompt Viewer")
        self.root.geometry("1000x700")
        self.root.minsize(800, 500)

        # 내부 상태
        self.last_info = None
        self.last_file_path = None
        self.tk_image = None

        # 전체 레이아웃 설정
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=2)

        # ─── 모드 선택 (상단)
        self.mode = tk.StringVar(value="Stable Diffusion")
        mode_frame = tk.Frame(root)
        mode_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

        tk.Label(mode_frame, text="모드 선택:").pack(side=tk.LEFT)
        tk.Radiobutton(mode_frame, text="Stable Diffusion", variable=self.mode, value="Stable Diffusion", command=self.on_mode_change).pack(side=tk.LEFT)
        tk.Radiobutton(mode_frame, text="ComfyUI", variable=self.mode, value="ComfyUI", command=self.on_mode_change).pack(side=tk.LEFT)

        # ─── 좌측: 이미지 미리보기
        self.image_frame = tk.Frame(root, bg="lightgray", bd=1, relief=tk.SUNKEN)
        self.image_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.image_frame.grid_rowconfigure(0, weight=1)
        self.image_frame.grid_columnconfigure(0, weight=1)

        self.image_label = tk.Label(self.image_frame, text="여기로 PNG 이미지를 드래그하거나 클릭하세요", bg="lightgray", anchor="center")
        self.image_label.grid(row=0, column=0, sticky="nsew")
        self.image_label.bind("<Button-1>", self.open_image_dialog)
        self.image_label.drop_target_register(DND_FILES)
        self.image_label.dnd_bind("<<Drop>>", self.on_drop)

        # ─── 우측: 메타데이터 출력
        self.output = scrolledtext.ScrolledText(root, wrap=tk.WORD)
        self.output.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

    # 이미지 클릭 → 파일 다이얼로그 열기
    def open_image_dialog(self, event=None):
        file_path = filedialog.askopenfilename(filetypes=[("PNG 이미지", "*.png")])
        if file_path:
            self.process_image(file_path)

    # 이미지 드롭
    def on_drop(self, event):
        file_path = event.data.strip("{}")
        if file_path.lower().endswith(".png"):
            self.process_image(file_path)
        else:
            messagebox.showwarning("지원되지 않음", "PNG 파일만 지원됩니다.")

    # 모드 전환 시 현재 이미지 재로딩
    def on_mode_change(self):
        if self.last_file_path:
            self.process_image(self.last_file_path)

    # 이미지 로딩 및 메타데이터 파싱
    def process_image(self, file_path):
        try:
            self.last_file_path = file_path

            # 이미지 표시
            self.show_image(file_path)

            # 메타데이터 추출
            img = Image.open(file_path)
            info = img.info
            self.last_info = info

            self.output.delete("1.0", tk.END)
            if self.mode.get() == "Stable Diffusion":
                self.display_sd_metadata(info)
            elif self.mode.get() == "ComfyUI":
                self.display_comfy_metadata(info)

        except Exception as e:
            messagebox.showerror("오류", f"이미지 처리 중 오류 발생:\n{e}")

    # 이미지 미리보기 표시
    def show_image(self, file_path):
        image = Image.open(file_path)
        image.thumbnail((400, 400))
        self.tk_image = ImageTk.PhotoImage(image)
        self.image_label.configure(image=self.tk_image, text="")
        self.image_label.image = self.tk_image

    # SD용 메타데이터 출력
    def display_sd_metadata(self, info):
        if "parameters" in info:
            self.output.insert(tk.END, "[parameters]\n" + info["parameters"])
        else:
            found = False
            for key in ["prompt", "Prompt", "negative_prompt", "sampler", "seed"]:
                if key in info:
                    self.output.insert(tk.END, f"[{key}]\n{info[key]}\n\n")
                    found = True
            if not found:
                self.output.insert(tk.END, "Stable Diffusion 메타데이터를 찾을 수 없습니다.")

    # ComfyUI용 메타데이터 출력
    def display_comfy_metadata(self, info):
        found = False
        for key in info:
            if key.lower() in ["workflow", "prompt", "extra info"]:
                self.output.insert(tk.END, f"[{key}]\n")
                try:
                    parsed = json.loads(info[key])
                    pretty = json.dumps(parsed, indent=4, ensure_ascii=False)
                    self.output.insert(tk.END, pretty + "\n\n")
                except json.JSONDecodeError:
                    self.output.insert(tk.END, info[key] + "\n\n")
                found = True
        if not found:
            self.output.insert(tk.END, "ComfyUI 관련 메타데이터를 찾을 수 없습니다.")

# 프로그램 실행
if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = MetadataViewer(root)
    root.mainloop()
