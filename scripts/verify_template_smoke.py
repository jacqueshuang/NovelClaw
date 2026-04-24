from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parents[1]

TEMPLATE_CASES = [
    (
        ROOT / "apps/auth-portal/local_web_portal/app/templates",
        "select_mode.html",
    ),
    (
        ROOT / "apps/multiagent/local_web_portal/app/templates",
        "dashboard.html",
    ),
    (
        ROOT / "apps/novelclaw/local_web_portal/app/templates",
        "dashboard.html",
    ),
]

for directory, template_name in TEMPLATE_CASES:
    env = Environment(loader=FileSystemLoader(str(directory)))
    env.get_template(template_name)

for css_path in [
    ROOT / "apps/auth-portal/local_web_portal/app/static/style.css",
    ROOT / "apps/multiagent/local_web_portal/app/static/style.css",
    ROOT / "apps/novelclaw/local_web_portal/app/static/style.css",
]:
    css = css_path.read_text(encoding="utf-8")
    for token in [
        "--ui-bg",
        "--ui-surface",
        "--ui-border",
        "--ui-shadow",
        "--ui-accent",
    ]:
        assert token in css, f"{css_path.name} missing {token}"

auth_template = (ROOT / "apps/auth-portal/local_web_portal/app/templates/select_mode.html").read_text(encoding="utf-8")
auth_css = (ROOT / "apps/auth-portal/local_web_portal/app/static/style.css").read_text(encoding="utf-8")
for marker in [
    "launch-hub-metric-row",
    "launch-hub-route-summary",
    "launch-hub-system-note",
]:
    assert marker in auth_template, f"auth portal template missing {marker}"
    assert marker in auth_css, f"auth portal css missing {marker}"

for template_name in [
    "dashboard.html",
    "jobs.html",
    "providers.html",
    "sessions.html",
    "idea_copilot.html",
]:
    text = (ROOT / "apps/multiagent/local_web_portal/app/templates" / template_name).read_text(encoding="utf-8")
    assert 'shared_locale() == "zh"' in text, f"{template_name} missing shared locale check"
    assert 'locale() == "zh-CN"' not in text, f"{template_name} still uses internal locale check"

multiagent_base = (ROOT / "apps/multiagent/local_web_portal/app/templates/base.html").read_text(encoding="utf-8")
multiagent_css = (ROOT / "apps/multiagent/local_web_portal/app/static/style.css").read_text(encoding="utf-8")
assert '<select id="locale-switch"' not in multiagent_base
assert 'value="zh"' in multiagent_base and 'value="en"' in multiagent_base
for marker in [
    "console-locale-switch",
    "lang-btn",
]:
    assert marker in multiagent_base, f"multiagent base missing {marker}"
    assert marker in multiagent_css, f"multiagent css missing {marker}"

novel_base = (ROOT / "apps/novelclaw/local_web_portal/app/templates/base.html").read_text(encoding="utf-8")
assert 'aria-pressed="{% if ui_language == \'zh\' %}true{% else %}false{% endif %}"' in novel_base
assert 'aria-pressed="{% if ui_language == \'en\' %}true{% else %}false{% endif %}"' in novel_base

models_template = (ROOT / "apps/novelclaw/local_web_portal/app/templates/console_models.html").read_text(encoding="utf-8")
assert 'ws-shell-head' in models_template, 'console_models.html still uses the old flat admin header'

for template_path in [
    ROOT / 'apps/auth-portal/local_web_portal/app/templates/select_mode.html',
    ROOT / 'apps/multiagent/local_web_portal/app/templates/base.html',
    ROOT / 'apps/novelclaw/local_web_portal/app/templates/base.html',
]:
    text = template_path.read_text(encoding='utf-8')
    assert '中文' in text and 'English' in text, f'{template_path.name} missing shared switcher labels'

print("template smoke ok")
