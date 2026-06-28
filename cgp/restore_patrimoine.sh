#!/usr/bin/env bash
# Restaure patrimoine.json et history/ depuis le repo git privé chiffré.
# Usage : bash cgp/restore_patrimoine.sh
# Prérequis : age installé, ~/.age/key.txt présent, ~/patrimoine-backup cloné.

set -euo pipefail

AGE_KEY_FILE="$HOME/.age/key.txt"
BACKUP_REPO="$HOME/patrimoine-backup"
PATRIMOINE_FILE="/home/francois/dev/fdelbrayelle/cgp-skills/data/patrimoine.json"
HISTORY_DIR="/home/francois/dev/fdelbrayelle/cgp-skills/data/history"

command -v age >/dev/null 2>&1 || { echo "age non installé — sudo apt install age (Ubuntu) ou brew install age (macOS)" >&2; exit 1; }
[ -f "$AGE_KEY_FILE" ]     || { echo "Clé age introuvable : $AGE_KEY_FILE" >&2; exit 1; }
[ -d "$BACKUP_REPO/.git" ] || { echo "Repo backup introuvable : $BACKUP_REPO" >&2; exit 1; }

# Mise à jour du repo local
cd "$BACKUP_REPO"
git pull --quiet

# Restauration de patrimoine.json
[ -f "$BACKUP_REPO/patrimoine.json.age" ] || { echo "patrimoine.json.age absent du repo" >&2; exit 1; }
age --decrypt -i "$AGE_KEY_FILE" -o "$PATRIMOINE_FILE" "$BACKUP_REPO/patrimoine.json.age"
echo "✓ patrimoine.json restauré"

# Restauration des snapshots mensuels
if [ -d "$BACKUP_REPO/history" ]; then
    mkdir -p "$HISTORY_DIR"
    for f in "$BACKUP_REPO/history"/*.json.age; do
        [ -f "$f" ] || continue
        BASENAME=$(basename "$f" .json.age)
        age --decrypt -i "$AGE_KEY_FILE" -o "$HISTORY_DIR/$BASENAME.json" "$f"
        echo "✓ history/$BASENAME.json restauré"
    done
fi

echo ""
echo "Restauration terminée. Lancez /auditing:SKILL pour vérifier."
