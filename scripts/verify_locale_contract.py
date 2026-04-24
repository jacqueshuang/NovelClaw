from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]

AUTH_FOUNDATION_CODE = "\n".join(
    (
        "from local_web_portal.app.settings import settings",
        "from local_web_portal.app.locale import UI_LOCALE_COOKIE, normalize_ui_locale",
        'assert settings.ui_language == "zh", settings.ui_language',
        'assert UI_LOCALE_COOKIE == "colong_ui_locale", UI_LOCALE_COOKIE',
        'assert normalize_ui_locale(None) == "zh"',
        'assert normalize_ui_locale("en-US") == "en"',
        'assert normalize_ui_locale("zh-CN") == "zh"',
        'assert normalize_ui_locale("bogus") == "zh"',
    )
)

AUTH_ROUTE_CODE = "\n".join(
    (
        "import os, sys, types",
        'os.environ.setdefault("APP_SESSION_SECRET", "verify-locale-contract-secret")',
        "itsdangerous = types.ModuleType('itsdangerous')",
        "exc = types.ModuleType('itsdangerous.exc')",
        "exc.BadSignature = Exception",
        "itsdangerous.BadSignature = exc.BadSignature",
        "itsdangerous.exc = exc",
        "class TimestampSigner:",
        "    def __init__(self, *args, **kwargs):",
        "        pass",
        "itsdangerous.TimestampSigner = TimestampSigner",
        "sys.modules.setdefault('itsdangerous', itsdangerous)",
        "sys.modules.setdefault('itsdangerous.exc', exc)",
        "jinja2 = types.ModuleType('jinja2')",
        "jinja2.pass_context = lambda fn: fn",
        "class FileSystemLoader:",
        "    def __init__(self, *args, **kwargs):",
        "        pass",
        "class Environment:",
        "    def __init__(self, *args, **kwargs):",
        "        self.globals = {}",
        "jinja2.FileSystemLoader = FileSystemLoader",
        "jinja2.Environment = Environment",
        "sys.modules.setdefault('jinja2', jinja2)",
        "from starlette.requests import Request",
        "from local_web_portal.app.main import _ui_language, set_ui_language",
        "async def receive():",
        "    return {'type': 'http.request', 'body': b'', 'more_body': False}",
        "def make_request(*, cookies=None, session=None, path='/ui-language'):",
        "    headers = []",
        "    if cookies:",
        "        cookie_header = '; '.join(f'{key}={value}' for key, value in cookies.items()).encode()",
        "        headers.append((b'cookie', cookie_header))",
        "    scope = {'type': 'http', 'http_version': '1.1', 'method': 'POST', 'path': path, 'headers': headers, 'query_string': b'', 'scheme': 'http', 'client': ('testclient', 50000), 'server': ('testserver', 80), 'session': session or {}}",
        "    return Request(scope, receive)",
        "blank_request = make_request(session={})",
        'assert _ui_language(blank_request) == "zh"',
        'broken_session_request = make_request(session={"ui_language": "bogus"})',
        'assert _ui_language(broken_session_request) == "zh"',
        'request = make_request(session={})',
        'response = set_ui_language(request, lang="en", next="/select-mode?tab=hub")',
        'assert request.session["ui_language"] == "en", request.session',
        'assert response.headers["location"] == "/select-mode?tab=hub", response.headers.get("location")',
        'set_cookie = response.headers.get("set-cookie", "")',
        'assert "colong_ui_locale=en" in set_cookie, set_cookie',
        'assert "SameSite=lax" in set_cookie, set_cookie',
        'print("auth route ok")',
    )
)

AUTH_DEFAULT_CODE = "\n".join(
    (
        "from local_web_portal.app.settings import settings",
        "from local_web_portal.app.locale import normalize_ui_locale",
        'assert settings.ui_language == "zh", settings.ui_language',
        'assert normalize_ui_locale(None) == "zh"',
        'assert normalize_ui_locale("bogus") == "zh"',
    )
)

