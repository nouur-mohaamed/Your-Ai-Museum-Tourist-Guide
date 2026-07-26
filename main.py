import streamlit as st
import tempfile
import os

from generate_response import GenerativeLLM
from core_engine import (
    get_statue_info,
    get_context,
    answer_statue_related_questions,
)

from generate_translation import generate_translation
from generate_speech import generate_speech

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Museum Guide",
    page_icon="🏺",
    layout="wide"
)

# -----------------------------
# BLACK & GOLD MUSEUM THEME
# -----------------------------
# Palette
#   --ivory       #0D0D0D   main background (near-black)
#   --parchment   #1A1A1A   card / panel background
#   --ink         #F2F2F2   primary text (off-white)
#   --ink-soft    #B8B8B8   secondary text
#   --gold        #B8925A   antique/muted gold — accent, dividers, eyebrows
#   --gold-deep   #8A6B3D   bronze — borders, hover states
#   --terracotta  #B8925A   secondary accent (unified with gold)
#   --black       #000000   deep contrast panels
#
# Type
#   Display : "Playfair Display" — headlines, artifact name
#   Body    : "EB Garamond"      — running text, labels, UI

st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,500&family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">

<style>

:root{
    --ivory: #0A0A0A;
    --parchment: #161513;
    --parchment-soft: #131211;
    --ink: #EDE8DD;
    --ink-soft: #A69B87;
    --gold: #B8925A;
    --gold-deep: #8A6B3D;
    --gold-soft: rgba(184,146,90,0.25);
    --terracotta: #B8925A;
    --black: #000000;
    --radius-lg: 22px;
    --radius-md: 14px;
    --radius-sm: 10px;
}

/* ---------- base canvas ---------- */
html, body, #root{
    background: var(--ivory) !important;
}

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="stMain"],
[data-testid="stBottom"],
[data-testid="stBottomBlockContainer"]{
    background: var(--ivory) !important;
    color: var(--ink);
}

[data-testid="stHeader"]{
    background: var(--ivory) !important;
    border-bottom: 1px solid var(--gold-soft);
}

[data-testid="stToolbar"]{
    right: 1.5rem;
}

/* ---------- catch-all: kill any stray white portals/popovers ---------- */
div[data-baseweb="popover"],
div[data-baseweb="popover"] div,
div[data-baseweb="menu"],
ul[data-baseweb="menu"],
div[role="listbox"]{
    background: var(--parchment) !important;
    color: var(--ink) !important;
    border: 1px solid var(--gold-soft) !important;
}

li[role="option"]{
    background: var(--parchment) !important;
    color: var(--ink) !important;
}

li[role="option"]:hover,
li[aria-selected="true"]{
    background: var(--gold-soft) !important;
    color: var(--ink) !important;
}

