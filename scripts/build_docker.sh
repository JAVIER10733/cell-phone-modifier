#!/bin/bash
echo "🐳 Construyendo imagen de Docker para CPM..."
docker build -t cell-phone-modifier:latest .
echo "✅ Imagen construida con éxito."
