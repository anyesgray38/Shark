# Shark

Your own terminal AI — starts with Claude, ends with your local model (no censorship).

## Quick Start

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key_here
python chat.py
```

## Switch to Your Own Local AI (no Claude, no censorship)

### 1. Install Ollama
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Pull a model
```bash
ollama pull llama3        # Meta Llama 3
ollama pull mistral       # Mistral 7B
ollama pull qwen2         # Qwen2
ollama pull phi3          # Microsoft Phi-3 (lightweight)
```

### 3. Switch Shark to local
```bash
python chat.py --set-provider local --set-model llama3
python chat.py   # now running 100% locally, no API key needed
```

Once switched, you can remove the `anthropic` package and delete `ANTHROPIC_API_KEY` entirely.

---

## Chat Commands

| Command | Description |
|---|---|
| `/quit` | Exit |
| `/save` | Save current session to `sessions/` |
| `/clear` | Clear conversation history |
| `/sessions` | List saved sessions |
| `/switch claude\|local` | Swap provider mid-session |
| `/system <text>` | Change system prompt |

## CLI Flags

```bash
python chat.py --provider local          # use local just this session
python chat.py --set-provider local      # save local as default
python chat.py --set-model mistral       # change local model
python chat.py --set-system "Be terse"   # set system prompt
python chat.py --load sessions/foo.json  # resume a session
python chat.py --no-stream               # disable streaming
python chat.py --sessions                # list sessions
```

## File Structure

```
Shark/
├── chat.py              # entry point
├── config.json          # your settings (edit directly or use --set-* flags)
├── requirements.txt
├── ai/
│   ├── providers/
│   │   ├── base.py          # provider interface
│   │   ├── claude_provider.py
│   │   └── local_provider.py  # Ollama / any OpenAI-compatible endpoint
│   └── core/
│       ├── config.py
│       ├── session.py
│       └── factory.py
└── sessions/            # saved chats (gitignored)
```

## Install OpenSSH Server (Debian/Ubuntu)

```bash
sudo apt install openssh-server
# or
bash install-openssh.sh
```
