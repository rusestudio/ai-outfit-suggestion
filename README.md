# AI Outfit Suggestion – Local Setup

This repository is a prototype for a fashion recommendation system that combines weather data, user inputs, a locally‑hosted LLM, and a local image generator. Everything runs on your machine using free/open‑source tools – no paid APIs are required.

---

## Project Structure

- `clothes_data/` – static JSON files (`all_clothing_types.json`, `all_material_data.json`) containing types, materials and other clothing info scraped from websites. Used by the prompt builder.

- `api_out/` – output directory for images produced by the Stable Diffusion WebUI. Sub‑folder `txt2img/` holds PNG files that are served by the FastAPI endpoint.

- `model_server/` – utilities for testing and running the local model servers; currently contains `test_ollama.py` which demonstrates calling the Ollama API.

- `data/` – project presentation file such as `finalpresentation.pdf`.

- single‑file helpers at the repo root:
  * `clothes_data_crawl.py` – crawler for clothing data (unused by production server).
  * `data_to_be_prompt.py` – provides the `clothes_data` dictionary imported by other modules.
  * `prompt.py` – builds prompts for the LLM and extracts image prompts from responses.
  * `llm_model_suggest.py` – handles communication with the Ollama server and parsing of its output.
  * `google_weather.py` – wrapper around the OpenWeatherMap API.

- `main.py` – FastAPI application. Handles form submission, fetches weather, calls the LLM, triggers image generation, and renders HTML templates (`templates/index.html` and `templates/result.html`).

- `templates/` – Jinja2 templates used by the FastAPI server.

- `requirements.txt` – Python dependencies.

- `.env` – environment variables for local configuration (not checked in with sensitive values).

---

## How It Works
1. **User submits** a date, destination and environment via the web form (`/`).
2. **FastAPI** controller (`/submit`) retrieves weather from OpenWeatherMap using `google_weather.get_weather`.
3. **Prompt builder** composes a natural-language request containing weather, available clothing types & materials, and user inputs.
4. **Ollama** (running locally) is queried via its HTTP API. The response includes three outfit suggestions and inline image prompts.
5. **Response parser** cleans up text and extracts the image prompts.
6. **Stable Diffusion WebUI** (AUTOMATIC1111) is called with each prompt to produce PNGs; they are saved to `api_out/txt2img`.
7. **Result page** displays the explanations and generated images; images are served through a `/download/{filename}` endpoint.

---

## Local Setup and Running

1. **Create & activate a Python virtual environment** (recommended):
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1  # Windows PowerShell
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start Ollama** (LLM server):
   ```bash
   ollama run <model-name>        # e.g. llama3 or any downloaded model
   ```
   The API listens on `http://localhost:11434` by default.

4. **Start AUTOMATIC1111 Stable Diffusion WebUI** for image generation.
   Follow the instructions in its GitHub repo; the default API endpoint is
   `http://127.0.0.1:7860/sdapi/v1/txt2img`.

5. **Configure environment variables** (populate a `.env` file or export in shell):
   ```env
   API_KEY_WEATHER=<your-openweathermap-key>
   # optional overrides (defaults shown):
   OLLAMA_API_URL="http://localhost:11434/api/generate"
   OLLAMA_MODEL="llama3"
   SD_WEBUI_URL="http://127.0.0.1:7860/sdapi/v1/txt2img"
   ```

6. **Run the FastAPI server**:
   ```bash
   uvicorn main:app --reload
   ```

7. **Open your browser** at `http://localhost:8000` and try the outfit suggestion form.

> ⚠️ Make sure both Ollama and the WebUI are running before submitting the form. The application will fall back to defaults if environment variables are missing, but the services must be reachable.

---

## Notes & Future Work

* The project is designed to be completely offline; all models run as local servers (Ollama for text, AUTOMATIC1111 WebUI for images). If a server is not running you may see connection errors – contact the developer to ensure the model processes are are started before testing.
* The local‑service architecture means the app is sensitive to port changes; override endpoints with environment variables if necessary.
* Old experiment folders have mostly been removed; keep `model_server` for any future tooling around the local model APIs.
* Image files are currently stored on disk; a future enhancement could save them in a database or cloud storage.
* The prompt templates in `prompt.py` are simple; feel free to refine them for better fashion advice.

Enjoy building your local AI‑powered outfit advisor!  🚀