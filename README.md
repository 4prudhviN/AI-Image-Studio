# 🎨 AI Image Studio

A modern AI image generation web app built with Python and Streamlit, powered by the [Pollinations AI](https://pollinations.ai/) API — **no API key required**.

Built for the **MirAI School of Technology — Virtual Summer Internship 2026 · AI Builder Track**.

---

## Features

- 🖼️ Generate images from text prompts instantly
- 🎭 10 art styles: Realistic, Anime, Oil Painting, Watercolor, Cyberpunk, Fantasy, Pixel Art, Sketch, 3D Render, Minimalist
- ✨ Magic Enhance — automatically boosts prompt quality with professional keywords
- 🎲 Surprise Me — randomly picks a creative prompt and generates an image
- ⬇️ Download generated images as PNG
- ⚙️ Control image width and height (256–1024 px) via sidebar sliders

---

## Project Structure

```
AI_Image_Studio/
│
├── app.py            # Main Streamlit application
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

---

## Setup & Installation

### 1. Clone or download the project

```bash
cd AI_Image_Studio
```

### 2. Create and activate a virtual environment (recommended)

**Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## How to Use

1. **Enter a prompt** — describe the image you want in the text box.
2. **Choose an art style** — pick from the dropdown.
3. **Adjust settings** in the sidebar:
   - Set the image width and height.
   - Enable **Magic Enhance** for higher-quality results.
4. Click **🎨 Generate Image** to create your artwork.
5. Or click **🎲 Surprise Me!** to generate a random creative image.
6. Click **⬇️ Download Image** to save the result as a PNG file.

---

## Dependencies

| Package     | Purpose                        |
|-------------|--------------------------------|
| streamlit   | Web UI framework               |
| requests    | HTTP calls to Pollinations API |
| Pillow      | Image processing               |

---

## API

This app uses the free [Pollinations AI Image API](https://image.pollinations.ai/):

```
https://image.pollinations.ai/prompt/{encoded_prompt}?width={w}&height={h}
```

No account or API key is needed.

---

## License

MIT — free to use, modify, and share.
