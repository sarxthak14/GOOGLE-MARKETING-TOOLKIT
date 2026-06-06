import streamlit as st
import pandas as pd
from generator import generate_ads, analyze_url, get_pagespeed_data, analyze_mismatch, get_ga4_data
from scorer import score_ad

st.set_page_config(
    page_title="Google Marketing Toolkit",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Dark theme CSS
st.markdown("""
<style>
    body { background-color: #000000 !important; color: #ffffff !important; }
    [data-testid="stAppViewContainer"] { background-color: #000000 !important; }
    [data-testid="stSidebar"] { background-color: #1a1a1a !important; }
    .stButton > button { background: linear-gradient(135deg, #0ea5e9, #0284c7) !important; color: white !important; border: none !important; border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)

# Header with Let's Start button
st.markdown("---")
col1, col2, col3 = st.columns([1, 8, 1])
with col1:
    if st.button("📋 Let's Start", use_container_width=True, key="lets_start"):
        st.session_state.show_nav = not st.session_state.get('show_nav', False)

st.markdown("---")

# Show navigation based on button state
if st.session_state.get('show_nav', False):
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        st.markdown("---")
        page = st.radio("Select Tool:", ["🎯 Ad Copy Simulator", "🔍 SEO Analyzer", "⚠️ Mismatch Detector", "📊 GA4 Analyzer"], key="nav_radio")
        st.markdown("---")
        st.markdown('<div style="color:#94a3b8; font-size:0.75rem;">Powered by Groq LLaMA 3.3</div>', unsafe_allow_html=True)
else:
    # Default page when sidebar is collapsed
    page = st.session_state.get('current_page', "🎯 Ad Copy Simulator")
    with st.sidebar:
        page = st.radio("Select Tool:", ["🎯 Ad Copy Simulator", "🔍 SEO Analyzer", "⚠️ Mismatch Detector", "📊 GA4 Analyzer"], key="nav_radio")
        st.session_state.current_page = page
        st.markdown("---")
        st.markdown('<div style="color:#94a3b8; font-size:0.75rem;">Powered by Groq LLaMA 3.3</div>', unsafe_allow_html=True)

# PAGE 1 — AD COPY SIMULATOR
if page == "🎯 Ad Copy Simulator":
    st.title("🎯 Ad Copy Simulator")
    st.write("Generate 5 AI-powered Google Ad variations and find your winner instantly")
    
    with st.sidebar:
        st.markdown("### ✍️ Your Product Details")
        st.markdown("---")
        product  = st.text_input("Product / Service", placeholder="e.g. Online Yoga Classes")
        audience = st.text_input("Target Audience", placeholder="e.g. Working women aged 25-40")
        benefit  = st.text_input("Key Benefit", placeholder="e.g. Lose weight in 30 days")
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
                is_winner = score == best_score
                with col:
                    st.markdown(f"""
                    <div style="background:#1a1a1a; border:2px solid {'#0ea5e9' if is_winner else '#333333'}; border-radius:12px; padding:1rem; margin-bottom:1rem;">
                        <div style="color:#a0aec0; font-size:0.7rem; font-weight:700; margin-bottom:4px;">{'🏆 WINNER · ' if is_winner else ''}VARIATION {i+1}</div>
                        <div style="font-size:1rem; font-weight:800; color:#e0f2fe; margin:0.5rem 0;">{headline}</div>
                        <div style="color:#cbd5e1; font-size:0.85rem; margin-bottom:0.5rem;">{description}</div>
                        <div style="color:#38bdf8; font-weight:700; font-size:0.9rem;">⚡ {score}/100</div>
                        <div style="color:#94a3b8; font-size:0.75rem; font-style:italic; margin-top:0.5rem;">💡 {why}</div>
                    </div>
                    """, unsafe_allow_html=True)

            winner = scores_data[[s["Score"] for s in scores_data].index(best_score)]
            st.success(f"🏆 Winner: {winner['Variation']} (Scored {winner['Score']}/100)")

            st.markdown("### 📊 Score Comparison")
            df = pd.DataFrame(scores_data).set_index("Variation")
            st.bar_chart(df, color="#0ea5e9")

            st.markdown("### 📥 Export Results")
            csv = pd.DataFrame(scores_data).to_csv(index=False)
            st.download_button("⬇️ Download as CSV", csv, "ad_results.csv", "text/csv")

# PAGE 2 — SEO ANALYZER
elif page == "🔍 SEO Analyzer":
    st.title("🔍 SEO Analyzer")
    st.write("Get real Google PageSpeed scores + AI-powered SEO recommendations")
    
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

            if not speed_data.get("error"):
                st.markdown("### 📊 Real Google Scores")
                c1, c2, c3, c4 = st.columns(4)
                for col, label, val in [
                    (c1, "⚡ Performance", speed_data["performance"]),
                    (c2, "🔍 SEO", speed_data["seo"]),
                    (c3, "♿ Accessibility", speed_data["accessibility"]),
                    (c4, "✅ Best Practices", speed_data["best_practices"])
                ]:
                    color = "#86efac" if val >= 70 else "#fcd34d" if val >= 40 else "#fca5a5"
                    col.metric(label, val, delta=None)

            st.markdown("### 📝 AI Analysis")
            st.write(raw)

# PAGE 3 — MISMATCH DETECTOR
elif page == "⚠️ Mismatch Detector":
    st.title("⚠️ Mismatch Detector")
    st.write("Find why your Google Ads Quality Score is low")
    
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
            
            st.markdown(raw)

# PAGE 4 — GA4 ANALYZER
elif page == "📊 GA4 Analyzer":
    st.title("📊 GA4 Drop-Off Analyzer")
    st.write("Real data from your Google Analytics — find where customers leave")
    
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

                    for page_data in pages_sorted[:5]:
                        bounce = page_data["bounce_rate"]
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Page", page_data["page"])
                        col2.metric("Bounce Rate", f"{bounce}%")
                        col3.metric("Sessions", page_data["sessions"])

            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Make sure credentials.json exists and GA4 API is enabled.")