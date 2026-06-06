import streamlit as st
import pandas as pd
from generator import generate_ads, analyze_url, get_pagespeed_data, analyze_mismatch, get_ga4_data
from scorer import score_ad

st.set_page_config(
    page_title="Google Marketing Toolkit",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Dark background */
    html, body, [data-testid="stAppViewContainer"], 
    [data-testid="stMainBlockContainer"], .main {
        background-color: #000000 !important;
        color: #ffffff !important;
    }
    
    /* Fixed sidebar */
    [data-testid="stSidebar"] {
        background-color: #1a1a1a !important;
        border-right: 1px solid #333333 !important;
        position: fixed !important;
        left: 0 !important;
        top: 0 !important;
        height: 100vh !important;
        width: 250px !important;
        z-index: 99 !important;
        overflow-y: auto !important;
    }
    
    /* Adjust main content for fixed sidebar */
    [data-testid="stMainBlockContainer"] {
        margin-left: 250px !important;
        padding: 2rem !important;
    }
    
    /* Hide hamburger menu completely */
    button[kind="header"] {
        display: none !important;
    }
    
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    /* Styling */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 50%, #38bdf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .hero-sub {
        text-align: center;
        color: #a0aec0;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    .card {
        background: #1a1a1a !important;
        border: 1px solid #333333 !important;
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px rgba(14,165,233,0.1);
    }
    
    .winner-banner {
        background: linear-gradient(135deg, #0a3e54, #1a5f7a) !important;
        border: 1px solid #0284c7 !important;
        border-radius: 16px;
        padding: 1.2rem 1.5rem;
        text-align: center;
        margin: 1.5rem 0;
    }
    
    .trigger-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
    }
    
    .badge-urgency { background: #7f1d1d; color: #fca5a5; }
    .badge-social { background: #1e3a8a; color: #93c5fd; }
    .badge-fomo { background: #78350f; color: #fcd34d; }
    .badge-value { background: #15803d; color: #86efac; }
    
    .headline { font-size: 1.3rem; font-weight: 800; color: #e0f2fe; margin: 0.5rem 0; }
    .description { color: #cbd5e1; font-size: 0.9rem; line-height: 1.6; margin-bottom: 0.8rem; }
    .why-text { color: #94a3b8; font-size: 0.8rem; font-style: italic; border-left: 2px solid #0284c7; padding-left: 0.8rem; }
    
    .score-pill { display: inline-block; padding: 6px 16px; border-radius: 20px; font-weight: 700; font-size: 0.85rem; margin-bottom: 0.8rem; }
    .score-high { background: #1b5e20; color: #86efac; }
    .score-medium { background: #6b3d10; color: #fcd34d; }
    .score-low { background: #7f1d1d; color: #fca5a5; }
    
    .section-title { font-size: 1.5rem; font-weight: 800; color: #e0f2fe; margin: 2rem 0 1rem 0; }
    
    .stButton > button {
        background: linear-gradient(135deg, #0ea5e9, #0284c7) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 0.7rem 1.5rem !important;
        width: 100% !important;
    }
    
    input, textarea, select {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #333333 !important;
        border-radius: 8px !important;
    }
    
    [data-testid="stTextInput"] input {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🧭 Navigation")
    st.markdown("---")
    page = st.radio("", ["🎯 Ad Copy Simulator", "🔍 SEO Analyzer", "⚠️ Mismatch Detector", "📊 GA4 Analyzer"])
    st.markdown("---")
    st.markdown('<div style="color:#94a3b8; font-size:0.75rem;">Powered by Groq LLaMA 3.3 · Built with Streamlit</div>', unsafe_allow_html=True)

def get_badge(trigger):
    t = trigger.lower()
    badges = {
        "urgency": ("Urgency", "badge-urgency"),
        "social proof": ("Social Proof", "badge-social"),
        "fomo": ("FOMO", "badge-fomo"),
        "value": ("Value/Saving", "badge-value"),
        "problem": ("Problem-Solution", "badge-value"),
    }
    for key, (label, cls) in badges.items():
        if key in t:
            return label, cls
    return trigger, "badge-urgency"

def get_score_class(score):
    if score >= 75: return "score-high"
    if score >= 50: return "score-medium"
    return "score-low"

# ══════════════════════════════════════════
# PAGE 1 — AD COPY SIMULATOR
# ══════════════════════════════════════════
if page == "🎯 Ad Copy Simulator":
    st.markdown('<div class="hero-title">🎯 Ad Copy Simulator</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Generate 5 AI-powered Google Ad variations and find your winner instantly</div>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### ✍️ Your Product Details")
        st.markdown("---")
        product  = st.text_input("Product / Service", placeholder="e.g. Online Yoga Classes")
        audience = st.text_input("Target Audience",   placeholder="e.g. Working women aged 25-40")
        benefit  = st.text_input("Key Benefit",        placeholder="e.g. Lose weight in 30 days")
        tone     = st.selectbox("Tone", ["Urgent", "Friendly", "Professional", "Playful"])
        st.markdown("---")
        generate = st.button("🚀 Generate Ads")

    if generate:
        if not product or not audience or not benefit:
            st.warning("Please fill in all fields!")
        else:
            with st.spinner("✨ Generating your 5 ad variations..."):
                raw_output = generate_ads(product, audience, benefit, tone)

            variations = raw_output.strip().split("VARIATION")[1:]
            scores_data = []
            parsed = []

            for var in variations:
                lines = var.strip().split("\n")
                headline = next((l.replace("Headline:","").strip() for l in lines if "Headline:" in l), "N/A")
                description = next((l.replace("Description:","").strip() for l in lines if "Description:" in l), "N/A")
                trigger = next((l.replace("Trigger:","").strip() for l in lines if "Trigger:" in l), "N/A")
                why = next((l.replace("Why this works:","").strip() for l in lines if "Why this works:" in l), "")
                score, reasons = score_ad(headline, description)
                parsed.append((headline, description, trigger, why, score, reasons))
                scores_data.append({"Variation": f"V{len(parsed)} · {trigger}", "Score": score})

            best_score = max(s["Score"] for s in scores_data)
            cols = st.columns(len(parsed))

            for i, ((headline, description, trigger, why, score, reasons), col) in enumerate(zip(parsed, cols)):
                label, badge_cls = get_badge(trigger)
                score_cls = get_score_class(score)
                is_winner = score == best_score
                winner_tag = "🏆 WINNER · " if is_winner else ""
                with col:
                    st.markdown(f"""
                    <div class="card" style="border: 2px solid {'#0ea5e9' if is_winner else '#333333'};">
                        <div style="font-size:0.7rem; color:#a0aec0; font-weight:700; letter-spacing:1px; margin-bottom:4px;">{winner_tag}VARIATION {i+1}</div>
                        <span class="trigger-badge {badge_cls}">{label}</span><br>
                        <span class="score-pill {score_cls}">⚡ {score}/100</span>
                        <div class="headline">{headline}</div>
                        <div class="description">{description}</div>
                        <div class="why-text">💡 {why}</div>
                        <div style="margin-top:1rem; font-size:0.8rem;">
                            {''.join(f'<div style="color:#{"86efac" if "✅" in r else "fca5a5"}; margin:2px 0;">{r}</div>' for r in reasons)}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            winner = scores_data[[s["Score"] for s in scores_data].index(best_score)]
            st.markdown(f"""
            <div class="winner-banner">
                <div style="font-size:1.5rem; font-weight:900; color:#38bdf8;">🏆 Winner: {winner['Variation']}</div>
                <div style="color:#cbd5e1; margin-top:4px;">Scored {winner['Score']}/100</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="section-title">📊 Score Comparison</div>', unsafe_allow_html=True)
            df = pd.DataFrame(scores_data).set_index("Variation")
            st.bar_chart(df, color="#0ea5e9")

            st.markdown('<div class="section-title">📥 Export Results</div>', unsafe_allow_html=True)
            csv = pd.DataFrame(scores_data).to_csv(index=False)
            st.download_button("⬇️ Download as CSV", csv, "ad_results.csv", "text/csv")

# ══════════════════════════════════════════
# PAGE 2 — SEO ANALYZER
# ══════════════════════════════════════════
elif page == "🔍 SEO Analyzer":
    st.markdown('<div class="hero-title">🔍 SEO Analyzer</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Get real Google PageSpeed scores + AI-powered SEO recommendations</div>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### 🔍 Page Details")
        st.markdown("---")
        url = st.text_input("Page URL", placeholder="e.g. https://yoursite.com/page")
        content = st.text_area("Page Content / Description", placeholder="Describe your page...", height=150)
        analyze = st.button("🔍 Analyze Page")

    if analyze:
        if not url or not content:
            st.warning("Please fill in both fields!")
        else:
            with st.spinner("⚡ Fetching real Google PageSpeed data..."):
                speed_data = get_pagespeed_data(url)
            with st.spinner("🤖 Running AI SEO analysis..."):
                raw = analyze_url(url, content)

            lines = raw.strip().split("\n")
            def extract(label):
                return next((l.replace(label,"").strip() for l in lines if l.startswith(label)), "N/A")

            title_current = extract("Current:")
            title_suggest = extract("Suggested:")
            title_why = extract("Why:")
            intent_type = extract("Type:")
            intent_exp = extract("Explanation:")
            issues = [l.split(":",1)[-1].strip() for l in lines if l.startswith("Issue")]
            wins = [l.split(":",1)[-1].strip() for l in lines if l.startswith("Win")]

            if not speed_data.get("error"):
                st.markdown('<div class="section-title">📊 Real Google Scores</div>', unsafe_allow_html=True)
                c1, c2, c3, c4 = st.columns(4)
                for col, label, val in [
                    (c1, "⚡ Performance", speed_data["performance"]),
                    (c2, "🔍 SEO", speed_data["seo"]),
                    (c3, "♿ Accessibility", speed_data["accessibility"]),
                    (c4, "✅ Best Practices", speed_data["best_practices"])
                ]:
                    color = "#86efac" if val >= 70 else "#fcd34d" if val >= 40 else "#fca5a5"
                    col.markdown(f"""
                    <div style="background:#1a1a1a; border:1px solid #333333; border-radius:20px; padding:1.5rem; text-align:center; box-shadow:0 4px 20px rgba(14,165,233,0.1);">
                        <div style="font-size:0.75rem; color:#a0aec0; font-weight:700; letter-spacing:1px; text-transform:uppercase;">{label}</div>
                        <div style="font-size:2.5rem; font-weight:900; color:{color};">{val}</div>
                        <div style="font-size:0.8rem; color:#cbd5e1;">out of 100</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown('<div class="section-title">⏱️ Core Web Vitals</div>', unsafe_allow_html=True)
                v1, v2, v3 = st.columns(3)
                for col, label, val in [
                    (v1, "First Contentful Paint", speed_data["fcp"]),
                    (v2, "Largest Contentful Paint", speed_data["lcp"]),
                    (v3, "Cumulative Layout Shift", speed_data["cls"])
                ]:
                    col.markdown(f"""
                    <div style="background:#1a1a1a; border:1px solid #333333; border-radius:20px; padding:1.5rem; text-align:center; box-shadow:0 4px 20px rgba(14,165,233,0.1);">
                        <div style="font-size:0.75rem; color:#a0aec0; font-weight:700; letter-spacing:1px; text-transform:uppercase;">{label}</div>
                        <div style="font-size:1.8rem; font-weight:900; color:#38bdf8;">{val}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning(f"PageSpeed error: {speed_data['error']}")

            intent_colors = {
                "Informational": ("#1e3a8a","#93c5fd"),
                "Transactional": ("#15803d","#86efac"),
                "Navigational": ("#78350f","#fcd34d"),
                "Commercial": ("#5b21b6","#d8b4fe"),
            }
            bg, fg = intent_colors.get(intent_type, ("#0a3e54","#38bdf8"))
            st.markdown(f"""
            <div style="background:{bg}; border-radius:16px; padding:1.2rem 1.5rem; margin:1.5rem 0;">
                <div style="font-size:0.75rem; color:#a0aec0; font-weight:700; letter-spacing:1px; text-transform:uppercase; margin-bottom:4px;">Search Intent</div>
                <div style="font-size:1.3rem; font-weight:800; color:{fg};">{intent_type}</div>
                <div style="color:#cbd5e1; font-size:0.85rem; margin-top:4px;">{intent_exp}</div>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="card">
                    <div style="font-size:0.75rem; color:#38bdf8; font-weight:700; letter-spacing:1px; text-transform:uppercase; margin-bottom:0.8rem;">📝 Title Tag</div>
                    <div style="font-size:0.8rem; color:#cbd5e1; margin-bottom:4px;">Current</div>
                    <div style="color:#e0f2fe; font-size:0.9rem; margin-bottom:1rem; padding:0.5rem; background:#0f172a; border-radius:8px;">{title_current}</div>
                    <div style="font-size:0.8rem; color:#86efac; margin-bottom:4px; font-weight:700;">✅ Suggested</div>
                    <div style="color:#e0f2fe; font-size:0.95rem; font-weight:700; padding:0.5rem; background:#0a3e54; border-radius:8px; border-left:3px solid #0ea5e9;">{title_suggest}</div>
                    <div style="color:#94a3b8; font-size:0.8rem; font-style:italic; margin-top:0.8rem; border-left:2px solid #0284c7; padding-left:0.8rem;">{title_why}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="card">
                    <div style="font-size:0.75rem; color:#cbd5e1; font-weight:700; letter-spacing:1px; text-transform:uppercase; margin-bottom:0.8rem;">📄 Issues & Wins</div>
                    <div style="font-size:0.8rem; color:#fca5a5; margin-bottom:4px; font-weight:700;">❌ Issues</div>
                    {''.join(f'<div style="color:#e0f2fe; font-size:0.85rem; padding:0.3rem 0;">{i}</div>' for i in issues if i)}
                    <div style="font-size:0.8rem; color:#86efac; margin-top:1rem; margin-bottom:4px; font-weight:700;">✅ Quick Wins</div>
                    {''.join(f'<div style="color:#e0f2fe; font-size:0.85rem; padding:0.3rem 0;">{w}</div>' for w in wins if w)}
                </div>
                """, unsafe_allow_html=True)

# ══════════════════════════════════════════
# PAGE 3 — MISMATCH DETECTOR
# ══════════════════════════════════════════
elif page == "⚠️ Mismatch Detector":
    st.markdown('<div class="hero-title">⚠️ Mismatch Detector</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Find why your Google Ads Quality Score is low</div>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### ⚠️ Your Ad Details")
        st.markdown("---")
        ad_headline = st.text_input("Ad Headline", placeholder="e.g. Best Yoga Classes Online")
        ad_description = st.text_area("Ad Description", placeholder="e.g. Join 10,000+ students. Start free today!", height=100)
        landing_url = st.text_input("Landing Page URL", placeholder="e.g. https://yoursite.com/yoga")
        st.markdown("---")
        detect = st.button("⚠️ Detect Mismatches")

    if detect:
        if not ad_headline or not ad_description or not landing_url:
            st.warning("Please fill in all fields!")
        else:
            with st.spinner("🔍 Analyzing..."):
                raw = analyze_mismatch(ad_headline, ad_description, landing_url)

            lines = raw.strip().split("\n")
            def ext(label):
                return next((l.replace(label,"").strip() for l in lines if l.startswith(label)), "N/A")

            match_score = ext("MATCH SCORE:")
            verdict = ext("VERDICT:")
            qs_score = ext("Expected Quality Score:")
            cpc_impact = ext("CPC Impact:")
            promises = [l.split(":",1)[-1].strip() for l in lines if l.startswith("Promise")]
            delivers = [l.split(":",1)[-1].strip() for l in lines if l.startswith("Delivers")]
            mismatches = [l.split(":",1)[-1].strip() for l in lines if l.startswith("Mismatch")]
            fixes = [l.split(":",1)[-1].strip() for l in lines if l.startswith("Fix")]

            try:
                score_num = int(''.join(filter(str.isdigit, match_score)))
            except:
                score_num = 50

            score_color = "#86efac" if score_num >= 75 else "#fcd34d" if score_num >= 50 else "#fca5a5"

            st.markdown(f"""
            <div class="card" style="text-align:center; padding:2rem; margin-bottom:1.5rem;">
                <div style="font-size:0.85rem; color:#a0aec0; font-weight:700; letter-spacing:1px; text-transform:uppercase;">Message Match Score</div>
                <div style="font-size:4rem; font-weight:900; color:{score_color};">{score_num}</div>
                <div style="font-size:0.9rem; color:#cbd5e1;">out of 100</div>
                <div style="background:#333333; border-radius:999px; height:12px; margin:1rem auto; max-width:300px;">
                    <div style="background:{score_color}; width:{score_num}%; height:12px; border-radius:999px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="card">
                    <div style="font-size:0.75rem; color:#38bdf8; font-weight:700; letter-spacing:1px; text-transform:uppercase; margin-bottom:0.8rem;">Verdict</div>
                    <div style="font-size:1.3rem; font-weight:800; color:#38bdf8;">{verdict}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="card">
                    <div style="font-size:0.75rem; color:#a0aec0; font-weight:700; letter-spacing:1px; text-transform:uppercase; margin-bottom:0.8rem;">Quality Score Impact</div>
                    <div style="font-size:1.1rem; font-weight:800; color:#38bdf8;">Score: {qs_score}/10 · {cpc_impact}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            col3, col4 = st.columns(2)
            with col3:
                st.markdown(f"""
                <div class="card">
                    <div style="font-size:0.75rem; color:#38bdf8; font-weight:700; letter-spacing:1px; text-transform:uppercase; margin-bottom:0.8rem;">📢 Ad Promises</div>
                    {''.join(f'<div style="color:#e0f2fe; font-size:0.9rem; padding:0.5rem 0; border-bottom:1px solid #333333;">🔵 {p}</div>' for p in promises if p)}
                </div>
                """, unsafe_allow_html=True)
            with col4:
                st.markdown(f"""
                <div class="card">
                    <div style="font-size:0.75rem; color:#86efac; font-weight:700; letter-spacing:1px; text-transform:uppercase; margin-bottom:0.8rem;">🌐 Page Delivers</div>
                    {''.join(f'<div style="color:#e0f2fe; font-size:0.9rem; padding:0.5rem 0; border-bottom:1px solid #333333;">✅ {d}</div>' for d in delivers if d)}
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            col5, col6 = st.columns(2)
            with col5:
                st.markdown(f"""
                <div class="card" style="background:#3d1a1a !important; border:1px solid #7f1d1d !important;">
                    <div style="font-size:0.75rem; color:#fca5a5; font-weight:700; letter-spacing:1px; text-transform:uppercase; margin-bottom:0.8rem;">❌ Mismatches</div>
                    {''.join(f'<div style="color:#e0f2fe; font-size:0.9rem; padding:0.5rem 0; border-bottom:1px solid #7f1d1d;">⚠️ {m}</div>' for m in mismatches if m)}
                </div>
                """, unsafe_allow_html=True)
            with col6:
                st.markdown(f"""
                <div class="card" style="background:#1b5e20 !important; border:1px solid #4caf50 !important;">
                    <div style="font-size:0.75rem; color:#86efac; font-weight:700; letter-spacing:1px; text-transform:uppercase; margin-bottom:0.8rem;">🔧 Fixes</div>
                    {''.join(f'<div style="color:#e0f2fe; font-size:0.9rem; padding:0.5rem 0; border-bottom:1px solid #4caf50;">✅ {f}</div>' for f in fixes if f)}
                </div>
                """, unsafe_allow_html=True)

# ══════════════════════════════════════════
# PAGE 4 — GA4 ANALYZER
# ══════════════════════════════════════════
elif page == "📊 GA4 Analyzer":
    st.markdown('<div class="hero-title">📊 GA4 Drop-Off Analyzer</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Real data from your Google Analytics — find where customers leave</div>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### 📊 GA4 Settings")
        st.markdown("---")
        property_id = st.text_input("GA4 Property ID", value="153293282", placeholder="Your GA4 Property ID")
        analyze_ga4 = st.button("📊 Analyze My GA4 Data")

    if analyze_ga4:
        with st.spinner("🔍 Connecting to your Google Analytics..."):
            try:
                pages = get_ga4_data(property_id, "credentials.json")

                if not pages:
                    st.warning("No data found. Check your Property ID.")
                else:
                    st.success("✅ Successfully pulled data from GA4")
                    pages_sorted = sorted(pages, key=lambda x: x["bounce_rate"], reverse=True)
                    INDUSTRY_AVG = 45.0

                    st.markdown('<div class="section-title">🚨 Drop-Off Pages</div>', unsafe_allow_html=True)

                    for page_data in pages_sorted[:5]:
                        bounce = page_data["bounce_rate"]
                        diff = round(bounce - INDUSTRY_AVG, 1)
                        color = "#fca5a5" if bounce > 60 else "#fcd34d" if bounce > 40 else "#86efac"
                        status = "🔴 Critical" if bounce > 60 else "🟡 Warning" if bounce > 40 else "🟢 Healthy"

                        st.markdown(f"""
                        <div class="card">
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
                                <div style="font-size:1rem; font-weight:800; color:#e0f2fe;">{page_data["page"]}</div>
                                <div style="font-size:0.85rem; font-weight:700; color:{color};">{status}</div>
                            </div>
                            <div style="display:flex; gap:1rem; margin-bottom:1rem; flex-wrap:wrap;">
                                <div style="background:#0a3e54; border-radius:12px; padding:0.5rem 1rem; text-align:center;">
                                    <div style="font-size:0.7rem; color:#a0aec0; font-weight:700;">SESSIONS</div>
                                    <div style="font-size:1.2rem; font-weight:900; color:#38bdf8;">{page_data["sessions"]}</div>
                                </div>
                                <div style="background:#0a3e54; border-radius:12px; padding:0.5rem 1rem; text-align:center;">
                                    <div style="font-size:0.7rem; color:#a0aec0; font-weight:700;">BOUNCE RATE</div>
                                    <div style="font-size:1.2rem; font-weight:900; color:{color};">{bounce}%</div>
                                </div>
                                <div style="background:#0a3e54; border-radius:12px; padding:0.5rem 1rem; text-align:center;">
                                    <div style="font-size:0.7rem; color:#a0aec0; font-weight:700;">AVG DURATION</div>
                                    <div style="font-size:1.2rem; font-weight:900; color:#38bdf8;">{int(page_data["avg_duration"])}s</div>
                                </div>
                                <div style="background:{'#7f1d1d' if diff > 0 else '#1b5e20'}; border-radius:12px; padding:0.5rem 1rem; text-align:center;">
                                    <div style="font-size:0.7rem; color:#a0aec0; font-weight:700;">VS INDUSTRY</div>
                                    <div style="font-size:1.2rem; font-weight:900; color:{color};">{'+'if diff>0 else ''}{diff}%</div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    avg_bounce = round(sum(p["bounce_rate"] for p in pages) / len(pages), 1)
                    total_sessions = sum(p["sessions"] for p in pages)
                    st.markdown(f"""
                    <div class="winner-banner">
                        <div style="font-size:1.2rem; font-weight:900; color:#38bdf8;">📊 Summary — Last 30 Days</div>
                        <div style="color:#cbd5e1; margin-top:8px;">Sessions: <b>{total_sessions}</b> · Avg Bounce: <b>{avg_bounce}%</b> · Industry: <b>45%</b></div>
                        <div style="color:#cbd5e1; margin-top:4px;">{'🔴 Above industry average' if avg_bounce > 45 else '🟢 Better than industry'}</div>
                    </div>
                    """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Make sure credentials.json exists and GA4 API is enabled.")