#!/bin/bash
echo "📚 Generando documentación..."
if command -v mkdocs &> /dev/null; then
    mkdocs build
    echo "✅ Documentación generada en el directorio 'site/'."
else
    echo "⚠️ MkDocs no está instalado. Ejecuta: pip install mkdocs"
fi
