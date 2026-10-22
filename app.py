import base64
import pathlib
import streamlit as st
import numpy as np
import pandas as pd
import pickle

st.set_page_config(page_title="The Enchanted Athenaeum", page_icon="📜", layout="wide")

# ---------------------------------------------------------
# Themes
#   dark  = Dark Academia (Cowhide Cocoa / Spiced Wine / Toasted Caramel / Olive Harvest / Golden Batter)
#   light = Cottagecore   (Lace White / Oatmeal / Cream / Mushroom / Linen)
# `face` = (css family name, file stem in ./fonts/). Drop poisoned-heart.otf / anaktoria.ttf
# into a fonts/ folder to use the real fonts; otherwise the Google Font fallback is used.
# ---------------------------------------------------------
THEMES = {
    "dark": dict(
        bg="#442D1C", text="#E8D1A7", muted="#C2B58C", accent="#84592B", title="#E8D1A7",
        card="#52361F", border="#84592B", hdr="linear-gradient(135deg,#743014,#442D1C)",
        hdr_border="#84592B", hdr_sub="#E8D1A7", badge_bg="#743014", badge_fg="#E8D1A7",
        badge_border="#8D8F67", btn_bg="#743014", btn_fg="#E8D1A7", input_bg="#52361F",
        shadow="rgba(0,0,0,.5)", rule="solid", deco="🕯️",
        face=("PoisonedHeart", "poisoned-heart"),
        font_title="'PoisonedHeart','Playfair Display'",
    ),
    "light": dict(
        bg="#F7F2EA", text="#4A3F35", muted="#8A7A69", accent="#C7B5A3", title="#5C4A3A",
        card="#FFFDF8", border="#D9CBB5", hdr="linear-gradient(135deg,#E9DFCF,#F5EBCF)",
        hdr_border="#C7B5A3", hdr_sub="#8A7A69", badge_bg="#E8DFD0", badge_fg="#5C4A3A",
        badge_border="#C7B5A3", btn_bg="#C7B5A3", btn_fg="#3E322A", input_bg="#FFFDF8",
        shadow="rgba(120,100,80,.15)", rule="dashed", deco="🌿",
        face=("Anaktoria", "anaktoria"),
        font_title="'Anaktoria','Almendra'",
    ),
}

def font_face(family, stem):
    """Embed a local font file from ./fonts/ if present."""
    for ext, fmt in (("woff2", "woff2"), ("otf", "opentype"), ("ttf", "truetype")):
        p = pathlib.Path("fonts") / f"{stem}.{ext}"
        if p.exists():
            b64 = base64.b64encode(p.read_bytes()).decode()
            return f"@font-face{{font-family:'{family}';src:url(data:font/{ext};base64,{b64}) format('{fmt}');}}"
    return ""

def inject_css(t):
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Almendra:ital,wght@0,400;0,700;1,400&family=Lora:ital,wght@0,400;0,600;1,400&family=Playfair+Display:ital,wght@0,700;1,700&display=swap');
{font_face(*t['face'])}

.stApp, [data-testid="stHeader"] {{ background:{t['bg']} !important; color:{t['text']} !important; }}
html, body, [class*="css"], label, p, .stMarkdown {{ font-family:'Lora',serif !important; color:{t['text']}; }}
h1,h2,h3 {{ font-family:{t['font_title']},serif !important; color:{t['title']} !important; font-weight:700; }}
[data-testid="stCaptionContainer"] p {{ color:{t['muted']} !important; font-style:italic; }}
hr {{ border-top:1px {t['rule']} {t['border']} !important; }}

/* Header */
.library-header {{ background:{t['hdr']}; border:1px solid {t['hdr_border']}; border-radius:14px;
  box-shadow:0 10px 30px {t['shadow']}; padding:2.5rem; text-align:center; margin-bottom:2rem; }}
.library-header h1 {{ font-size:3.2rem; margin:0 0 .5rem; }}
.library-header p {{ color:{t['hdr_sub']}; font-style:italic; font-size:1.1rem; margin:0; }}

/* Cards */
.book-card {{ background:{t['card']}; border:1px {t['rule']} {t['border']}; border-left:5px solid {t['accent']};
  border-radius:10px; padding:1.4rem 1.6rem; margin-bottom:1.2rem; box-shadow:0 4px 15px {t['shadow']};
  transition:transform .2s, border-color .2s; }}
