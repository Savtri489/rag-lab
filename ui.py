"""Shared look and helpers for every page."""
import html
import os

import streamlit as st

from rag_lab.pipeline import RAGPipeline

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

CSS = """<style>
.block-container{padding-top:1.5rem;max-width:1100px}
.hero{background:linear-gradient(120deg,#14213D 0%,#0F5C73 60%,#0F7B7D 100%);border-radius:16px;padding:42px 40px;margin-bottom:22px}
.hero h1{color:#fff !important;font-size:2.6rem;margin:4px 0 8px;letter-spacing:-.02em;padding:0}
.hero p{color:#D6E4EE !important;font-size:1.1rem;max-width:62ch;margin:0}
.hero .kicker{text-transform:uppercase;letter-spacing:.12em;font-size:.78rem;color:#F2A541 !important;font-weight:700;margin-bottom:0}
.sec{font-size:1.4rem;font-weight:700;margin:30px 0 12px;color:#14213D}
.card{background:#fff;border:1px solid #D5DDE7;border-radius:12px;padding:18px 20px;min-height:128px}
.card h3{margin:0 0 6px;font-size:1.05rem;color:#14213D;padding:0}
.card p{margin:0;color:#4A5A72;font-size:.95rem;line-height:1.5}
.num{display:block;font-weight:700;color:#0F7B7D;font-size:.85rem;margin-bottom:2px}
.pill{display:inline-block;padding:4px 14px;border-radius:99px;font-size:.85rem;font-weight:600}
.ok{background:#DDF3E6;color:#1F7A4D}.no{background:#F9E1DB;color:#B8432F}
.hit{background:#fff;border:1px solid #D5DDE7;border-radius:10px;padding:12px 16px;margin-bottom:10px}
.hit b{color:#14213D}.hit span{color:#5B6B82;font-size:.88rem}
.bar{height:6px;background:#E3E9F0;border-radius:3px;margin:6px 0 8px}
.bar i{display:block;height:100%;background:#F2A541;border-radius:3px}
.map{display:flex;gap:3px;height:48px;margin:6px 0 10px}
.map div{border-radius:6px;border:2px solid transparent;display:flex;align-items:center;justify-content:center;font-size:.75rem;color:#14213D}
.map div.top{border-color:#F2A541}
.note{background:#FFF6E5;border-left:4px solid #F2A541;border-radius:6px;padding:12px 16px;color:#14213D}
</style>"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)


def hero(kicker: str, title: str, sub: str):
    st.markdown(f'<div class="hero"><p class="kicker">{kicker}</p><h1>{title}</h1><p>{sub}</p></div>',
                unsafe_allow_html=True)


def section(text: str):
    st.markdown(f'<div class="sec">{text}</div>', unsafe_allow_html=True)


def cards(items, per_row=3):
    """items: list of (label, title, body). label is a small number or tag."""
    for start in range(0, len(items), per_row):
        row = items[start:start + per_row]
        for col, (label, title, body) in zip(st.columns(per_row), row):
            col.markdown(f'<div class="card"><span class="num">{label}</span><h3>{title}</h3><p>{body}</p></div>',
                         unsafe_allow_html=True)


def esc(text: str) -> str:
    return html.escape(text)


@st.cache_resource
def get_pipeline(strategy: str, size: int, overlap: int, k: int) -> RAGPipeline:
    pipe = RAGPipeline(strategy=strategy, size=size, overlap=overlap, k=k)
    pipe.ingest_folder(DATA)
    return pipe