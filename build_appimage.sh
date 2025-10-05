#!/bin/bash
# Build AppImage for Blacklist application

set -e

APP_NAME="Blacklist"
APP_VERSION="1.0"
APP_DIR="AppDir"

echo "🔨 Building $APP_NAME AppImage..."

# Clean previous build
rm -rf $APP_DIR
rm -f *.AppImage

# Create AppDir structure
mkdir -p $APP_DIR/usr/bin
mkdir -p $APP_DIR/usr/lib
mkdir -p $APP_DIR/usr/share/applications
mkdir -p $APP_DIR/usr/share/icons/hicolor/256x256/apps

# Copy application files
echo "📦 Copying application files..."
cp gui_terminal.py $APP_DIR/usr/bin/blacklist.py
cp blacklist.py $APP_DIR/usr/bin/
cp blacklist_theme.wav $APP_DIR/usr/bin/

# Create launcher script
cat > $APP_DIR/usr/bin/blacklist << 'EOF'
#!/bin/bash
DIR="$(dirname "$(readlink -f "$0")")"
cd "$DIR"
exec python3 blacklist.py "$@"
EOF
chmod +x $APP_DIR/usr/bin/blacklist

# Copy desktop file
cp blacklist.desktop $APP_DIR/usr/share/applications/

# Create a simple icon (text-based)
cat > $APP_DIR/usr/share/icons/hicolor/256x256/apps/blacklist.png << 'EOF'
This would be your icon file
EOF

# Create AppRun
cat > $APP_DIR/AppRun << 'EOF'
#!/bin/bash
SELF=$(readlink -f "$0")
HERE=${SELF%/*}
export PATH="${HERE}/usr/bin:${PATH}"
export LD_LIBRARY_PATH="${HERE}/usr/lib:${LD_LIBRARY_PATH}"
export PYTHONPATH="${HERE}/usr/bin:${PYTHONPATH}"
cd "${HERE}/usr/bin"
exec python3 gui_terminal.py "$@"
EOF
chmod +x $APP_DIR/AppRun

# Copy desktop file to root
cp blacklist.desktop $APP_DIR/

# Download appimagetool if not present
if [ ! -f appimagetool-x86_64.AppImage ]; then
    echo "📥 Downloading appimagetool..."
    wget -q https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
    chmod +x appimagetool-x86_64.AppImage
fi

# Build AppImage
echo "🔧 Building AppImage..."
ARCH=x86_64 ./appimagetool-x86_64.AppImage $APP_DIR ${APP_NAME}-${APP_VERSION}-x86_64.AppImage

echo "✅ AppImage created: ${APP_NAME}-${APP_VERSION}-x86_64.AppImage"
echo "🚀 Run with: ./${APP_NAME}-${APP_VERSION}-x86_64.AppImage"
