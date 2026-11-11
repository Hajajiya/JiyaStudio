
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import streamlit as st
import yt_dlp

# =========================================================
# PAGE CONFIG
# =========================================================



st.set_page_config(
    page_title="Jiya Studio — Video Downloader",
    page_icon="🖤",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# LOCAL IMAGE
# =========================================================



def get_background():
    return """
        background:
            radial-gradient(
                ellipse at 15% 10%,
                rgba(124, 58, 237, 0.22),
                transparent 40%
            ),
            radial-gradient(
                ellipse at 85% 20%,
                rgba(59, 130, 246, 0.18),
                transparent 40%
            ),
            radial-gradient(
                ellipse at 50% 100%,
                rgba(14, 165, 233, 0.10),
                transparent 45%
            ),
            #080b14;

        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    """


background_css = get_background()

# =========================================================
# LIQUID GLASS DESIGN
# =========================================================

st.markdown(f"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {{
    font-family: 'Inter', sans-serif;
}}

.stApp {{
    {background_css}
    color: #f5f7ff;
}}

.block-container {{
    max-width: 1100px;
    padding-top: 2.5rem;
    padding-bottom: 4rem;
}}

header[data-testid="stHeader"] {{
    background: transparent;
}}

.brand {{
    display: flex;
    align-items: center;
    gap: 13px;
    margin-bottom: 30px;
}}

