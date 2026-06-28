#!/usr/bin/env bash
# Sauvegarde chiffrée de patrimoine.json + history/ vers le repo git privé.
# Appelé automatiquement par le hook PostToolUse Write de Claude Code.
# Ne fait rien si le contenu n'a pas changé depuis la dernière sauvegarde.

set -euo pipefail

PATRIMOINE_FILE="/home/francois/dev/fdelbrayelle/cgp-skills/data/patrimoine.json"
HISTORY_DIR="/home/francois/dev/fdelbrayelle/cgp-skills/data/history"
AGE_KEY_FILE="$HOME/.age/key.txt"
BACKUP_REPO="$HOME/patrimoine-backup"
HASH_CACHE="$BACKUP_REPO/.last_hash"

# Guards
[ -f "$PATRIMOINE_FILE" ]  || exit 0
[ -f "$AGE_KEY_FILE" ]     || exit 0
[ -d "$BACKUP_REPO/.git" ] || exit 0
command -v age >/dev/null 2>&1 || exit 0

# Sortie anticipée si le contenu n'a pas changé
CURRENT_HASH=$(sha256sum "$PATRIMOINE_FILE" | awk '{print $1}')
if [ -f "$HASH_CACHE" ] && [ "$(cat "$HASH_CACHE")" = "$CURRENT_HASH" ]; then
    exit 0
fi

# Extraction de la clé publique age
PUBKEY=$(grep -m1 'public key:' "$AGE_KEY_FILE" | awk '{print $NF}')
[ -n "$PUBKEY" ] || { echo "backup_patrimoine: clé publique age introuvable" >&2; exit 1; }

# Chiffrement de patrimoine.json
age -r "$PUBKEY" -o "$BACKUP_REPO/patrimoine.json.age" "$PATRIMOINE_FILE"

# Chiffrement des snapshots mensuels
if [ -d "$HISTORY_DIR" ]; then
    mkdir -p "$BACKUP_REPO/history"
    for f in "$HISTORY_DIR"/*.json; do
        [ -f "$f" ] || continue
        BASENAME=$(basename "$f" .json)
        age -r "$PUBKEY" -o "$BACKUP_REPO/history/$BASENAME.json.age" "$f"
    done
fi

# Commit et push si changement détecté
cd "$BACKUP_REPO"
git add -A
if git diff --cached --quiet; then
    exit 0
fi

git commit -m "backup: $(date -Iseconds)" --quiet
git push origin main --quiet

# Mise à jour du hash cache
echo "$CURRENT_HASH" > "$HASH_CACHE"
echo "patrimoine.json sauvegardé (chiffré) → fdelbrayelle/patrimoine-backup" >&2
