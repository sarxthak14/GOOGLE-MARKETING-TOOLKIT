import streamlit as st
from groq import Groq

# Get API key from Streamlit Secrets
api_key = st.secrets.get("GROQ_API_KEY")

if not api_key:
    st.error("❌ GROQ_API_KEY not found in Streamlit Secrets!")
    st.stop()

client = Groq(api_key=api_key)

def generate_ads(product, audience, benefit, tone):
    prompt = f"""
    You are a Google Ads expert. Generate exactly 5 Google Ad copy variations for:
    
    Product: {product}
    Target Audience: {audience}
    Key Benefit: {benefit}
    Tone: {tone}
    
    Each variation must use a DIFFERENT psychological trigger:
    1. Urgency (e.g. "Limited time offer")
    2. Social Proof (e.g. "Trusted by 10,000+ users")
    3. FOMO (e.g. "Don't miss out")
    4. Value/Saving (e.g. "Save 40% today")
    5. Problem-Solution (e.g. "Tired of X? Try Y")
    
    For each variation, return EXACTLY in this format:
    
    VARIATION 1:
    Trigger: Urgency
    Headline: (max 30 characters)
    Description: (max 90 characters)
    Why this works: (one sentence explanation)
    
    VARIATION 2:
    Trigger: Social Proof
    Headline: (max 30 characters)
    Description: (max 90 characters)
    Why this works: (one sentence explanation)
    
    Continue for all 5 variations.
    """
    
    message = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return message.content[0].text

def analyze_url(url, content):
    prompt = f"""
    You are an SEO expert. Analyze this webpage and provide 5 specific recommendations to improve its SEO:
    
    URL: {url}
    Content: {content}
    
    For each recommendation, explain:
    1. What's the issue?
    2. Why does it matter for SEO?
    3. How to fix it?
    
    Keep it concise and actionable.
    """
    
    message = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return message.content[0].text

def get_pagespeed_data(url):
    try:
        import requests
        api_key = st.secrets.get("PAGESPEED_API_KEY")
        
        if not api_key:
            return {"error": "PageSpeed API key not found"}
        
        endpoint = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={api_key}"
        response = requests.get(endpoint)
        data = response.json()
        
        scores = data.get("lighthouseResult", {}).get("categories", {})
        
        return {
            "performance": scores.get("performance", {}).get("score", 0) * 100,
            "seo": scores.get("seo", {}).get("score", 0) * 100,
            "accessibility": scores.get("accessibility", {}).get("score", 0) * 100,
            "best_practices": scores.get("best-practices", {}).get("score", 0) * 100
        }
    except Exception as e:
        return {"error": str(e)}

def analyze_mismatch(ad_headline, ad_description, landing_url):
    prompt = f"""
    You are a Google Ads Quality Score expert. Analyze this ad and landing page for mismatches that could lower Quality Score:
    
    Ad Headline: {ad_headline}
    Ad Description: {ad_description}
    Landing URL: {landing_url}
    
    Identify:
    1. Keyword relevance issues
    2. Ad-to-landing page mismatches
    3. Expected user experience problems
    4. Quality Score risks
    
    Provide specific recommendations to improve Quality Score.
    """
    
    message = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return message.content[0].text

def get_ga4_data(property_id, credentials_file):
    try:
        from google.analytics.data_v1beta import BetaAnalyticsDataClient
        from google.analytics.data_v1beta.types import RunReportRequest
        
        client = BetaAnalyticsDataClient()
        
        request = RunReportRequest(
            property=f"properties/{property_id}",
            data_ranges=[{"start_date": "30daysAgo", "end_date": "today"}],
            dimensions=[{"name": "pagePath"}],
            metrics=[{"name": "bounceRate"}, {"name": "sessions"}],
        )
        
        response = client.run_report(request)
        
        pages = []
        for row in response.rows:
            pages.append({
                "page": row.dimension_values[0].value,
                "bounce_rate": float(row.metric_values[0].value),
                "sessions": int(row.metric_values[1].value)
            })
        
        return pages
    except Exception as e:
        return None