[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p{
    color: var(--ink-soft) !important;
}

::-webkit-scrollbar{ width: 10px; height: 10px; }
::-webkit-scrollbar-track{ background: var(--ivory); }
::-webkit-scrollbar-thumb{ background: var(--gold-deep); border-radius: 10px; }

.block-container{
    padding-top: 2.5rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

/* ---------- typography ---------- */
html, body, [class*="css"]{
    font-family: 'EB Garamond', Georgia, serif;
    color: var(--ink);
    font-size: 1.08rem;
}

h1, h2, h3{
    font-family: 'Playfair Display', Georgia, serif !important;
    color: var(--ink) !important;
    letter-spacing: 0.2px;
    font-weight: 700 !important;
}

/* main title acts as a museum-placard headline */
h1{
    font-weight: 700 !important;
    font-size: 3.1rem !important;
    padding-bottom: 0.4rem;
    border-bottom: 3px solid var(--gold);
    border-radius: 2px;
    display: inline-block;
    margin-bottom: 0.7rem !important;
    line-height: 1.15 !important;
}

h2{
    font-weight: 700 !important;
    font-size: 1.85rem !important;
}

h3{
    font-weight: 700 !important;
    font-size: 1.3rem !important;
    color: var(--gold) !important;
    text-transform: uppercase;
    letter-spacing: 1.6px;
    font-family: 'EB Garamond', serif !important;
    font-style: italic;
}

p, span, label, div{
    font-family: 'EB Garamond', Georgia, serif;
}

/* intro caption under the title */
[data-testid="stMarkdownContainer"] p{
    font-size: 1.2rem;
    line-height: 1.65;
    color: var(--ink-soft);
}

/* story / body copy reads larger and more relaxed */
[data-testid="stMarkdownContainer"]{
    font-size: 1.15rem;
    line-height: 1.7;
}

/* ---------- horizontal rule / divider ---------- */
hr{
    border: none;
    border-top: 1.5px solid var(--gold);
    border-radius: 2px;
    margin: 2.2rem 0;
    position: relative;
}

/* ---------- selectbox (language) ---------- */
[data-testid="stSelectbox"] label{
    font-family: 'Playfair Display', serif !important;
    font-style: italic;
    color: var(--gold) !important;
    font-size: 1.05rem !important;
}

[data-testid="stSelectbox"] > div > div{
    background: var(--parchment) !important;
    border: 1px solid var(--gold) !important;
    border-radius: var(--radius-md) !important;
    color: var(--ink) !important;
    font-size: 1.05rem !important;
    padding: 0.2rem 0.3rem;
}

/* ---------- file uploader / camera ---------- */
[data-testid="stFileUploaderDropzone"]{
    background: var(--parchment) !important;
    border: 1.5px dashed var(--gold-deep) !important;
    border-radius: var(--radius-lg) !important;
    padding: 1.2rem !important;
}

[data-testid="stFileUploaderDropzone"] *{
    color: var(--ink-soft) !important;
    font-size: 1.02rem !important;
}

[data-testid="stCameraInput"]{
    background: var(--parchment) !important;
    border: 1.5px dashed var(--gold-deep) !important;
    border-radius: var(--radius-lg) !important;
    padding: 1rem !important;
}

[data-testid="stCameraInput"] video,
[data-testid="stCameraInput"] > div{
    border-radius: var(--radius-md) !important;
    overflow: hidden;
}

button[kind="secondary"], .stButton>button, [data-testid="stCameraInput"] button, [data-testid="stFileUploaderDropzone"] button, [data-testid="stBaseButton-secondary"]{
    background: var(--gold) !important;
    color: #FFFFFF !important;
    border: 1px solid var(--gold-deep) !important;
    border-radius: 999px !important;
    font-family: 'EB Garamond', serif !important;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    font-size: 0.95rem !important;
    padding: 0.5rem 1.4rem !important;
    transition: all 0.2s ease-in-out;
    font-weight: 700 !important;
}

button[kind="secondary"] p, .stButton>button p, [data-testid="stCameraInput"] button p, [data-testid="stFileUploaderDropzone"] button p, [data-testid="stBaseButton-secondary"] p{
    color: #FFFFFF !important;
    font-weight: 700 !important;
}

button[kind="secondary"]:hover, .stButton>button:hover{
    background: var(--gold-deep) !important;
    color: #FFFFFF !important;
    border-color: var(--gold) !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 14px rgba(184,146,90,0.35);
}

/* ---------- artifact image (no frame, full photo visible) ---------- */
[data-testid="stImage"]{
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}

[data-testid="stImage"] > div{
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

[data-testid="stImage"] img{
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    border-radius: var(--radius-lg);
    width: 100%;
    height: auto;
    object-fit: contain;
}

/* ---------- info panels (location / lifespan) ---------- */
[data-testid="column"]{
    padding: 0.4rem;
}

.mg-info-card{
    background: var(--parchment-soft);
    border: 1px solid var(--gold-soft);
    border-radius: var(--radius-md);
    padding: 0.9rem 1.2rem;
    margin-bottom: 0.9rem;
}

/* ---------- audio player ---------- */
audio{
    width: 100%;
    border-radius: var(--radius-md);
}

[data-testid="stAudio"]{
    background: var(--parchment-soft);
    border: 1px solid var(--gold-soft);
    border-radius: var(--radius-md);
    padding: 0.8rem 1rem;
}

/* ---------- chat ---------- */
[data-testid="stChatMessage"]{
    background: var(--parchment) !important;
    border: 1px solid var(--gold-soft);
    border-radius: var(--radius-md);
    padding: 0.8rem 1.1rem;
    font-size: 1.08rem;
}

/* avatar circles — override Streamlit's default blue/red with the theme palette */
[data-testid="stChatMessageAvatarUser"],
[data-testid="chatAvatarIcon-user"]{
    background-color: var(--gold) !important;
    color: var(--black) !important;
    border: 1px solid var(--gold-deep) !important;
}

[data-testid="stChatMessageAvatarAssistant"],
[data-testid="chatAvatarIcon-assistant"]{
    background-color: var(--black) !important;
    color: var(--gold) !important;
    border: 1px solid var(--gold) !important;
}

[data-testid="stChatMessageAvatarUser"] svg,
[data-testid="stChatMessageAvatarAssistant"] svg{
    fill: currentColor !important;
}

[data-testid="stChatInput"]{
    background: var(--ivory) !important;
    border: 1px solid var(--gold-soft) !important;
    border-radius: var(--radius-lg) !important;
    box-shadow: none !important;
}

[data-testid="stChatInput"] > div{
    background: var(--ivory) !important;
}

[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] textarea:disabled{
    background: var(--parchment) !important;
    border: 1px solid var(--gold-deep) !important;
    border-radius: var(--radius-lg) !important;
    color: var(--ink) !important;
    -webkit-text-fill-color: var(--ink-soft) !important;
    opacity: 1 !important;
    font-family: 'EB Garamond', serif !important;
    font-size: 1.08rem !important;
    padding: 0.7rem 1rem !important;
}

[data-testid="stChatInputSubmitButton"]{
    background: var(--gold-deep) !important;
    color: var(--black) !important;
    border-radius: 999px !important;
}

[data-testid="stChatInputSubmitButton"]:disabled{
    background: var(--gold-soft) !important;
    color: var(--ivory) !important;
    opacity: 1 !important;
}

/* ---------- spinner text ---------- */
[data-testid="stSpinner"] p{
    font-style: italic;
    color: var(--gold);
    font-size: 1.05rem;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# HERO / TITLE
# -----------------------------
st.markdown(
    """
    <div style="margin-bottom:0.2rem;">
        <span style="font-family:'EB Garamond',serif; font-style:italic; letter-spacing:3px;
        text-transform:uppercase; color:#B8925A; font-size:0.85rem;">Antiquities &amp; Heritage</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.title("🏛 AI Museum Tourist Guide")
st.write("Upload or capture an artifact and let the AI become your tour guide.")

# -----------------------------
# INITIALIZE
# -----------------------------

if "llm" not in st.session_state:
    st.session_state.llm = GenerativeLLM()

if "artifact" not in st.session_state:
    st.session_state.artifact = None

if "story" not in st.session_state:
    st.session_state.story = ""

if "location" not in st.session_state:
    st.session_state.location = ""

if "lifespan" not in st.session_state:
    st.session_state.lifespan = ""

if "name" not in st.session_state:
    st.session_state.name = ""

if "audio" not in st.session_state:
    st.session_state.audio = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "image_hash" not in st.session_state:
    st.session_state.image_hash = None

# -----------------------------
# LANGUAGE
# -----------------------------

language = st.selectbox(
    "Language",
    [
        "english",
        "french",
        "spanish"
    ]
)

# -----------------------------
# IMAGE INPUT
# -----------------------------

col1, col2 = st.columns(2)

with col1:
    uploaded = st.file_uploader(
        "Upload Image",
        type=["jpg","jpeg","png"]
    )

with col2:
    camera = st.camera_input(
        "Capture Image"
    )

image = uploaded if uploaded else camera

# -----------------------------
# PROCESS IMAGE
# -----------------------------

if image:

    image_bytes = image.getvalue()

    # Detect new uploaded image
    current_hash = hash(image_bytes)

    if current_hash != st.session_state.image_hash:

        st.session_state.image_hash = current_hash

        # Reset everything — new photo, clean slate, analysis not run yet
        st.session_state.messages = []
        st.session_state.story = ""
        st.session_state.audio = None
        st.session_state.location = ""
        st.session_state.lifespan = ""
        st.session_state.name = ""

    st.markdown("<br>", unsafe_allow_html=True)

    analyze_clicked = st.button(
        "🔍 Analyze Artifact" if st.session_state.story == "" else "🔍 Re-analyze Artifact",
        use_container_width=False
    )

    if analyze_clicked:

        # Save temporarily
        tmp = tempfile.NamedTemporaryFile(delete=False,suffix=".jpg")
        tmp.write(image_bytes)
        tmp.close()

        with st.spinner("Analyzing artifact..."):

            result = get_statue_info(
                tmp.name,
                llm=st.session_state.llm
            )

        os.remove(tmp.name)

        story = result["statue_info_text"]
        location = result["location"]
        lifespan = result["lifespan"]

        if language != "english":

            chunks = story.split("\n")

            translated_story = ""

            for chunk in chunks:

                if chunk.strip():
                    translated_story += generate_translation(
                        chunk,
                        target_lang=language,
                        src_lang="english"
                    ) + "\n"

            story = translated_story

            location = generate_translation(
                location,
                target_lang=language,
                src_lang="english"
            )
        audio = generate_speech(
            story,
            language
        )

        # Reset chat history for the newly generated story
        st.session_state.messages = []
        st.session_state.story = story
        st.session_state.location = location
        st.session_state.lifespan = lifespan
        st.session_state.audio = audio
        st.session_state.name = result["name"]

# -----------------------------
# DISPLAY
# -----------------------------

if st.session_state.story != "":

    st.markdown("<hr>", unsafe_allow_html=True)

    left, right = st.columns([1, 1])

    with left:

        st.image(f'statue_display_images/{st.session_state.name}.jpg', use_container_width=True)

        st.markdown(
            f"""
            <div class="mg-info-card">
                <h3 style="margin-bottom:0.2rem;">📍 Location</h3>
                <p style="margin:0;">{st.session_state.location}</p>
            </div>
            <div class="mg-info-card">
                <h3 style="margin-bottom:0.2rem;">⏳ Lifespan</h3>
                <p style="margin:0;">{st.session_state.lifespan}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with right:

        st.markdown(f"## {st.session_state.name}")

        st.markdown("### 🔊 Audio Guide")

        st.audio(
            st.session_state.audio,
            format="audio/wav"
        )

        st.write(st.session_state.story)

# -----------------------------
# CHAT
# -----------------------------

st.divider()

st.header("💬 Ask about this artifact")

CHAT_AVATARS = {"user": "🧑", "assistant": "🏺"}

for msg in st.session_state.messages:

    with st.chat_message(msg["role"], avatar=CHAT_AVATARS.get(msg["role"])):
        st.markdown(msg["content"])

chat_ready = st.session_state.story != ""

if not chat_ready:
    st.caption("🔒 Analyze an artifact above to unlock the chat.")

question = st.chat_input(
    "Ask a question..." if chat_ready else "Analyze an artifact first...",
    disabled=not chat_ready
)

if question and chat_ready:

    shown_question = question

    if language != "english":

        question = generate_translation(
            question,
            target_lang="english",
            src_lang=language
        )

    st.session_state.messages.append(
        {
            "role":"user",
            "content":shown_question
        }
    )

    with st.chat_message("user", avatar=CHAT_AVATARS["user"]):
        st.markdown(shown_question)

    with st.spinner("Thinking..."):
        prompt=f"in {st.session_state.name} data,{question}"
        context = get_context(prompt,st.session_state.name,3)

        answer = answer_statue_related_questions(
            name=st.session_state.name,
            query_related_context=context,
            query=question,
            llm=st.session_state.llm
        )

        if language != "english":

            answer = generate_translation(
                answer,
                target_lang=language,
                src_lang="english"
            )

    with st.chat_message("assistant", avatar=CHAT_AVATARS["assistant"]):
        st.markdown(answer)

    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":answer
        }
    )
