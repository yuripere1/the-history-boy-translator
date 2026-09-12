# History Boy Translator — Streamlit + OpenRouter

A Streamlit app that translates text into the supplied History Boy voice using OpenRouter.

## GitHub files

Put these in the root of your GitHub repository:

- `app.py`
- `requirements.txt`
- `README.md`

## Streamlit Community Cloud

When creating the app:

- Repository: your GitHub repository
- Branch: `main`
- Main file path: `app.py`

Streamlit Community Cloud supports secrets through the app's Advanced settings.

## Add your OpenRouter key

After creating the app, open its settings and add this secret:

```toml
OPENROUTER_API_KEY = "sk-or-v1-your-key-here"
```

Do NOT commit the key to GitHub.

## Model

The app defaults to:

```text
openrouter/free
```

You can change the model inside the app to another OpenRouter model slug available to you.

## Local run

Install dependencies:

```bash
pip install -r requirements.txt
```

Create:

```text
.streamlit/secrets.toml
```

with:

```toml
OPENROUTER_API_KEY = "sk-or-v1-your-key-here"
```

Then:

```bash
streamlit run app.py
```

Never commit `.streamlit/secrets.toml`.
