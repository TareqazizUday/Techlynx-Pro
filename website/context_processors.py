"""Template context for SEO: stable HTTPS origin in production."""

from django.conf import settings


def site_seo(request):
    """
    SITE_ORIGIN / SITE_SCHEME — use for canonical, Open Graph, Twitter Card, JSON-LD.
    Production always https so Google gets consistent URLs even if a proxy mis-reports scheme.
    """
    host = request.get_host()
    if not settings.DEBUG:
        scheme = 'https'
    else:
        scheme = 'https' if request.is_secure() else request.scheme
    origin = f'{scheme}://{host}'
    return {
        'SITE_SCHEME': scheme,
        'SITE_ORIGIN': origin,
    }
