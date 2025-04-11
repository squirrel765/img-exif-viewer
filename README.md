# 🖼️ Img Exif Viewer

**Img Exif Viewer**는 Stable Diffusion 및 ComfyUI로 생성된 PNG 이미지의 프롬프트 메타데이터(EXIF 및 tEXt)를 확인할 수 있는 Windows용 GUI 도구입니다.

- ✅ Stable Diffusion / ComfyUI 모드 전환 지원
- ✅ PNG 이미지 드래그 앤 드롭 또는 클릭으로 불러오기
- ✅ 좌측 이미지 미리보기 + 우측 프롬프트 표시
- ✅ 창 크기에 따라 자동 리사이징
- ✅ `.exe` 실행 파일 제공 (설치 불필요)

---

## 📸 기능 미리보기

<img width="740" alt="Image" src="https://github.com/user-attachments/assets/e3125338-c438-4fa7-b4cb-5fa030e1375a" />

---

## 🚀 다운로드

👉 [최신 릴리즈에서 `.exe` 다운로드]

> 설치 없이 바로 실행 가능한 단일 실행파일입니다.


## 🔧 사용 방법

1. 프로그램을 실행합니다.
2. PNG 파일을 드래그하거나 클릭하여 선택합니다.
3. 좌측에 이미지가, 우측에 프롬프트 메타데이터가 표시됩니다.
4. 상단에서 모드를 전환하면, 해당 형식에 맞춰 자동으로 다시 표시됩니다.

---

## 🛠️ 개발 환경

- Python 3.10+
- [`Pillow`](https://pillow.readthedocs.io/)
- [`tkinterdnd2`](https://pypi.org/project/tkinterdnd2/)
- [`PyInstaller`](https://pyinstaller.org/) (for `.exe` build)

## 🔧 개발자용 설치 (선택사항)
> `.exe` 파일만 사용하는 경우 이 단계를 건너뛰어도 됩니다.

```bash
pip install pillow tkinterdnd2
python Img_Exif_Viewer.py