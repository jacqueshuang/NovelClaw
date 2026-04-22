from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
for dotenv_path in (BASE_DIR / ".env", BASE_DIR.parent / ".env"):
    if dotenv_path.exists():
        load_dotenv(dotenv_path, override=False)


def env_or_default(name: str, default: str, *fallback_names: str) -> str:
    for key in (name, *fallback_names):
        val = os.getenv(key)
        if val is None:
            continue
        val = val.strip()
        if val:
            return val
    return default


def env_flag(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _resolve_database_url() -> str:
    raw = env_or_default(
        "APP_DATABASE_URL",
        f"sqlite:///{(DATA_DIR / 'app.db').as_posix()}",
        "DATABASE_URL",
    )
    if not raw.startswith("sqlite:///"):
        return raw
    db_path = raw[len("sqlite:///"):].strip()
    if not db_path or db_path == ":memory:":
        return raw
    candidate = Path(db_path).expanduser()
    if not candidate.is_absolute():
        candidate = (BASE_DIR.parent / candidate).resolve()
    candidate.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{candidate.as_posix()}"


@dataclass(frozen=True)
class Settings:
    app_name: str = "NovelClaw Portal"
    database_url: str = _resolve_database_url()
    https_only: bool = env_flag("APP_HTTPS_ONLY", False)
    session_cookie_name: str = env_or_default("APP_SESSION_COOKIE_NAME", "session")
    session_cookie_domain: str = os.getenv("APP_SESSION_COOKIE_DOMAIN", "").strip()
    app_base_url: str = os.getenv("APP_BASE_URL", "").strip().rstrip("/")
    app_multiagent_url: str = os.getenv("APP_MULTIAGENT_URL", "").strip()
    app_claw_url: str = os.getenv("APP_CLAW_URL", "").strip()
    ui_language: str = os.getenv("WEB_UI_LANGUAGE", "en").lower()
    preview_user_email: str = env_or_default("APP_PREVIEW_USER_EMAIL", "preview@novelclaw.local").lower()
    session_secret_env: str = env_or_default("APP_SESSION_SECRET", "", "SECRET_KEY")


settings = Settings()
