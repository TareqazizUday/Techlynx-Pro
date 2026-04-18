"""
HTTP security headers. Complements django.middleware.security.SecurityMiddleware.

Note: Browser DevTools can always view public HTML/CSS/JS — that is expected.
These headers reduce XSS, injection, and misuse; secrets must stay server-side only.
"""

from urllib.parse import unquote

from django.conf import settings
from django.http import HttpResponseBadRequest


class RejectSuspiciousPathMiddleware:
    """Block encoded/decoded path traversal before static/media views run."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        raw = unquote(request.path)
        if '..' in raw or request.path.startswith('//'):
            return HttpResponseBadRequest('Bad request')
        return self.get_response(request)


class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.get("Content-Security-Policy"):
            return response

        # Align with current templates: inline handlers/styles, Google Fonts, GA4 (gtag), same-origin API.
        parts = [
            "default-src 'self'",
            "base-uri 'self'",
            "form-action 'self'",
            "frame-ancestors 'none'",
            "object-src 'none'",
            "img-src 'self' data: https: blob:",
            "font-src 'self' data: https://fonts.gstatic.com",
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
            "script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://www.google-analytics.com",
            "connect-src 'self' https://www.googletagmanager.com https://www.google-analytics.com "
            "https://analytics.google.com https://stats.g.doubleclick.net",
        ]
        if not settings.DEBUG:
            parts.append("upgrade-insecure-requests")

        response["Content-Security-Policy"] = "; ".join(parts)

        # Restrict powerful browser features we do not use.
        response.setdefault(
            "Permissions-Policy",
            "accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), "
            "microphone=(), payment=(), usb=(), interest-cohort=()",
        )

        return response