AUTH_CONFIG_EN_CODE = "\n".join(
    (
        "from local_web_portal.app.locale import normalize_ui_locale",
        'assert normalize_ui_locale(None) == "en"',
        'assert normalize_ui_locale("bogus") == "en"',
    )
)

AUTH_CONFIG_ZH_CODE = "\n".join(
    (
        "from local_web_portal.app.locale import normalize_ui_locale",
        'assert normalize_ui_locale(None) == "zh"',
        'assert normalize_ui_locale("bogus") == "zh"',
    )
)

MULTIAGENT_PRELUDE = "\n".join(
    (
        "import os, sys, types",
        "os.environ.setdefault('APP_SESSION_SECRET', 'verify-locale-contract-secret')",
        "os.environ.setdefault('APP_ENCRYPTION_KEY', 'MDEyMzQ1Njc4OWFiY2RlZjAxMjM0NTY3ODlhYmNkZWY=')",
        "jinja2 = types.ModuleType('jinja2')",
        "jinja2.pass_context = lambda fn: fn",
        "class FileSystemLoader:",
        "    def __init__(self, *args, **kwargs):",
        "        pass",
        "class Environment:",
        "    def __init__(self, *args, **kwargs):",
        "        self.globals = {}",
        "jinja2.FileSystemLoader = FileSystemLoader",
        "jinja2.Environment = Environment",
        "sys.modules.setdefault('jinja2', jinja2)",
        "itsdangerous = types.ModuleType('itsdangerous')",
        "exc = types.ModuleType('itsdangerous.exc')",
        "exc.BadSignature = Exception",
        "itsdangerous.BadSignature = exc.BadSignature",
        "itsdangerous.exc = exc",
        "class TimestampSigner:",
        "    def __init__(self, *args, **kwargs):",
        "        pass",
        "    def sign(self, value):",
        "        return value",
        "    def unsign(self, value, max_age=None):",
        "        return value",
        "itsdangerous.TimestampSigner = TimestampSigner",
        "sys.modules.setdefault('itsdangerous', itsdangerous)",
        "sys.modules.setdefault('itsdangerous.exc', exc)",
    )
)

MULTIAGENT_FOUNDATION_CODE = "\n".join(
    (
        MULTIAGENT_PRELUDE,
        "from local_web_portal.app.i18n import (",
        "    DEFAULT_LOCALE,",
        "    PRODUCT_LOCALE_COOKIE,",
        "    from_internal_locale,",
        "    get_locale,",
        "    get_shared_locale,",
        "    install_i18n,",
        "    locale_options,",
        "    normalize_shared_locale,",
        "    to_internal_locale,",
        ")",
        "class DummyRequest:",
        "    def __init__(self, cookies=None, session=None):",
        "        self.cookies = cookies or {}",
        "        self.session = session or {}",
        "class DummyEnv:",
        "    def __init__(self):",
        "        self.globals = {}",
        "class DummyTemplates:",
        "    def __init__(self):",
        "        self.env = DummyEnv()",
        'assert DEFAULT_LOCALE == "zh-CN", DEFAULT_LOCALE',
        'assert PRODUCT_LOCALE_COOKIE == "colong_ui_locale", PRODUCT_LOCALE_COOKIE',
        'assert normalize_shared_locale(None) == "zh"',
        'assert normalize_shared_locale("en-GB") == "en"',
        'assert to_internal_locale("zh") == "zh-CN"',
        'assert from_internal_locale("zh-CN") == "zh"',
        'assert locale_options() == [{"code": "zh", "label": "中文"}, {"code": "en", "label": "English"}]',
        "request = DummyRequest(cookies={PRODUCT_LOCALE_COOKIE: 'zh'})",
        'assert get_shared_locale(request) == "zh"',
        'assert get_locale(request) == "zh-CN"',
        "templates = DummyTemplates()",
        "install_i18n(templates)",
        "context = {'request': request}",
        'assert templates.env.globals["locale"](context) == "zh-CN"',
        'assert templates.env.globals["shared_locale"](context) == "zh"',
        'assert templates.env.globals["shared_locale"](context) in [item["code"] for item in templates.env.globals["locale_options"]()]',
    )
)

