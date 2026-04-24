from __future__ import annotations

from fastapi import Request
from starlette.responses import Response

from .settings import settings


UI_LOCALE_COOKIE = "colong_ui_locale"
SUPPORTED_UI_LOCALES = ("zh", "en")
_SESSION_KEY = "ui_language"


def _canonicalize_ui_locale(value: str | None) -> str | None:
    raw = (value or "").strip().lower().replace("_", "-")
    if raw == "en" or raw.startswith("en-"):
        return "en"
    if raw == "zh" or raw.startswith("zh-"):
        return "zh"
    return None


def normalize_ui_locale(value: str | None) -> str:
    normalized = _canonicalize_ui_locale(value)
    if normalized:
        return normalized
    configured = _canonicalize_ui_locale(settings.ui_language)
    if configured:
        return configured
    return "zh"


def resolve_ui_locale(request: Request | None) -> str:
    if request is None:
        return normalize_ui_locale(None)
    cookie_locale = request.cookies.get(UI_LOCALE_COOKIE)
    if cookie_locale:
        return normalize_ui_locale(cookie_locale)
    session_locale = request.session.get(_SESSION_KEY)
    if session_locale:
        return normalize_ui_locale(str(session_locale))
    return normalize_ui_locale(None)


def apply_ui_locale(request: Request, response: Response, value: str | None) -> str:
    locale = normalize_ui_locale(value)
    request.session[_SESSION_KEY] = locale
    response.set_cookie(
        UI_LOCALE_COOKIE,
        locale,
        path="/",
        samesite="lax",
        secure=settings.https_only,
        domain=settings.shared_cookie_domain or None,
    )
    return locale
