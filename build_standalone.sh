#!/bin/bash
# Build standalone executable for Blacklist application

set -e

echo "🔨 Building Blacklist standalone executable..."

# Install PyInstaller if not already installed
echo "📦 Installing PyInstaller..."
/home/xsysop/Documents/python/.venv/bin/pip install pyinstaller

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build dist

# Build with PyInstaller
echo "🔧 Building executable..."
/home/xsysop/Documents/python/.venv/bin/pyinstaller blacklist.spec

# Check if build was successful
if [ -f "dist/Blacklist" ]; then
    echo "✅ Build successful!"
    echo "📦 Executable location: dist/Blacklist"
    echo "📊 Size: $(du -h dist/Blacklist | cut -f1)"
    echo ""
    echo "🚀 To run: ./dist/Blacklist"
    echo "📋 To distribute: Copy the entire 'dist/Blacklist' file"
else
    echo "❌ Build failed!"
    exit 1
fi
