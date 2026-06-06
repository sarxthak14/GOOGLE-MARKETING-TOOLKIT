import os
import requests
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_ads(product, audience, benefit, tone):
    prompt = ("You are a Google Ads expert. Generate exactly 5 Google Ad copy variations.\nProduct: " + product + "\nTarget Audience: " + audience + "\nKey Benefit: " + benefit + "\nTone: " + tone + "\n\nFor each return EXACTLY:\n\nVARIATION 1:\nTrigger: Urgency\nHeadline: (max 30 chars)\nDescription: (max 90 chars)\nWhy this works: (one sentence)\n\nVARIATION 2:\nTrigger: Social Proof\nHeadline: (max 30 chars)\nDescription: (max 90 chars)\nWhy this works: (one sentence)\n\nVARIATION 3:\nTrigger: FOMO\nHeadline: (max 30 chars)\nDescription: (max 90 chars)\nWhy this works: (one sentence)\n\nVARIATION 4:\nTrigger: Value/Saving\nHeadline: (max 30 chars)\nDescription: (max 90 chars)\nWhy this works: (one sentence)\n\nVARIATION 5:\nTrigger: Problem-Solution\nHeadline: (max 30 chars)\nDescription: (max 90 chars)\nWhy this works: (one sentence)")
    r = client.chat.completions.create(model="llama-3.3-70b-versatile", max_tokens=1000, messages=[{"role":"user","content":prompt}])
    return r.choices[0].message.content

def analyze_url(url, content):
    prompt = ("You are an SEO expert.\nURL: " + url + "\nContent: " + content + "\n\nReturn EXACTLY:\nCTR SCORE: (0-100)\n\nCURRENT ISSUES:\nIssue 1: (issue)\nIssue 2: (issue)\nIssue 3: (issue)\n\nTITLE TAG:\nCurrent: (title)\nSuggested: (better title max 60 chars)\nWhy: (reason)\n\nMETA DESCRIPTION:\nCurrent: (meta)\nSuggested: (better meta max 160 chars)\nWhy: (reason)\n\nSEARCH INTENT:\nType: (Informational/Transactional/Navigational/Commercial)\nExplanation: (reason)\n\nQUICK WINS:\nWin 1: (win)\nWin 2: (win)\nWin 3: (win)")
    r = client.chat.completions.create(model="llama-3.3-70b-versatile", max_tokens=1000, messages=[{"role":"user","content":prompt}])
    return r.choices[0].message.content

def get_pagespeed_data(url):
    api_key = os.getenv("PAGESPEED_API_KEY")
    params = {"url": url, "key": api_key, "strategy": "mobile", "category": ["performance","seo","accessibility","best-practices"]}
    try:
        data = requests.get("https://www.googleapis.com/pagespeedonline/v5/runPagespeed", params=params).json()
        cats = data["lighthouseResult"]["categories"]
        aud = data["lighthouseResult"]["audits"]
        opps = [a["title"] for a in aud.values() if a.get("score") is not None and a["score"] < 0.9 and "title" in a]
        return {"performance":round(cats["performance"]["score"]*100),"seo":round(cats["seo"]["score"]*100),"accessibility":round(cats["accessibility"]["score"]*100),"best_practices":round(cats["best-practices"]["score"]*100),"fcp":aud["first-contentful-paint"]["displayValue"],"lcp":aud["largest-contentful-paint"]["displayValue"],"cls":aud["cumulative-layout-shift"]["displayValue"],"opportunities":opps[:5],"error":None}
    except Exception as e:
        return {"error": str(e)}

def analyze_mismatch(ad_headline, ad_description, landing_page_url):
    try:
        from html.parser import HTMLParser
        class T(HTMLParser):
            def __init__(self):
                super().__init__()
                self.text=[]
                self.skip=False
            def handle_starttag(self,tag,attrs):
                if tag in {"script","style","nav","footer"}: self.skip=True
            def handle_endtag(self,tag):
                if tag in {"script","style","nav","footer"}: self.skip=False
            def handle_data(self,data):
                if not self.skip and data.strip(): self.text.append(data.strip())
        p=T()
        p.feed(requests.get(landing_page_url,timeout=10).text)
        page_text=" ".join(p.text)[:3000]
    except Exception as e:
        page_text="Could not fetch page: "+str(e)
    prompt = ("You are a Google Ads Quality Score expert.\nAD HEADLINE: " + ad_headline + "\nAD DESCRIPTION: " + ad_description + "\nLANDING PAGE CONTENT: " + page_text + "\n\nReturn EXACTLY:\nMATCH SCORE: (0-100)\n\nVERDICT: (Excellent Match/Good Match/Partial Match/Poor Match/Critical Mismatch)\n\nWHAT AD PROMISES:\nPromise 1: (promise)\nPromise 2: (promise)\nPromise 3: (promise)\n\nWHAT PAGE DELIVERS:\nDelivers 1: (delivers)\nDelivers 2: (delivers)\nDelivers 3: (delivers)\n\nMISMATCHES FOUND:\nMismatch 1: (mismatch)\nMismatch 2: (mismatch)\nMismatch 3: (mismatch)\n\nQUALITY SCORE IMPACT:\nExpected Quality Score: (1-10)\nCPC Impact: (e.g. +20% higher CPC)\nReason: (one sentence)\n\nFIX SUGGESTIONS:\nFix 1: (fix)\nFix 2: (fix)\nFix 3: (fix)")
    r = client.chat.completions.create(model="llama-3.3-70b-versatile", max_tokens=1500, messages=[{"role":"user","content":prompt}])
    return r.choices[0].message.content


def get_ga4_data(property_id, credentials_path):
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    import pickle, os as os2
    SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]
    creds = None
    if os2.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    client = BetaAnalyticsDataClient(credentials=creds)
    from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Dimension, Metric
    request = RunReportRequest(property=f"properties/{property_id}", dimensions=[Dimension(name="pagePath")], metrics=[Metric(name="sessions"), Metric(name="bounceRate"), Metric(name="averageSessionDuration"), Metric(name="screenPageViews")], date_ranges=[DateRange(start_date="30daysAgo", end_date="today")], limit=10)
    response = client.run_report(request)
    pages = []
    for row in response.rows:
        pages.append({"page": row.dimension_values[0].value, "sessions": int(row.metric_values[0].value), "bounce_rate": round(float(row.metric_values[1].value)*100, 1), "avg_duration": round(float(row.metric_values[2].value), 0), "pageviews": int(row.metric_values[3].value)})
    return pages


def get_ga4_data(property_id, credentials_path):
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    import pickle, os as os2
    SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]
    creds = None
    if os2.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    client = BetaAnalyticsDataClient(credentials=creds)
    from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Dimension, Metric
    request = RunReportRequest(property=f"properties/{property_id}", dimensions=[Dimension(name="pagePath")], metrics=[Metric(name="sessions"), Metric(name="bounceRate"), Metric(name="averageSessionDuration"), Metric(name="screenPageViews")], date_ranges=[DateRange(start_date="30daysAgo", end_date="today")], limit=10)
    response = client.run_report(request)
    pages = []
    for row in response.rows:
        pages.append({"page": row.dimension_values[0].value, "sessions": int(row.metric_values[0].value), "bounce_rate": round(float(row.metric_values[1].value)*100, 1), "avg_duration": round(float(row.metric_values[2].value), 0), "pageviews": int(row.metric_values[3].value)})
    return pages
