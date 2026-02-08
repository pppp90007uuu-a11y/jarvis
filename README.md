# Jarvis Assistant (Pro Upgrade)

Yeh repo ek professional-grade scaffold provide karta hai jo tumhare "Jarvis" assistant ko
upgrade karke ek disciplined, permission-based local companion banata hai. Isme clean structure,
configuration, memory handling, safety checks, aur CLI flow diya gaya hai, taa ki aage jaa kar tools,
skills, aur integrations add karna easy ho.

## Features
- **Modular structure** for core logic, config, memory, safety, and runtime state.
- **CLI entrypoint** with modes (assistant, trading, automation, focus, study).
- **Logging setup** for production-friendly diagnostics.
- **Config loading** via environment variables and `.env` support.
- **Memory store** for reminders and user-approved notes.
- **Safety checks** for camera/screen permissions and destructive actions.
- **Hindi voice output** via system TTS (espeak/say) with explicit opt-in.

## Quick Start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m jarvis.main --help
```

## Usage examples
```bash
python -m jarvis.main "Jarvis screen dekho"
python -m jarvis.main --mode trading "NIFTY 50 ka trend batao"
python -m jarvis.main --mode trading "Set symbol NIFTY50"
python -m jarvis.main --mode trading "Set timeframe 15m"
python -m jarvis.main --mode ironman "Mission plan banao"
python -m jarvis.main --remember "Kal 10 baje meeting remind karna"
python -m jarvis.main --speak "Jarvis hello bolo"
python -m jarvis.main "Jarvis status"
python -m jarvis.main "Jarvis listen on"
python -m jarvis.main "Jarvis memory clear karo"
```

## Environment variables
```
JARVIS_NAME=Jarvis
JARVIS_ENV=development
JARVIS_LOG_LEVEL=INFO
JARVIS_WAKE_WORD=Jarvis
JARVIS_HOTKEY=Ctrl+Shift+J
JARVIS_LOCALE=hi-IN
JARVIS_MEMORY_ENABLED=true
JARVIS_MEMORY_PATH=.jarvis_memory.json
JARVIS_VOICE_ENABLED=false
JARVIS_TTS_ENGINE=espeak
JARVIS_TTS_VOICE=hi
JARVIS_REQUIRE_WAKE_WORD=true
```

## Next Steps
- Add tool integrations (browser, files, APIs).
- Add conversation memory (local db or vector store).
- Add skill registry + routing for specialized tasks.

## Behavior notes
- Assistant default me idle rehta hai jab tak wake word nahi aata.
- Sensitive actions ke liye confirm/cancel flow enforce hota hai.
- Trading mode analysis-only hota hai; trade execute nahi kiya jaata.
- Camera/screen/voice access explicit consent ke bina start nahi hota.
- Iron Man mode me concise status + mission-style planning focus hota hai.
