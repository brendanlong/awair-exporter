#!/bin/bash
set -e

echo "Setting up development environment..."

echo "Installing dependencies..."
uv sync

echo "Installing project in development mode..."
uv pip install -e .

echo "Installing pre-commit hooks..."
pre-commit install

echo "Setup complete!"