.book-card:hover {{ transform:translateY(-3px); border-color:{t['title']}; }}
.book-title {{ font-family:{t['font_title']},serif; color:{t['title']}; font-size:1.5rem; font-weight:700; margin-bottom:.3rem; }}
.book-author {{ color:{t['muted']}; font-style:italic; margin-bottom:.8rem; }}
.match-badge {{ display:inline-block; background:{t['badge_bg']}; color:{t['badge_fg']};
  border:1px solid {t['badge_border']}; padding:.25rem .8rem; border-radius:20px; font-size:.85rem; font-weight:600; }}

/* Widgets */
div[data-baseweb="select"] > div {{ background:{t['input_bg']} !important; border:1px solid {t['border']} !important;
  color:{t['text']} !important; border-radius:8px !important; }}
div[data-baseweb="select"] * {{ color:{t['text']} !important; }}
div[data-baseweb="popover"] li, div[data-baseweb="popover"] ul {{ background:{t['input_bg']} !important; color:{t['text']} !important; }}
[data-testid="stSlider"] [role="slider"] {{ background:{t['accent']} !important; }}
[data-testid="stSlider"] [data-testid="stTickBar"] *, [data-testid="stSliderThumbValue"] {{ color:{t['text']} !important; }}
.stButton > button {{ width:100%; background:{t['btn_bg']}; color:{t['btn_fg']}; border:1px solid {t['border']};
  border-radius:8px; font-family:{t['font_title']},serif; font-size:1.2rem; padding:.5rem 1rem; transition:all .3s; }}
.stButton > button:hover {{ border-color:{t['title']}; color:{t['btn_fg']}; transform:translateY(-2px); box-shadow:0 4px 12px {t['shadow']}; }}
[data-testid="stToggle"] p {{ color:{t['text']} !important; }}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Theme toggle
# ---------------------------------------------------------
_, col_toggle = st.columns([5, 1])
with col_toggle:
    dark = st.toggle("🌙 Dark Academia", value=True, help="Off = Cottagecore 🌸")
t = THEMES["dark" if dark else "light"]
inject_css(t)

# ---------------------------------------------------------
# Data & model
# ---------------------------------------------------------
@st.cache_resource
def load_model_artifacts():
    with open('svd_cf_model.pkl', 'rb') as f:
        return pickle.load(f)['book_features']

@st.cache_data
def load_datasets():
    df = pd.read_csv('final_dataset.csv')
    return (df[['book_index', 'book_id', 'title', 'authors']]
            .drop_duplicates('book_index').set_index('book_index'))

book_features = load_model_artifacts()
book_map = load_datasets()

norms = np.linalg.norm(book_features, axis=1, keepdims=True)
norms[norms == 0] = 1.0
normalized_book_features = book_features / norms

def recommend_similar_books(idx, n=5):
    sims = (normalized_book_features @ normalized_book_features[idx]).flatten()
    sims[idx] = -1.0  # exclude self
    top = np.argsort(sims)[-n:][::-1]
    recs = book_map.loc[top].copy()
    recs['similarity_score'] = sims[top]
    return recs

# ---------------------------------------------------------
# Interface
# ---------------------------------------------------------
quote = ("A room without books is like a body without a soul." if dark
         else "Where there are books, there is always a little garden.")
author = "Cicero" if dark else "an old cottage proverb"
icon = "📜" if dark else "🌸"

st.markdown(f"""
<div class="library-header">
    <h1>{icon} The Enchanted Athenaeum</h1>
    <p>"{quote}" — {author}</p>
</div>
""", unsafe_allow_html=True)

col_input, _ = st.columns([2, 1])
with col_input:
    selected_title = st.selectbox(
        f"{t['deco']} Select or search for a tome you cherished:",
        sorted(book_map['title'].dropna().unique()))
    num_recs = st.slider("✨ Number of recommendations to unveil:", 1, 10, 5)
    generate_btn = st.button("🔮 Uncover Similar Reads")

if generate_btn:
    matched = book_map[book_map['title'] == selected_title]
    if matched.empty:
        st.error("That volume was not found in the archives.")
    else:
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader(f"{t['deco']} Books aligned with *{selected_title}*")
        st.caption(f"By {matched.iloc[0]['authors']}")
        st.markdown("---")

        with st.spinner("Consulting latent vector archives..."):
            recs = recommend_similar_books(matched.index[0], num_recs)

        for _, row in recs.iterrows():
            pct = max(0, row['similarity_score']) * 100
            st.markdown(f"""
            <div class="book-card">
                <div class="book-title">📖 {row['title']}</div>
                <div class="book-author">by {row['authors']}</div>
                <span class="match-badge">✨ {pct:.1f}% Reader Alignment</span>
            </div>
            """, unsafe_allow_html=True)