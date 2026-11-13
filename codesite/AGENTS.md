# Repository Guidelines

## Project Structure & Module Organization

`codesite/` holds Django settings, URL routing, and ASGI/WSGI entry points. Feature code lives in Django apps: `core/` for shared pages and layout, `python_problems/` for the coding-problem domain and Judge0 integration, `forums/` for feedback forums, and `animations/` for data-structure demonstrations. Keep each app's views, forms, models, URLs, templates, and static assets together. Put reusable problem-domain logic in `python_problems/services/` and language utilities in `python_problems/utils/`. Commit generated Django migrations under each app's `migrations/` directory.

## Build, Test, and Development Commands

Create a virtual environment, then install Python dependencies with `python -m pip install -r requirements.txt`. Start the application with `DJANGO_ENV=local DJANGO_SECRET_KEY=dev-secret python manage.py runserver`; local development uses Redis at `127.0.0.1:6379` by default. Apply schema changes with `python manage.py migrate`; generate app migrations with `python manage.py makemigrations <app>`.

Run Django tests with `python manage.py test`. Install browser-test dependencies with `npm ci`, install a browser with `npx playwright install --with-deps`, and run end-to-end tests with `npm run test:e2e`. Playwright starts the Django server unless one is already running.

## Coding Style & Naming Conventions

Follow the surrounding Python style: four-space indentation, `snake_case` functions and variables, `PascalCase` classes, and concise imports grouped at the top. Use Django `TestCase` classes and methods named `test_<behavior>`. Keep template partials descriptive and underscore-prefixed, such as `_problem_detail_title.html`; use kebab-case for static asset names. No formatter or linter is configured, so match nearby code and keep changes focused.

## Testing Guidelines

Add unit coverage beside the affected app in `tests.py`, especially for model, form, service, and view behavior. Place browser scenarios in `tests/*.spec.ts` and use Playwright's `test('<behavior>', ...)` form. Tests that exercise code execution depend on the configured Judge0 service and seeded problem data; isolate pure logic in Django tests when practical.

## Commit & Pull Request Guidelines

Recent commits use short, imperative summaries, often naming the affected behavior (for example, `remove old app sql problems` or `fix: problem header ...`). Keep the subject focused and avoid unrelated edits. Pull requests should explain the user-visible change, identify migrations or configuration changes, link the relevant issue when available, and include screenshots for template or CSS changes. Run the relevant Django and Playwright tests before requesting review.

## Configuration & Security

Keep credentials in environment variables (`DJANGO_SECRET_KEY`, database settings, OAuth keys, and service URLs); `.env` is ignored and must not be committed. Review `codesite/settings.py` when adding deployment-dependent configuration.
