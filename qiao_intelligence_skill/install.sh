#!/bin/bash

# Qiao Intelligence Skill Installation Script
# Installs the self-awareness skill in Claude skills directory

set -e

echo "🧠 Installing Qiao Intelligence Skill..."

# Define paths
SKILL_SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_NAME="qiao-intelligence"
CLAUDE_SKILLS_DIR="$HOME/.claude/skills"
SKILL_TARGET_DIR="$CLAUDE_SKILLS_DIR/$SKILL_NAME"

# Check if source directory exists
if [ ! -d "$SKILL_SOURCE_DIR" ]; then
    echo "❌ Error: Source directory not found: $SKILL_SOURCE_DIR"
    exit 1
fi

# Create Claude skills directory if it doesn't exist
echo "📁 Creating Claude skills directory..."
mkdir -p "$CLAUDE_SKILLS_DIR"

# Remove existing installation if present
if [ -d "$SKILL_TARGET_DIR" ]; then
    echo "🗑️  Removing existing installation..."
    rm -rf "$SKILL_TARGET_DIR"
fi

# Copy skill files
echo "📋 Copying skill files..."
cp -r "$SKILL_SOURCE_DIR" "$SKILL_TARGET_DIR"

# Set proper permissions
echo "🔐 Setting permissions..."
chmod -R 755 "$SKILL_TARGET_DIR"
chmod 644 "$SKILL_TARGET_DIR"/*.md
chmod 644 "$SKILL_TARGET_DIR"/references/*.md
chmod 755 "$SKILL_TARGET_DIR"/install.sh

# Verify installation
echo "✅ Verifying installation..."
if [ -f "$SKILL_TARGET_DIR/SKILL.md" ] && [ -f "$SKILL_TARGET_DIR/README.md" ]; then
    echo "✅ Skill files verified"
else
    echo "❌ Error: Skill files not properly installed"
    exit 1
fi

# Count files
SKILL_FILES=$(find "$SKILL_TARGET_DIR" -name "*.md" | wc -l)
REFERENCE_FILES=$(find "$SKILL_TARGET_DIR/references" -name "*.md" 2>/dev/null | wc -l)

echo ""
echo "🎉 Qiao Intelligence Skill installed successfully!"
echo ""
echo "📊 Installation Summary:"
echo "   📍 Location: $SKILL_TARGET_DIR"
echo "   📄 Skill files: $SKILL_FILES"
echo "   📚 Reference files: $REFERENCE_FILES"
echo ""
echo "🚀 Usage:"
echo "   Claude Code: 'Use the qiao-intelligence skill to analyze my research profile'"
echo "   Claude CLI:  claude --skill qiao-intelligence 'Analyze my research patterns'"
echo ""
echo "📖 Quick Start:"
echo "   1. Restart Claude Code/CLI to load the new skill"
echo "   2. Ask: 'Use qiao-intelligence to understand my research identity'"
echo "   3. Explore your project patterns and strategic insights"
echo ""
echo "🔄 Updates: Edit files in $SKILL_TARGET_DIR to update the skill"
echo ""
echo "💡 Pro Tip: Keep this skill updated as you create new projects!"
