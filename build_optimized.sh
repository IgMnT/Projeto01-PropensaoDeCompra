#!/bin/bash

# Build script otimizado para Render (baixo uso de memória)
echo "=== RENDER BUILD SCRIPT (MEMORY OPTIMIZED) ==="

# Limpar cache antes de instalar
echo "🧹 Clearing pip cache..."
pip cache purge

# Instalar dependências sem cache
echo "📦 Installing Python packages (no cache)..."
pip install --no-cache-dir -r requirements.txt

# Criar diretórios necessários
echo "📁 Creating directories..."
mkdir -p model
mkdir -p parameter

# Treinar modelo leve
echo "🤖 Training lightweight model..."
python train_lightweight_model.py

# Limpar arquivos temporários
echo "🧹 Cleaning up..."
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true

# Verificar se arquivos foram criados
echo "✅ Checking files..."
ls -la model/ || echo "Model directory empty"
ls -la parameter/ || echo "Parameter directory empty"

echo "🚀 Build completed successfully!"
