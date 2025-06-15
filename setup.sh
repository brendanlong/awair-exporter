#!/bin/bash
set -e

echo "Setting up development environment..."

echo "Installing dependencies..."
uv sync

echo "Installing pre-commit hooks..."
pre-commit install

echo "Setup complete!"
