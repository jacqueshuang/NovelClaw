# Launch Hub UI Refresh and Chinese Startup Parameter Notes Design

**Problem**

The current `auth-portal` `/select-mode` page still reads like an auth-derived screen even though it now acts as the main system entry. It explains too much in long paragraphs, does not make the difference between `MultiAgent` and `NovelClaw` decisive enough, and exposes startup information as scattered technical details instead of a clean onboarding surface. At the same time, the startup-required parameters are spread across root `.env.*.example` files and app-level `.env.example` files with mostly English comments, which increases setup friction.

**Design Goal**

Turn `/select-mode` into a launch hub that helps users choose the right workspace in seconds, and rewrite startup parameter comments into concise Chinese guidance that explicitly marks required, recommended, and optional values.

---

## Scope

### In scope
- Redesign `apps/auth-portal/local_web_portal/app/templates/select_mode.html` into a launch-hub style entry page.
- Adjust `apps/auth-portal/local_web_portal/app/templates/base.html` so the shell/title semantics match the new launch-hub role.
- Add a dedicated launch-hub CSS section in `apps/auth-portal/local_web_portal/app/static/style.css`.
- Rewrite Chinese comments in these startup example files:
  - `.env.auth-portal.example`
  - `.env.multiagent.example`
  - `.env.novelclaw.example`
  - `apps/auth-portal/local_web_portal/.env.example`
  - `apps/multiagent/local_web_portal/.env.example`
  - `apps/novelclaw/local_web_portal/.env.example`

### Out of scope
- Reworking `multiagent` or `novelclaw` dashboard internals.
- Renaming runtime parameters or changing backend behavior.
- Adding new startup APIs or new settings fields.
- Turning the launch hub into a global status dashboard.

---

## Current Codebase Facts

- `apps/auth-portal/local_web_portal/app/main.py` renders `/select-mode` and already provides all needed data for a decision page: `preview_session`, `current_mode`, `current_mode_label`, `mode_a_url`, and `mode_b_url`.
- The page is currently implemented in `apps/auth-portal/local_web_portal/app/templates/select_mode.html` and inherits from `apps/auth-portal/local_web_portal/app/templates/base.html`.
- The auth-portal stylesheet already contains a large auth-oriented page block near the bottom of `apps/auth-portal/local_web_portal/app/static/style.css`; the redesign can live as a new, semantic launch-hub section appended near the end instead of trying to retrofit every old auth selector.
- Startup parameters are split between root deployment examples and app-local `.env.example` files, and the relevant runtime readers are in:
  - `apps/auth-portal/local_web_portal/app/settings.py`
  - `apps/multiagent/local_web_portal/app/settings.py`
  - `apps/novelclaw/local_web_portal/app/settings.py`

---

## UX Direction

### Page role
The page should present itself as a **Launch Hub**, not a leftover auth form. It is the system’s entry decision screen.

### Information hierarchy
1. **Top bar** — brand, language switch, current mode/session summary.
2. **Hero** — one-line explanation of what this page is for.
3. **Workspace decision cards** — strong contrast between `MultiAgent` and `NovelClaw`, each with a focused CTA.
4. **Decision assist table** — “If your goal is X, choose Y.”
5. **Startup prep cards** — ports, required parameters, and launch order in one glance.

### Visual tone
- Product-like, calm, polished, and modern.
- Blue emphasis for `MultiAgent`, purple/indigo emphasis for `NovelClaw`.
- Less “auth page” glassmorphism; more structured launch console feel.
- Preserve responsiveness without changing backend routes.

---

## UI Component Design

### 1. Top bar
Replace the current auth-oriented header with a launch header:
- Brand mark: `NC`
- Title: `NovelClaw Launch Hub`
- Subtitle: short bilingual helper text
- Right side: language toggle, current mode chip, preview session chip

### 2. Hero
Short, decisive copy:
- Chinese: “选择你的写作工作台”
- English: “Choose your writing workspace”
- Supporting copy explains there are two entry paths: fast generation vs. long-form refinement.

### 3. Workspace cards
Each card should include:
- Workspace label
- One-sentence intent statement
- Three bullet-style strengths
- Active state indicator
- Primary CTA
- Low-priority technical route label

`MultiAgent` should feel like the quick-start path.
`NovelClaw` should feel like the long-form production path.

### 4. Decision assist table
A tiny comparison table removes ambiguity:
- “I want to start from one idea quickly” → `MultiAgent`
- “I want to build a long-running writing workspace” → `NovelClaw`

### 5. Startup prep cards
Three compact cards:
- **访问地址 / ports**
- **启动前至少准备的参数**
- **推荐启动顺序**

This keeps startup guidance visible without turning the page into documentation.

---

## Chinese Comment System for Startup Parameters

### Comment style
Each parameter should use short Chinese comments with this structure:
- Requiredness marker: `[必填]`, `[建议填写]`, `[可选]`, or `[建议保留默认]`
- Purpose in plain Chinese
- Default/fallback behavior when relevant
- If the code auto-generates a fallback value locally (for example `APP_SESSION_SECRET` in the app-local web env files), the comment should say that local preview can auto-create it but production should still treat it as required.

### Grouping
All example env files should be reorganized into clear groups when applicable:
- 访问与入口
- 会话与安全
- 数据存储
- 模型与 Provider
- 运行控制
- 高级开关

### Tone
- Explain the parameter in human language first.
- Mention default behavior when the code clearly defines one.
- Avoid backend jargon when a plain operational explanation is enough.

---

## File-Level Design

### UI files
- `apps/auth-portal/local_web_portal/app/templates/base.html`
  - Change the default title/body semantics from auth portal wording to launch hub wording.
- `apps/auth-portal/local_web_portal/app/templates/select_mode.html`
  - Replace the existing auth-style layout with a launch-hub structure.
- `apps/auth-portal/local_web_portal/app/static/style.css`
  - Append a dedicated `launch-hub-*` design block rather than overloading old `auth-*` selectors further.

### Parameter annotation files
- `.env.auth-portal.example`
- `.env.multiagent.example`
- `.env.novelclaw.example`
- `apps/auth-portal/local_web_portal/.env.example`
- `apps/multiagent/local_web_portal/.env.example`
- `apps/novelclaw/local_web_portal/.env.example`

These files should gain Chinese comments only; no key names or runtime semantics should change.

---

## Acceptance Criteria

### Launch hub page
- `/select-mode` reads as a system launch hub, not an auth page.
- Users can distinguish `MultiAgent` vs `NovelClaw` within a few seconds.
- The page includes a visible startup-prep section.
- Existing routes (`/mode-a`, `/mode-b`, `/ui-language`, `/logout`) remain unchanged.
- The template remains renderable with the existing context provided by `main.py`.

### Parameter comments
- Every startup-critical variable in the six target env example files has a Chinese explanation.
- Requiredness is explicit for secret, database, API key, and launch-control parameters.
- Comments align with actual defaults observed in the corresponding `settings.py` files.

---

## Risks and Controls

| Risk | Control |
|---|---|
| Page looks polished but still reads like a login form | Use new `launch-hub-*` semantics and a decision-first content structure |
| Parameter comments drift from actual runtime defaults | Base every comment on existing `settings.py` readers |
| Scope expands into dashboard redesign | Limit UI work to auth-portal `/select-mode` and shared shell wording |
| Styling becomes entangled with old auth selectors | Add a separate launch-hub CSS block instead of mutating the whole auth block |

---

## Implementation Boundary

This design intentionally keeps backend logic stable. The implementation should focus on template structure, CSS semantics, and comment clarity only.