.brand-icon {{
    width: 49px;
    height: 49px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 16px;
    font-size: 25px;
    background: linear-gradient(135deg,#8b9cff,#6257e8);
    box-shadow: 0 8px 30px rgba(105,100,255,.4);
}}

.brand-name {{
    font-size: 24px;
    font-weight: 800;
    letter-spacing: -1px;
    color: white;
}}

.brand-name span {{
    color: #99a6ff;
}}

.hero-title {{
    font-size: clamp(36px,5vw,58px);
    font-weight: 800;
    letter-spacing: -2.5px;
    line-height: 1.12;
    margin-top: 15px;
    background: linear-gradient(100deg,#fff,#aebaff 55%,#71e9df);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.hero-subtitle {{
    color: #b0b8ca;
    font-size: 15px;
    line-height: 1.8;
    margin-top: 15px;
    margin-bottom: 35px;
}}

.glass-card {{
    background: linear-gradient(
        135deg,
        rgba(255,255,255,.12),
        rgba(255,255,255,.035)
    );
    border: 1px solid rgba(255,255,255,.17);
    border-radius: 24px;
    padding: 25px;
    backdrop-filter: blur(28px);
    -webkit-backdrop-filter: blur(28px);
    box-shadow:
        0 20px 60px rgba(0,0,0,.25),
        inset 0 1px 0 rgba(255,255,255,.15);
    margin-bottom: 22px;
}}

.section-title {{
    font-size: 18px;
    font-weight: 700;
    color: white;
}}

.stTextInput input {{
    background: rgba(255,255,255,.07) !important;
    border: 1px solid rgba(255,255,255,.18) !important;
    border-radius: 14px !important;
    color: white !important;
    height: 52px !important;
    padding-left: 16px !important;
}}

.stTextInput input:focus {{
    border-color: #8999ff !important;
    box-shadow: 0 0 0 3px rgba(137,153,255,.15) !important;
}}

.stTextInput label,
.stRadio label,
.stSelectbox label,
.stFileUploader label {{
    color: #e0e5f4 !important;
    font-weight: 600 !important;
}}

.stSelectbox div[data-baseweb="select"] > div {{
    background: rgba(255,255,255,.07) !important;
    border: 1px solid rgba(255,255,255,.17) !important;
    border-radius: 13px !important;
    color: white !important;
    min-height: 48px;
}}

.stRadio [role="radiogroup"] {{
    gap: 12px;
}}

.stRadio [role="radio"] {{
    background: rgba(255,255,255,.05);
    border: 1px solid rgba(255,255,255,.14);
    padding: 10px 14px;
    border-radius: 12px;
}}

.stButton > button {{
    width: 100%;
    min-height: 55px;
    border: 1px solid rgba(255,255,255,.3);
    border-radius: 15px;
    color: white;
    font-size: 15px;
    font-weight: 700;
    background: linear-gradient(110deg,#6579ff,#8870ff 55%,#55c9d9);
    box-shadow: 0 8px 30px rgba(104,113,255,.3);
    transition: all .25s ease;
}}

.stButton > button:hover {{
    transform: translateY(-2px);
    border-color: white;
    box-shadow: 0 12px 35px rgba(104,113,255,.45);
    color: white;
}}

.stDownloadButton > button {{
    width: 100%;
    min-height: 55px;
    border-radius: 15px;
    background: linear-gradient(110deg,#19bd99,#39d5be);
    color: #061a19;
    border: none;
    font-weight: 800;
    font-size: 15px;
}}

.stDownloadButton > button:hover {{
    transform: translateY(-2px);
    color: #061a19;
}}

div[data-testid="stExpander"] {{
    background: rgba(255,255,255,.045);
    border: 1px solid rgba(255,255,255,.14);
    border-radius: 16px;
    overflow: hidden;
}}

div[data-testid="stExpander"] summary {{
    color: white;
}}

[data-testid="stFileUploaderDropzone"] {{
    background: rgba(255,255,255,.04) !important;
    border: 1px dashed rgba(255,255,255,.25) !important;
    border-radius: 15px !important;
}}

.stProgress > div > div > div {{
    background: linear-gradient(90deg,#6579ff,#4bd9ce);
    border-radius: 20px;
}}

.stProgress > div > div {{
    background: rgba(255,255,255,.1);
    border-radius: 20px;
}}

div[data-testid="stAlert"] {{
    background: rgba(255,255,255,.07);
    border: 1px solid rgba(255,255,255,.16);
    border-radius: 15px;
}}

[data-testid="stImage"] img {{
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,.18);
}}

.stCaption {{
    color: #a0abc2 !important;
}}

hr {{
    border-color: rgba(255,255,255,.14) !important;
}}

.footer {{
    text-align: center;
    color: #a0abc2;
    font-size: 12px;
    padding: 25px 0;
    line-height: 1.9;
}}

@media(max-width:768px) {{
    .block-container {{
        padding: 1.2rem 1rem 3rem;
    }}

    .hero-title {{
        letter-spacing: -1px;
    }}

    .glass-card {{
        padding: 18px;
    }}
}}

</style>
""", unsafe_allow_html=True)


# =========================================================
# BRAND / HERO
# =========================================================

st.markdown("""
<div class="brand">
    <div class="brand-icon">◈</div>
    <div class="brand-name">Jiya <span>Studio</span></div>
</div>

<div class="hero-title">
    Download anything.<br>
    Keep everything.
</div>

<div class="hero-subtitle">
    Your all-in-one media downloader.<br>
    Download videos and audio from your favourite platforms
    with quality control and a simple workflow.
</div>
""", unsafe_allow_html=True)


# =========================================================
# QUALITY MAP
# =========================================================

QUALITY_MAP = {
    "Best": None,
    "1080p": 1080,
    "720p": 720,
    "480p": 480,
    "360p": 360
}


# =========================================================
# ORIGINAL DOWNLOADER HELPERS
# =========================================================

def is_h264(vcodec):
    return bool(vcodec) and vcodec.lower().startswith(("avc", "h264"))


def is_aac(acodec):
    return bool(acodec) and acodec.lower().startswith(("mp4a", "aac"))


def get_codecs(info):
    vcodec = info.get("vcodec")
    acodec = info.get("acodec")

    for f in info.get("requested_formats") or []:
        if f.get("vcodec") and f["vcodec"] != "none":
            vcodec = f["vcodec"]

        if f.get("acodec") and f["acodec"] != "none":
            acodec = f["acodec"]

    return vcodec, acodec


def make_compatible(path, vcodec, acodec):

    if not shutil.which("ffmpeg"):
        return path

    v_ok, a_ok = is_h264(vcodec), is_aac(acodec)

    base, _ = os.path.splitext(path)
    out = base + ".compat.mp4"

    cmd = ["ffmpeg", "-y", "-i", path]

    if v_ok:
        cmd += ["-c:v", "copy"]
    else:
        cmd += [
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "20",
            "-pix_fmt", "yuv420p"
        ]

    if a_ok:
        cmd += ["-c:a", "copy"]
    else:
        cmd += ["-c:a", "aac", "-b:a", "192k"]

    cmd += ["-movflags", "+faststart", out]

    result = subprocess.run(cmd, capture_output=True)

    if result.returncode == 0 and os.path.exists(out):
        os.remove(path)
        final = base + ".mp4"
        os.replace(out, final)
        return final

    if os.path.exists(out):
        os.remove(out)

    return path


def build_opts(outdir, mode, quality, cookies_path, hook):

    height = QUALITY_MAP[quality]

    if mode == "Audio only (MP3)":
        fmt = "bestaudio/best"

    elif height:
        fmt = (
            f"bestvideo[height<={height}][vcodec^=avc1]+bestaudio[acodec^=mp4a]/"
            f"bestvideo[height<={height}]+bestaudio/"
            f"best[height<={height}]/best"
        )

    else:
        fmt = "bestvideo[vcodec^=avc1]+bestaudio[acodec^=mp4a]/bestvideo+bestaudio/best"

    opts = {
        "format": fmt,
        "outtmpl": os.path.join(outdir, "%(title).80s [%(id)s].%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "progress_hooks": [hook],
        "restrictfilenames": False,
    }

    if mode == "Audio only (MP3)":
        opts["postprocessors"] = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ]

    else:
        opts["format_sort"] = ["vcodec:h264", "acodec:aac", "res", "ext:mp4:m4a"]
        opts["merge_output_format"] = "mp4"

    if cookies_path:
        opts["cookiefile"] = cookies_path

    return opts


def fetch_info(url, cookies_path):

    opts = {
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True
    }

    if cookies_path:
        opts["cookiefile"] = cookies_path

    with yt_dlp.YoutubeDL(opts) as ydl:
        return ydl.extract_info(url, download=False)


# =========================================================
# DOWNLOADER UI
# =========================================================

st.markdown("""
<div class="glass-card">
    <div class="section-title">✦ Start your download</div>
</div>
""", unsafe_allow_html=True)

url = st.text_input(
    "Video URL",
    placeholder="Paste your video link here..."
)

col1, col2 = st.columns(2)

with col1:
    mode = st.radio(
        "Download format",
        ["Video (MP4)", "Audio only (MP3)"],
        horizontal=True
    )

with col2:
    quality = st.selectbox(
        "Video quality",
        list(QUALITY_MAP.keys()),
        disabled=(mode != "Video (MP4)")
    )

with st.expander("⚙️ Advanced settings — Cookies"):

    cookies_file = st.file_uploader(
        "Upload cookies.txt (Netscape format)",
        type=["txt"]
    )


# =========================================================
# SESSION STATE
# =========================================================

if "result" not in st.session_state:
    st.session_state.result = None


# =========================================================
# DOWNLOAD ACTION
# =========================================================

if st.button(
    "⬇️  Download Media",
    type="primary",
    disabled=not url.strip()
):

    st.session_state.result = None

    tmpdir = tempfile.mkdtemp()
    cookies_path = None

    if cookies_file:
        cookies_path = os.path.join(tmpdir, "cookies.txt")

        with open(cookies_path, "wb") as f:
            f.write(cookies_file.getbuffer())

    try:

        with st.spinner("Fetching video info..."):
            info = fetch_info(url.strip(), cookies_path)

        if info.get("thumbnail"):
            st.image(info["thumbnail"], width=300)

        st.write(f"**{info.get('title', 'Untitled')}**")

        if info.get("uploader"):
            st.write(f"By: {info['uploader']}")

        bar = st.progress(0.0, text="Starting...")

        def hook(d):

            if d["status"] == "downloading":

                total = d.get("total_bytes") or d.get("total_bytes_estimate")

                if total:
                    pct = min(d["downloaded_bytes"] / total, 1.0)
                    bar.progress(pct, text=f"Downloading... {pct:.0%}")

            elif d["status"] == "finished":
                bar.progress(1.0, text="Processing...")

        outdir = os.path.join(tmpdir, "out")
        os.makedirs(outdir)

        with yt_dlp.YoutubeDL(
            build_opts(outdir, mode, quality, cookies_path, hook)
        ) as ydl:
            dl_info = ydl.extract_info(url.strip(), download=True)

        files = [
            f for f in os.listdir(outdir)
            if not f.endswith((".part", ".ytdl"))
        ]

        if not files:
            st.error("Download finished but no file was produced.")

        else:

            fname = files[0]
            fpath = os.path.join(outdir, fname)

            if mode == "Video (MP4)":

                vcodec, acodec = get_codecs(dl_info)

                if not (is_h264(vcodec) and is_aac(acodec)):

                    bar.progress(
                        1.0,
                        text="Converting to a compatible format (H.264/AAC)..."
                    )

                    fpath = make_compatible(fpath, vcodec, acodec)
                    fname = os.path.basename(fpath)

            with open(fpath, "rb") as f:
                data = f.read()

            st.session_state.result = {
                "name": fname,
                "data": data
            }

            bar.progress(1.0, text="Done!")

    except yt_dlp.utils.DownloadError as e:
        st.error(f"Download failed: {str(e)[:500]}")

    except Exception as e:
        st.error(f"Error: {e}")

    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


# =========================================================
# DOWNLOAD RESULT
# =========================================================

if st.session_state.result:

    r = st.session_state.result

    mime = (
        "audio/mpeg"
        if r["name"].lower().endswith(".mp3")
        else "video/mp4"
    )

    st.success("Ready!")

    st.download_button(
        "💾 Save file",
        data=r["data"],
        file_name=r["name"],
        mime=mime
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown("""
<div class="footer">
    <strong style="color:#aebaff;">JIYA STUDIO</strong><br>
    Designed for a better media experience.<br>
    Only download content you own or have permission to download,
    and respect each platform's terms of service.
    <br><br>
    © 2026 Jiya Studio
</div>
""", unsafe_allow_html=True)


# Video Download 
