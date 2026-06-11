#!/usr/bin/env bash
set -euo pipefail

RECOMMENDED_MODELS=("llama3.2:3b" "gemma3:4b")
OPTIONAL_MODEL="qwen2.5-coder:7b"

echo "Checking Ollama installation..."

if ! command -v ollama >/dev/null 2>&1; then
  cat <<'EOF'
Ollama is not installed or is not on your PATH.

Install it on macOS:
  1. Download Ollama from https://ollama.com/download
  2. Open the app once so the local server starts.
  3. Re-run this script.

If you use Homebrew, you can also try:
  brew install --cask ollama
EOF
  exit 1
fi

echo "Ollama found: $(ollama --version)"
echo

for model in "${RECOMMENDED_MODELS[@]}"; do
  echo "Pulling recommended model: ${model}"
  ollama pull "${model}"
  echo
done

echo "Optional model: ${OPTIONAL_MODEL}"
echo "This coding model can be useful, but it may be slow or memory-heavy on an 8 GB MacBook Air M2."
read -r -p "Pull ${OPTIONAL_MODEL} now? [y/N] " pull_optional

case "${pull_optional}" in
  [yY]|[yY][eE][sS])
    echo "Pulling optional model: ${OPTIONAL_MODEL}"
    ollama pull "${OPTIONAL_MODEL}"
    ;;
  *)
    echo "Skipping ${OPTIONAL_MODEL}. You can pull it later with: ollama pull ${OPTIONAL_MODEL}"
    ;;
esac

cat <<'EOF'

Ollama model setup complete.

Try these test commands:
  ollama run llama3.2:3b "Say hello in one sentence."
  python src/local_ollama_test.py
  python src/local_ollama_test.py gemma3:4b

If Ollama is not running, open the Ollama app or run:
  ollama serve
EOF
