# Backend

## Run

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

You can add `--reload` to automatically reload the backend.

## Seed Templates

```bash
uv run python -m scripts.seed_templates
```

## Test Template Rendering

Render a test CV with sample data (automatically seeds templates first):

```bash
uv run python -m scripts.test_render
```

Then compile to PDF:

```bash
typst compile templates/rendered_test.typ templates/rendered_test.pdf
```

## Test LLM Service (Full Integration)

Test the complete CV generation flow with real LLM calls (requires server running):

```bash
uv run python -m scripts.demo_llm
```

This creates a user, project, skills, calls the LLM API, and generates a complete CV.
You can compilte it with `typst compile templates/llm_test_output.typ`
