#!/bin/bash

# Build script para Render
echo "=== RENDER BUILD SCRIPT ==="

# Instalar dependências
echo "📦 Installing Python packages..."
pip install -r requirements.txt

# Criar diretórios necessários
echo "📁 Creating directories..."
mkdir -p model
mkdir -p parameter

# Treinar modelo se não existir
echo "🤖 Training model..."
python train_model.py

# Verificar se arquivos foram criados
echo "✅ Checking files..."
ls -la model/
ls -la parameter/

echo "🚀 Build completed successfully!"
