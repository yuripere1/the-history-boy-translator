# History Boy Translator — OpenRouter version

This version uses an OpenRouter-compatible chat API through a small Node backend.
The API key is deliberately kept out of the browser.

## 1. Get a key
Create an OpenRouter account and API key at https://openrouter.ai/

## 2. Install
Node.js 18+ is recommended. No npm packages are required.

## 3. Set your key

macOS/Linux:
```bash
export OPENROUTER_API_KEY="YOUR_KEY_HERE"
npm start
```

Windows PowerShell:
```powershell
$env:OPENROUTER_API_KEY="YOUR_KEY_HERE"
npm start
```

The server runs at http://localhost:3000.

## 4. Open the app
Open `index.html` in your browser. The default backend endpoint is:
http://localhost:3000/api/translate

The default model is `openrouter/free`.

## Security
Do not put the API key into `index.html`, commit it to GitHub, or send it in a client-side request.
For public deployment, put the backend behind HTTPS and configure CORS to your site.

## Important
Free-model availability and limits are controlled by OpenRouter and can change. If
`openrouter/free` is unavailable, choose an available free model in the app or OpenRouter dashboard.
