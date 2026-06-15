"""
Voice Generator Dashboard
"""
import streamlit as st
import os
from pathlib import Path
from piper_tts import PiperTTS

st.set_page_config(page_title="Voice Generator", page_icon="🎤", layout="wide")

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a1628 0%, #1a2a4a 50%, #0d1f3c 100%);
    }
    
    .main-header {
        background: linear-gradient(90deg, #0d47a1, #1565c0, #1976d2, #1e88e5);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px rgba(13, 71, 161, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .main-header h1 {
        font-size: 2.5em;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .main-header p {
        margin: 10px 0 0 0;
        opacity: 0.9;
        font-size: 1.1em;
    }
    
    .stSidebar {
        background: linear-gradient(180deg, #0d1f3c, #132744, #0d1f3c);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    .stSidebar h1, .stSidebar h2, .stSidebar h3 {
        color: #64b5f6 !important;
    }
    .stSidebar .stButton button {
        background: #1565c0 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        transition: all 0.3s;
    }
    .stSidebar .stButton button:hover {
        background: #1e88e5 !important;
        box-shadow: 0 4px 15px rgba(21, 101, 192, 0.4);
    }
    
    .stTextArea textarea {
        background: #1a2a4a !important;
        color: #e3f2fd !important;
        border: 1px solid #1565c0 !important;
        border-radius: 10px !important;
        font-size: 16px !important;
    }
    .stTextArea textarea:focus {
        border-color: #42a5f5 !important;
        box-shadow: 0 0 15px rgba(66, 165, 245, 0.2);
    }
    
    .stButton > button[type="primary"] {
        background: linear-gradient(90deg, #0d47a1, #1976d2) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 30px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(13, 71, 161, 0.4);
    }
    .stButton > button[type="primary"]:hover {
        background: linear-gradient(90deg, #1565c0, #1e88e5) !important;
        box-shadow: 0 6px 25px rgba(21, 101, 192, 0.6);
        transform: translateY(-2px);
    }
    
    .section-title {
        color: #64b5f6;
        font-size: 1.3em;
        font-weight: bold;
        border-bottom: 2px solid #1565c0;
        padding-bottom: 8px;
        margin-bottom: 15px;
    }
    
    .audio-card {
        background: linear-gradient(135deg, #132744, #1a3052);
        border: 1px solid rgba(100, 181, 246, 0.2);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    
    .stAlert {
        background: #132744 !important;
        border: 1px solid #1565c0 !important;
        color: #e3f2fd !important;
        border-radius: 10px !important;
    }
    
    [data-testid="stMetric"] {
        background: #132744;
        border: 1px solid rgba(100, 181, 246, 0.2);
        border-radius: 10px;
        padding: 10px;
    }
    [data-testid="stMetric"] label {
        color: #90caf9 !important;
    }
    [data-testid="stMetricValue"] {
        color: #e3f2fd !important;
    }
    
    .stFileUploader {
        border: 2px dashed #1565c0 !important;
        border-radius: 10px !important;
        padding: 20px !important;
        background: #0d1f3c !important;
    }
    
    .footer {
        text-align: center;
        color: #546e7a;
        padding: 20px;
        font-size: 0.9em;
    }
    
    .stSelectbox select {
        background: #1a2a4a !important;
        color: #e3f2fd !important;
        border: 1px solid #1565c0 !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #bbdefb !important;
    }
    p, span, label {
        color: #90caf9 !important;
    }
    .stCaption {
        color: #78909c !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("### 🎛️ Settings")
    
    voice = st.selectbox("Choose Voice:", ['Female (US)', 'Male (US)', 'Female (UK)'], index=0)
    
    if 'tts' not in st.session_state or st.session_state.get('current_voice') != voice:
        st.session_state.tts = PiperTTS(voice)
        st.session_state.current_voice = voice
    
    tts = st.session_state.tts
    
    st.markdown("---")
    
    st.markdown("### 📂 Upload File")
    uploaded_file = st.file_uploader("Choose .txt file", type=['txt'], label_visibility="collapsed")
    
    if uploaded_file is not None:
        file_text = uploaded_file.read().decode('utf-8')
        st.session_state.text = file_text
        st.success(f"✅ Loaded: {uploaded_file.name}")
    
    st.markdown("---")
    
    st.markdown("### 🗑️ Clear Files")
    if st.button("🗑️ Delete All Audio", use_container_width=True):
        audio_dir = Path("output/audio")
        if audio_dir.exists():
            count = 0
            for file in list(audio_dir.glob("*.mp3")) + list(audio_dir.glob("*.wav")):
                try:
                    file.unlink()
                    count += 1
                except:
                    pass
            st.success(f"✅ Deleted {count} files!")
            st.rerun()
    
    st.markdown("---")
    
    audio_dir = Path("output/audio")
    if audio_dir.exists():
        mp3_files = list(audio_dir.glob("*.mp3")) if audio_dir.exists() else []
        wav_files = list(audio_dir.glob("*.wav")) if audio_dir.exists() else []
        file_count = len(mp3_files) + len(wav_files)
        total_size = sum(f.stat().st_size for f in mp3_files if f.exists()) + sum(f.stat().st_size for f in wav_files if f.exists())
        st.caption(f"📊 Files: {file_count}")
        st.caption(f"💾 Size: {total_size/1024:.1f} KB")
    
    st.caption(f"🎤 {voice}")

# ==================== HEADER ====================
st.markdown("""
<div class="main-header">
    <h1>🎤 Voice Generator</h1>
    <p>Convert Text to Natural Speech</p>
</div>
""", unsafe_allow_html=True)

# ==================== MAIN CONTENT ====================
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown('<p class="section-title">📝 Input</p>', unsafe_allow_html=True)
    
    if 'text' not in st.session_state:
        st.session_state.text = ""
    
    text = st.text_area(
        "Enter text:",
        value=st.session_state.text,
        height=300,
        placeholder="Type your text here or upload a .txt file...",
        key="text_input",
        label_visibility="collapsed"
    )
    
    char_count = len(text.strip())
    st.caption(f"📊 {char_count} characters | ⏱️ ~{char_count/15:.1f}s")
    
    if st.button("🔊 Generate", type="primary", use_container_width=True):
        if text.strip():
            with st.spinner(f"🔄 Generating..."):
                try:
                    result = tts.synthesize(text)
                    st.session_state.last_audio = result['path']
                    st.session_state.last_duration = result['duration']
                    st.session_state.last_voice = result['voice']
                    st.success(f"✅ Done! | {result['duration']:.1f}s")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("⚠️ Please enter text")

with col2:
    st.markdown('<p class="section-title">🎧 Output</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="audio-card">', unsafe_allow_html=True)
    
    if 'last_audio' in st.session_state:
        audio_path = st.session_state.last_audio
        
        if Path(audio_path).exists():
            with open(audio_path, 'rb') as f:
                audio_bytes = f.read()
            st.audio(audio_bytes, format='audio/mp3')
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.download_button("📥 Download", audio_bytes, file_name=Path(audio_path).name, mime="audio/mp3", use_container_width=True)
            with col_b:
                st.metric("Duration", f"{st.session_state.last_duration:.1f}s")
        else:
            st.info("📭 File no longer exists")
    else:
        st.info("👆 Generate to see output")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== HISTORY ====================
st.markdown("---")
st.markdown('<p class="section-title">📊 History</p>', unsafe_allow_html=True)

audio_dir = Path("output/audio")
if audio_dir.exists():
    audio_files = sorted(list(audio_dir.glob("*.mp3")) + list(audio_dir.glob("*.wav")), key=os.path.getmtime, reverse=True)
    audio_files = [f for f in audio_files if f.exists()]
    
    if audio_files:
        st.caption(f"📂 {len(audio_files)} files")
        
        for audio_file in audio_files:
            if not audio_file.exists():
                continue
                
            c1, c2, c3, c4, c5 = st.columns([3, 1.5, 1, 1, 1])
            
            with c1:
                st.text(f"🎵 {audio_file.name}")
            
            with c2:
                st.caption(f"⏱️ ~{audio_file.stat().st_size/3000:.1f}s")
            
            with c3:
                size_kb = audio_file.stat().st_size / 1024
                st.caption(f"📦 {size_kb:.0f}KB")
            
            with c4:
                mime = "audio/mp3" if audio_file.suffix == ".mp3" else "audio/wav"
                with open(audio_file, 'rb') as f:
                    st.download_button("📥", f.read(), file_name=audio_file.name, key=f"dl_{audio_file.name}", mime=mime)
            
            with c5:
                if st.button("🗑️", key=f"del_{audio_file.name}"):
                    try:
                        audio_file.unlink()
                        st.rerun()
                    except:
                        pass
    else:
        st.info("📭 No files yet")

st.markdown("---")
st.markdown('<p class="footer">Voice Generator v1.0</p>', unsafe_allow_html=True)