MULTIAGENT_ROUTE_CODE = "\n".join(
    (
        MULTIAGENT_PRELUDE,
        "from starlette.requests import Request",
        "from local_web_portal.app.main import change_language",
        "from local_web_portal.app.i18n import get_locale, get_shared_locale, PRODUCT_LOCALE_COOKIE",
        "async def receive():",
        "    return {'type': 'http.request', 'body': b'', 'more_body': False}",
        "def make_request(*, cookies=None, session=None, path='/language', query=''):",
        "    headers = []",
        "    if cookies:",
        "        cookie_header = '; '.join(f'{key}={value}' for key, value in cookies.items()).encode()",
        "        headers.append((b'cookie', cookie_header))",
        "    scope = {'type': 'http', 'http_version': '1.1', 'method': 'POST', 'path': path, 'headers': headers, 'query_string': query.encode(), 'scheme': 'http', 'client': ('testclient', 50000), 'server': ('testserver', 80), 'session': session or {}}",
        "    return Request(scope, receive)",
        "blank_request = make_request(session={})",
        'assert get_shared_locale(blank_request) == "zh"',
        'assert get_locale(blank_request) == "zh-CN"',
        "request = make_request(session={})",
        'response = change_language(request, locale="zh", next="/jobs?filter=running")',
        'assert request.session["locale"] == "zh-CN", request.session',
        'assert response.headers["location"] == "/jobs?filter=running", response.headers.get("location")',
        'set_cookie = response.headers.get("set-cookie", "")',
        'assert f"{PRODUCT_LOCALE_COOKIE}=zh" in set_cookie, set_cookie',
        'print("multiagent route ok")',
    )
)

MULTIAGENT_DEFAULT_CODE = "\n".join(
    (
        MULTIAGENT_PRELUDE,
        "from local_web_portal.app.i18n import DEFAULT_LOCALE, normalize_shared_locale, to_internal_locale",
        'assert DEFAULT_LOCALE == "zh-CN", DEFAULT_LOCALE',
        'assert normalize_shared_locale(None) == "zh"',
        'assert normalize_shared_locale("bogus") == "zh"',
        'assert to_internal_locale(None) == "zh-CN"',
    )
)

MULTIAGENT_CONFIG_EN_CODE = "\n".join(
    (
        MULTIAGENT_PRELUDE,
        "from local_web_portal.app.i18n import from_internal_locale, normalize_shared_locale, to_internal_locale",
        'assert normalize_shared_locale(None) == "en"',
        'assert normalize_shared_locale("bogus") == "en"',
        'assert to_internal_locale(None) == "en"',
        'assert from_internal_locale("bogus") == "en"',
    )
)

MULTIAGENT_CONFIG_ZH_CODE = "\n".join(
    (
        MULTIAGENT_PRELUDE,
        "from local_web_portal.app.i18n import normalize_shared_locale, to_internal_locale",
        'assert normalize_shared_locale(None) == "zh"',
        'assert normalize_shared_locale("bogus") == "zh"',
        'assert to_internal_locale(None) == "zh-CN"',
    )
)

NOVELCLAW_FOUNDATION_CODE = "\n".join(
    (
        "from local_web_portal.app.settings import settings",
        "from local_web_portal.app.locale import UI_LOCALE_COOKIE, normalize_ui_locale",
        'assert settings.ui_language == "zh", settings.ui_language',
        'assert UI_LOCALE_COOKIE == "colong_ui_locale", UI_LOCALE_COOKIE',
        'assert normalize_ui_locale("") == "zh"',
        'assert normalize_ui_locale("en") == "en"',
        'assert normalize_ui_locale("zh-Hans") == "zh"',
        'assert normalize_ui_locale("bogus") == "zh"',
    )
)

