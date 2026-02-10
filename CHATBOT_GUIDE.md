# Techlynx Chatbot - Quick Setup Guide

## Overview

The Techlynx AI Assistant is a Gemini-powered chatbot that can answer questions about your company's services, pricing, and general information by reading all content from your website.

## Architecture

- **Frontend**: Vanilla JavaScript with Tailwind CSS
- **Backend**: Django REST endpoint at `/api/chat/`
- **AI Model**: Google Gemini 2.5 Flash
- **Context**: ~100K tokens from 16 website pages
- **Storage**: Session-based (chat history cleared on browser close)

## Setup Instructions

### 1. Get Gemini API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key" 
4. Copy the generated key

### 2. Configure Environment

Open `.env` file in project root and add:

```env
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. Install Dependencies (Already Done)

```bash
pip install google-generativeai beautifulsoup4
```

### 4. Test the Chatbot

1. Run development server: `python manage.py runserver`
2. Open browser: http://localhost:8000
3. Click chatbot icon (bottom-right corner)
4. Ask: "What services do you offer?"
5. Verify you get an AI response

## Features

### User Features
- ✅ Chat bubble widget (bottom-right floating button)
- ✅ Expandable chat window (400x600px desktop, fullscreen mobile)
- ✅ Session-based conversation history
- ✅ Typing indicator animation
- ✅ Dark mode compatible
- ✅ Mobile responsive
- ✅ Keyboard shortcuts (Enter to send, Escape to close)

### Technical Features
- ✅ Rate limiting: 10 queries/hour per session
- ✅ Input validation: 500 character max
- ✅ CSRF protection
- ✅ Error handling and user-friendly messages
- ✅ Context caching (refreshes on server restart)
- ✅ Automatic HTML stripping from templates
- ✅ Markdown formatting in responses

## File Structure

```
website/
├── chatbot_context.py      # Context extraction system
├── views.py                 # chatbot_query() endpoint
└── urls.py                  # /api/chat/ route

templates/
└── base.html                # Chat UI widget

static/js/
└── custom.js                # TechlynxChatbot class

.env                          # GEMINI_API_KEY configuration
```

## How It Works

### Context Extraction

1. **On First Request**: `get_chatbot_context()` in `chatbot_context.py`
2. **Reads Templates**: All 16 HTML files in `templates/website/`
3. **Strips HTML**: Uses BeautifulSoup4 to extract readable text
4. **Organizes Content**: Sections for Services, About, Contact, etc.
5. **Caches Result**: Stored in global variable `_cached_context`
6. **Refresh**: Automatic on server restart

### Request Flow

```
User Input → JavaScript (custom.js)
    ↓
AJAX POST /api/chat/ with CSRF token
    ↓
Django View (chatbot_query)
    ↓
Rate Limit Check (10/hour session)
    ↓
Get Cached Context (chatbot_context.py)
    ↓
Build System Prompt + User Question
    ↓
Call Gemini API (gemini-2.5-flash)
    ↓
Return JSON Response
    ↓
Display in Chat UI
```

## Customization

### Change AI Model

In `views.py`, line with `GenerativeModel`:

```python
# Current (fast, stable)
model = genai.GenerativeModel('gemini-2.5-flash')

# Alternative (higher quality, slower)
model = genai.GenerativeModel('gemini-2.5-pro')

# Always latest Flash model
model = genai.GenerativeModel('gemini-flash-latest')
```

### Adjust Rate Limits

In `views.py`, `chatbot_query()` function:

```python
# Current: 10 queries per hour
if len(request.session['chatbot_queries']) >= 10:

# Change to 20 queries per hour
if len(request.session['chatbot_queries']) >= 20:
```

### Modify System Prompt

In `views.py`, `system_prompt` variable - adjust instructions:

```python
system_prompt = f"""You are a helpful AI assistant for Techlynx Pro...
[Edit this to change bot personality and behavior]
"""
```

### Update Context Coverage

In `chatbot_context.py`, `extract_site_context()`:

```python
# Adjust character limits per section
context_parts.append(content[:1500])  # Change 1500 to desired length
```

## Testing Scenarios

### Test Queries

1. **Services**: "What services do you offer?"
2. **Pricing**: "How much does web development cost?"
3. **AI Specific**: "Tell me about your AI solutions"
4. **Contact**: "How can I contact you?"
5. **Industries**: "What industries do you work with?"
6. **Out of Scope**: "Who is your CEO?" (should say "I don't have that info")

### Expected Responses

- Should mention specific services from service pages
- Should reference budget ranges ($5K-$10K, etc.)
- Should encourage contacting for quotes
- Should NOT discuss competitors
- Should admit when information isn't available

## Troubleshooting

### "Chatbot is temporarily unavailable"
- **Cause**: Missing or invalid `GEMINI_API_KEY`
- **Fix**: Check `.env` file, ensure key is correct

### "Rate limit exceeded"
- **Cause**: More than 10 queries in 1 hour
- **Fix**: Wait 1 hour or clear Django session cookies

### "Network error"
- **Cause**: Backend API not responding
- **Fix**: Check Django server is running, check browser console

### Slow Responses (>5 seconds)
- **Cause**: Large context or slow Gemini API
- **Fix**: Consider switching to RAG approach or reducing context size

### Context Not Updated
- **Cause**: Cached context not refreshed after template changes
- **Fix**: Restart Django server to regenerate context

## Production Deployment

### Environment Variables

Set these in your hosting platform (Heroku, AWS, etc.):

```bash
GEMINI_API_KEY=your_production_api_key
DEBUG=False
SECRET_KEY=secure_random_key_here
```

### Security Checklist

- ✅ GEMINI_API_KEY in environment variables (not hardcoded)
- ✅ DEBUG=False in production
- ✅ CSRF protection enabled
- ✅ Rate limiting active
- ✅ Input validation (500 char limit)
- ✅ HTTPS enabled on domain

### Cost Monitoring

**Gemini API Usage:**
- Track at: https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas
- Set budget alerts in Google Cloud Console
- Monitor daily query counts

**Cost Formula:**
```
Daily Cost = (queries_per_day × 100K_tokens_per_query) / 1M × $0.075
Example: 1000 queries/day = ~$7.50/month
```

## Upgrade to RAG (If Needed)

If you get >3000 queries/day or content grows >200K tokens, consider upgrading to RAG (Retrieval-Augmented Generation):

1. Add vector database (ChromaDB or FAISS)
2. Generate embeddings for content chunks
3. Retrieve only relevant chunks per query
4. Reduces cost and improves speed

**When to Upgrade:**
- Monthly costs exceed $50
- Response times consistently >4 seconds
- Content grows beyond 16 pages
- Need to add PDFs, documentation, or dynamic content

## Support

For issues or questions:
- Check Django logs: Terminal where `runserver` is running
- Check browser console: F12 Developer Tools
- Test API directly: Use Postman to POST to `/api/chat/`
- Gemini API status: https://status.cloud.google.com/

## Future Enhancements

**Possible Additions:**
- [ ] Analytics dashboard (query tracking, popular questions)
- [ ] Admin panel to view chat logs
- [ ] Sentiment analysis on user queries
- [ ] Suggested questions/quick replies
- [ ] File upload support (send documents to analyze)
- [ ] Multi-language support (detect language, respond accordingly)
- [ ] Integration with CRM (save leads from chat)
- [ ] Chatbot personality customization

---

**Version**: 1.0  
**Last Updated**: February 2026  
**AI Model**: Google Gemini 2.5 Flash
