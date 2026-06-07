# 🎯 Google Marketing Toolkit

A powerful, AI-powered Streamlit application designed to streamline digital marketing workflows. Leverage Groq's LLaMA 3.3 language model and Google's PageSpeed Insights API to generate marketing copy, analyze web performance, and optimize your digital campaigns—all in one unified interface.

---

## ✨ Features

### 1. **Content Generator**
Generate high-converting marketing copy powered by Groq LLaMA 3.3:
- Product descriptions optimized for e-commerce
- Social media captions and hashtag strategies
- Email marketing subject lines and body copy
- Ad copy for various platforms (Google Ads, Facebook, LinkedIn)
- Blog post outlines and article frameworks

### 2. **Performance Analyzer**
Integrate Google PageSpeed Insights API to:
- Analyze website performance metrics (desktop & mobile)
- Generate actionable optimization recommendations
- Identify Core Web Vitals issues
- Access detailed performance reports with scores

### 3. **SEO Optimizer**
AI-driven SEO enhancement tools:
- Meta tag generation (title, description, keywords)
- Keyword research insights
- Content optimization recommendations
- Schema markup suggestions

### 4. **Campaign Dashboard**
Track and manage marketing campaigns:
- Campaign performance metrics
- ROI calculations
- A/B testing frameworks
- Competitor analysis tools

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- pip (Python package manager)
- Groq API key ([Get one here](https://console.groq.com))
- Google PageSpeed Insights API key ([Get one here](https://developers.google.com/speed/pagespeed/insights))

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/google-marketing-toolkit.git
   cd google-marketing-toolkit
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   PAGESPEED_API_KEY=your_google_pagespeed_api_key_here
   ```

### Running the Application

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`.

---

## 📋 Project Structure

```
google-marketing-toolkit/
├── app.py                      # Main Streamlit application
├── config/
│   ├── settings.py            # Configuration settings
│   └── api_keys.py            # API key management
├── tools/
│   ├── content_generator.py   # Content generation logic
│   ├── performance_analyzer.py # PageSpeed Insights integration
│   ├── seo_optimizer.py       # SEO optimization tools
│   └── campaign_dashboard.py  # Campaign tracking
├── utils/
│   ├── groq_client.py         # Groq API wrapper
│   ├── pagespeed_client.py    # Google PageSpeed API wrapper
│   └── helpers.py             # Utility functions
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variable template
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

---

## 🔧 Configuration

### API Key Setup

**Option 1: Environment Variables (Recommended)**
```bash
export GROQ_API_KEY="your_key_here"
export PAGESPEED_API_KEY="your_key_here"
```

**Option 2: Streamlit Secrets**
Create `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "your_key_here"
PAGESPEED_API_KEY = "your_key_here"
```

---

## 💡 Usage Examples

### Content Generation
```python
from tools.content_generator import ContentGenerator

gen = ContentGenerator()
copy = gen.generate_product_description(
    product_name="Premium Coffee Maker",
    features=["Programmable", "Thermal Carafe", "Built-in Grinder"],
    target_audience="Home Baristas"
)
print(copy)
```

### Performance Analysis
```python
from tools.performance_analyzer import PerformanceAnalyzer

analyzer = PerformanceAnalyzer()
metrics = analyzer.analyze_url("https://example.com")
print(f"Mobile Score: {metrics['mobile_score']}")
print(f"Desktop Score: {metrics['desktop_score']}")
```

---

## 🌐 Deployment

### Deploy to Streamlit Cloud

1. Push your repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with your GitHub account
4. Click "New app" and select your repository
5. Configure deployment settings and add secrets:
   - `GROQ_API_KEY`
   - `PAGESPEED_API_KEY`

### Deploy to Heroku

```bash
# Create Procfile
echo "web: streamlit run app.py --server.port=\$PORT" > Procfile

# Create runtime.txt (specify Python version)
echo "python-3.9.16" > runtime.txt

# Deploy
git push heroku main
```

### Deploy to Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

```bash
docker build -t marketing-toolkit .
docker run -p 8501:8501 -e GROQ_API_KEY=your_key marketing-toolkit
```

---

## 🔐 Security Best Practices

✅ **Never commit API keys to version control**
- Use `.env` files (excluded via `.gitignore`)
- Use environment variables in production
- Rotate API keys regularly

✅ **Validate user inputs**
- Sanitize text inputs to prevent injection attacks
- Limit API request rates

✅ **Secure deployments**
- Use HTTPS for all API calls
- Implement authentication for shared deployments
- Monitor API usage and costs

---

## 📊 Performance Metrics

| Component | Status | Details |
|-----------|--------|---------|
| Groq LLaMA 3.3 | ✅ Active | Fast inference, low latency |
| PageSpeed API | ✅ Active | Real-time performance analysis |
| Streamlit UI | ✅ Active | Responsive, mobile-friendly |
| Deployment | ✅ Ready | Cloud-compatible |

---

## 🐛 Troubleshooting

### Issue: "API Key Invalid"
- Verify API key is correctly set in `.env` or Streamlit secrets
- Check API key has proper permissions
- Regenerate API key if expired

### Issue: "PageSpeed API Quota Exceeded"
- Check your API quotas at Google Cloud Console
- Implement request caching to reduce calls
- Consider upgrading your Google Cloud plan

### Issue: "Streamlit Connection Timeout"
- Check internet connection
- Verify firewall rules allow API requests
- Increase timeout settings in config

---

## 📚 Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Groq API Docs](https://console.groq.com/docs)
- [Google PageSpeed Insights](https://developers.google.com/speed/pagespeed/insights)
- [Digital Marketing Best Practices](https://moz.com/beginners-guide-to-seo)

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Commit your changes:**
   ```bash
   git commit -m "Add: clear description of your feature"
   ```
4. **Push to your branch:**
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Open a Pull Request** with a clear description

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions
- Write unit tests for new features

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Sarthak**
- GitHub: https://github.com/sarxthak14/GOOGLE-MARKETING-TOOLKIT
- LinkedIn: https://www.linkedin.com/in/sarthakmishra1/
- Email: Sarthakm4u@gmail.com

---

## 🙏 Acknowledgments

- **Groq** for the powerful LLaMA 3.3 model
- **Google** for PageSpeed Insights API
- **Streamlit** for the excellent web framework
- The open-source community for invaluable tools and support

---

## 📝 Changelog

### v1.0.0 (Current)
- ✅ Content Generator tool
- ✅ Performance Analyzer integration
- ✅ SEO Optimizer functionality
- ✅ Campaign Dashboard
- ✅ Streamlit Cloud deployment

### Upcoming (v1.1.0)
- 🔄 Advanced analytics dashboard
- 🔄 Multi-language support
- 🔄 Export reports (PDF, CSV)
- 🔄 Team collaboration features

---

**⭐ If this toolkit helped you, please consider starring the repository!**

---

*Last updated: June 2026*