NOVELCLAW_ROUTE_CODE = "\n".join(
    (
        "import os, sys, types",
        'os.environ.setdefault("APP_SESSION_SECRET", "verify-locale-contract-secret")',
        'os.environ.setdefault("APP_ENCRYPTION_KEY", "MDEyMzQ1Njc4OWFiY2RlZjAxMjM0NTY3ODlhYmNkZWY=")',
        'os.environ.setdefault("APP_DATABASE_URL", "sqlite:///:memory:")',
        'os.environ.setdefault("APP_RUNS_DIR", "/tmp")',
        "itsdangerous = types.ModuleType('itsdangerous')",
        "exc = types.ModuleType('itsdangerous.exc')",
        "exc.BadSignature = Exception",
        "itsdangerous.BadSignature = exc.BadSignature",
        "itsdangerous.exc = exc",
        "class TimestampSigner:",
        "    def __init__(self, *args, **kwargs):",
        "        pass",
        "itsdangerous.TimestampSigner = TimestampSigner",
        "sys.modules.setdefault('itsdangerous', itsdangerous)",
        "sys.modules.setdefault('itsdangerous.exc', exc)",
        "jinja2 = types.ModuleType('jinja2')",
        "jinja2.pass_context = lambda fn: fn",
        "class FileSystemLoader:",
        "    def __init__(self, *args, **kwargs):",
        "        pass",
        "class Environment:",
        "    def __init__(self, *args, **kwargs):",
        "        self.globals = {}",
        "jinja2.FileSystemLoader = FileSystemLoader",
        "jinja2.Environment = Environment",
        "sys.modules.setdefault('jinja2', jinja2)",
        "from local_web_portal.app.main import _ui_language, set_ui_language",
        "class DummyRequest:",
        "    def __init__(self, session=None, cookies=None):",
        "        self.session = session or {}",
        "        self.cookies = cookies or {}",
        "request = DummyRequest(session={}, cookies={})",
        'assert _ui_language(request) == "zh"',
        'response = set_ui_language(request, lang="en", next="/console/chat?session_id=7")',
        'assert request.session["ui_language"] == "en", request.session',
        'assert response.headers["location"] == "/console/chat?session_id=7", response.headers.get("location")',
        'set_cookie = response.headers.get("set-cookie", "")',
        'assert "colong_ui_locale=en" in set_cookie, set_cookie',
        'assert "SameSite=lax" in set_cookie, set_cookie',
        'print("novelclaw route ok")',
    )
)

