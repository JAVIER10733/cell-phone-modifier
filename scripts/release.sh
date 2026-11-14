#!/bin/bash
echo "🚀 Preparando nueva versión de CPM..."

# Pedir la nueva versión
read -p "Ingresa la nueva versión (ej. 1.0.1): " NEW_VERSION

# Actualizar el archivo VERSION
echo "$NEW_VERSION" > VERSION

# Hacer commit
git add VERSION
git commit -m "chore: release v$NEW_VERSION"
git tag "v$NEW_VERSION"

echo "✅ Versión $NEW_VERSION lista. No olvides hacer 'git push origin main --tags'."