NOVELCLAW_RUNTIME_CODE = "\n".join(
    (
        "import os, sys, types, json",
        'os.environ.setdefault("APP_SESSION_SECRET", "verify-locale-contract-secret")',
        'os.environ.setdefault("APP_ENCRYPTION_KEY", "MDEyMzQ1Njc4OWFiY2RlZjAxMjM0NTY3ODlhYmNkZWY=")',
        'os.environ.setdefault("APP_DATABASE_URL", "sqlite:///:memory:")',
        'os.environ.setdefault("APP_RUNS_DIR", "/tmp")',
        "itsdangerous = types.ModuleType('itsdangerous')",
        "exc = types.ModuleType('itsdangerous.exc')",
        "exc.BadSignature = Exception",
        "itsdangerous.BadSignature = exc.BadSignature",
        "itsdangerous.exc = exc",
        "class TimestampSigner:",
        "    def __init__(self, *args, **kwargs):",
        "        pass",
        "itsdangerous.TimestampSigner = TimestampSigner",
        "sys.modules.setdefault('itsdangerous', itsdangerous)",
        "sys.modules.setdefault('itsdangerous.exc', exc)",
        "jinja2 = types.ModuleType('jinja2')",
        "jinja2.pass_context = lambda fn: fn",
        "class FileSystemLoader:",
        "    def __init__(self, *args, **kwargs):",
        "        pass",
        "class Environment:",
        "    def __init__(self, *args, **kwargs):",
        "        self.globals = {}",
        "jinja2.FileSystemLoader = FileSystemLoader",
        "jinja2.Environment = Environment",
        "sys.modules.setdefault('jinja2', jinja2)",
        "from local_web_portal.app.main import _portal_memory_system",
        "from local_web_portal.app.job_runner import _job_language_profile, _provider_env",
        "from local_web_portal.app.provider_registry import ProviderSpec",
        "_portal_memory_system.cache_clear()",
        'assert _portal_memory_system().config.language == "zh", _portal_memory_system().config.language',
        "class DummyExecuteResult:",
        "    def __init__(self, payload):",
        "        self._payload = payload",
        "    def scalar_one_or_none(self):",
        "        return self._payload",
        "class DummyDb:",
        "    def __init__(self, payload):",
        "        self._payload = payload",
        "    def execute(self, stmt):",
        "        return DummyExecuteResult(self._payload)",
        'assert _job_language_profile(DummyDb(None), 1) == ("zh", "zh", "follow_input")',
        'session_payload = type("SessionPayload", (), {"conversation_json": json.dumps({"preferred_language": "bogus", "source_language": "bogus"})})()',
        'assert _job_language_profile(DummyDb(session_payload), 1) == ("zh", "zh", "follow_input")',
        'provider_specs = {"demo": ProviderSpec(slug="demo", label="Demo", base_url="https://api.example.com/v1", model="demo-model", wire_api="chat")}',
        'env = _provider_env("demo", "sk-demo-key", provider_specs=provider_specs)',
        'assert env["LANGUAGE"] == "zh", env["LANGUAGE"]',
        'assert env["SOURCE_LANGUAGE"] == "zh", env["SOURCE_LANGUAGE"]',
        'print("novelclaw runtime ok")',
    )
)

NOVELCLAW_DEFAULT_CODE = "\n".join(
    (
        "from local_web_portal.app.settings import settings",
        "from local_web_portal.app.locale import normalize_ui_locale",
        'assert settings.ui_language == "zh", settings.ui_language',
        'assert normalize_ui_locale(None) == "zh"',
        'assert normalize_ui_locale("bogus") == "zh"',
    )
)

NOVELCLAW_CONFIG_EN_CODE = "\n".join(
    (
        "from local_web_portal.app.locale import normalize_ui_locale",
        'assert normalize_ui_locale(None) == "en"',
        'assert normalize_ui_locale("bogus") == "en"',
    )
)

NOVELCLAW_CONFIG_ZH_CODE = "\n".join(
    (
        "from local_web_portal.app.locale import normalize_ui_locale",
        'assert normalize_ui_locale(None) == "zh"',
        'assert normalize_ui_locale("bogus") == "zh"',
    )
)

COOKIE_NAME_AGREEMENT_CODE = "\n".join(
    (
        "from local_web_portal.app.locale import UI_LOCALE_COOKIE",
        "assert UI_LOCALE_COOKIE == 'colong_ui_locale'",
        "print('auth cookie ok')",
    )
)

MULTIAGENT_COOKIE_AGREEMENT_CODE = "\n".join(
    (
        MULTIAGENT_PRELUDE,
        "from local_web_portal.app.i18n import PRODUCT_LOCALE_COOKIE",
        "assert PRODUCT_LOCALE_COOKIE == 'colong_ui_locale'",
        "print('multiagent cookie ok')",
    )
)

CHECKS = (
    {
        "name": "auth foundation",
        "app_dir": ROOT_DIR / "apps" / "auth-portal",
        "cases": (
            {"env": {"WEB_UI_LANGUAGE": "zh"}, "clear_env": (), "code": AUTH_FOUNDATION_CODE},
            {"env": {"WEB_UI_LANGUAGE": "zh"}, "clear_env": (), "code": AUTH_ROUTE_CODE},
            {"env": {"WEB_UI_LANGUAGE": "zh"}, "clear_env": (), "code": COOKIE_NAME_AGREEMENT_CODE},
            {"env": {}, "clear_env": ("WEB_UI_LANGUAGE",), "code": AUTH_DEFAULT_CODE},
            {"env": {"WEB_UI_LANGUAGE": "en-US"}, "clear_env": (), "code": AUTH_CONFIG_EN_CODE},
            {"env": {"WEB_UI_LANGUAGE": "zh-CN"}, "clear_env": (), "code": AUTH_CONFIG_ZH_CODE},
        ),
    },
    {
        "name": "multiagent foundation",
        "app_dir": ROOT_DIR / "apps" / "multiagent",
        "cases": (
            {"env": {"WEB_UI_LANGUAGE": "zh"}, "clear_env": (), "code": MULTIAGENT_FOUNDATION_CODE},
            {"env": {"WEB_UI_LANGUAGE": "zh"}, "clear_env": (), "code": MULTIAGENT_ROUTE_CODE},
            {"env": {"WEB_UI_LANGUAGE": "zh"}, "clear_env": (), "code": MULTIAGENT_COOKIE_AGREEMENT_CODE},
            {"env": {}, "clear_env": ("WEB_UI_LANGUAGE",), "code": MULTIAGENT_DEFAULT_CODE},
            {"env": {"WEB_UI_LANGUAGE": "en-US"}, "clear_env": (), "code": MULTIAGENT_CONFIG_EN_CODE},
            {"env": {"WEB_UI_LANGUAGE": "zh-CN"}, "clear_env": (), "code": MULTIAGENT_CONFIG_ZH_CODE},
        ),
    },
    {
        "name": "novelclaw foundation",
        "app_dir": ROOT_DIR / "apps" / "novelclaw",
        "cases": (
            {"env": {"WEB_UI_LANGUAGE": "zh"}, "clear_env": (), "code": NOVELCLAW_FOUNDATION_CODE},
            {"env": {"WEB_UI_LANGUAGE": "zh"}, "clear_env": (), "code": NOVELCLAW_ROUTE_CODE},
            {"env": {"WEB_UI_LANGUAGE": "zh"}, "clear_env": (), "code": NOVELCLAW_RUNTIME_CODE},
            {"env": {}, "clear_env": ("WEB_UI_LANGUAGE",), "code": NOVELCLAW_DEFAULT_CODE},
            {"env": {"WEB_UI_LANGUAGE": "en-US"}, "clear_env": (), "code": NOVELCLAW_CONFIG_EN_CODE},
            {"env": {"WEB_UI_LANGUAGE": "zh-CN"}, "clear_env": (), "code": NOVELCLAW_CONFIG_ZH_CODE},
        ),
    },
)


def _pythonpath_for(app_dir: Path) -> str:
    existing = os.environ.get("PYTHONPATH", "")
    parts = [str(app_dir)]
    if existing:
        parts.append(existing)
    return os.pathsep.join(parts)



def run_case(
    app_dir: Path,
    code: str,
    env_overrides: dict[str, str],
    clear_env: tuple[str, ...] = (),
) -> None:
    env = dict(os.environ)
    for key in clear_env:
        env.pop(key, None)
    env["PYTHONPATH"] = _pythonpath_for(app_dir)
    env.update(env_overrides)
    result = subprocess.run(
        [sys.executable, "-c", code],
        cwd=str(ROOT_DIR),
        env=env,
        capture_output=True,
        text=True,
    )
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.returncode != 0:
        if result.stderr:
            sys.stderr.write(result.stderr)
        raise SystemExit(result.returncode)



def run_check(name: str, app_dir: Path, cases: tuple[dict[str, object], ...]) -> None:
    for case in cases:
        run_case(
            app_dir=app_dir,
            code=str(case["code"]),
            env_overrides=dict(case["env"]),
            clear_env=tuple(case.get("clear_env", ())),
        )
    print(f"{name} ok")



def main() -> None:
    for check in CHECKS:
        run_check(
            name=str(check["name"]),
            app_dir=Path(check["app_dir"]),
            cases=tuple(check["cases"]),
        )
    print("locale contract ok")


if __name__ == "__main__":
    main()
