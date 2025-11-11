# Unify 2.1 Plugin Marketplace

This plugin is available through the Claude Code marketplace system.

## Quick Install via Marketplace

### Option 1: Install from This Repository (Recommended)

```bash
# Add this marketplace
/plugin marketplace add linus-mcmanamey/unify_2_1_plugin

# Browse available plugins
/plugin

# Install the plugin
/plugin install unify_2_1
```

### Option 2: Install from Community Marketplaces

Once submitted to community marketplaces, you can also install via:

```bash
# Example: From claude-code-plugins-plus
/plugin marketplace add jeremylongshore/claude-code-plugins-plus
/plugin install unify_2_1
```

## What Gets Installed

- ✅ **16 Specialized Agents** - Multi-agent orchestration with Chain of Verification
- ✅ **28 Slash Commands** - Complete workflow automation
- ✅ **9 Skills** - On-demand knowledge loading
- ✅ **3 Intelligent Hooks** - Automatic skill activation and orchestrator routing

## Post-Installation Configuration

After installation, configure the hooks in your `~/.claude/settings.json`:

```json
{
  "hooks": {
    "user-prompt-submit": ".claude/plugins/repos/unify_2_1/hooks/combined-prompt-hook.py"
  }
}
```

Then **restart Claude Code** for changes to take effect.

## Marketplace Submission Status

### Current Status
- ✅ Marketplace.json created
- ✅ GitHub repository published
- ⏳ Pending submission to community marketplaces

### Submit to Community Marketplaces

To submit this plugin to popular community marketplaces:

#### 1. Claude Code Plugins Plus (243+ plugins)
**Repository**: https://github.com/jeremylongshore/claude-code-plugins-plus

**Submission Process**:
1. Fork the repository
2. Add plugin entry to `.claude-plugin/marketplace.json`
3. Create pull request with:
   - Plugin metadata
   - Description and features
   - Installation instructions
   - Screenshots/examples

#### 2. CCPlugins Curated Marketplace
**Repository**: https://github.com/ccplugins/marketplace

**Submission Process**:
1. Fork the repository
2. Add plugin to `plugins/` directory
3. Update marketplace.json
4. Submit PR with detailed description

#### 3. Claude Code Marketplace (Web)
**Website**: https://claudecodemarketplace.com/

**Submission Process**:
1. Contact maintainers via GitHub issues
2. Provide plugin repository URL
3. Include detailed feature list
4. Wait for review and approval

#### 4. ingpoc Marketplace
**Repository**: https://github.com/ingpoc/claude-code-plugins-marketplace

**Submission Process**:
1. Fork the repository
2. Create plugin directory with metadata
3. Add to marketplace catalog
4. Submit PR with complete documentation

## Plugin Entry Format for Submissions

When submitting to marketplaces, use this entry:

```json
{
  "name": "unify_2_1",
  "source": {
    "type": "git",
    "url": "https://github.com/linus-mcmanamey/unify_2_1_plugin.git"
  },
  "description": "Enterprise-grade PySpark data engineering with multi-agent orchestration, intelligent hooks, and Azure Synapse integration. Features 16 agents, 28 commands, 9 skills, and automatic complexity-based routing.",
  "version": "1.0.0",
  "author": "Linus McMananey",
  "license": "MIT",
  "keywords": ["pyspark", "azure", "synapse", "etl", "medallion", "orchestration", "multi-agent", "hooks"],
  "homepage": "https://github.com/linus-mcmanamey/unify_2_1_plugin"
}
```

## Creating Your Own Marketplace

Want to share with your team? Create your own marketplace:

### Step 1: Create Marketplace Repository

```bash
# Create new repository
mkdir my-team-plugins
cd my-team-plugins
git init
```

### Step 2: Add Marketplace Configuration

Create `.claude-plugin/marketplace.json`:

```json
{
  "name": "my-team-marketplace",
  "metadata": {
    "description": "Internal plugins for my team",
    "version": "1.0.0"
  },
  "owner": {
    "name": "Your Name",
    "email": "your.email@company.com"
  },
  "plugins": [
    {
      "name": "unify_2_1",
      "source": {
        "type": "git",
        "url": "https://github.com/linus-mcmanamey/unify_2_1_plugin.git"
      },
      "description": "Unify 2.1 data engineering plugin",
      "version": "1.0.0"
    }
  ]
}
```

### Step 3: Share with Team

```bash
# Push to GitHub
git add .
git commit -m "Add team marketplace"
git push origin main

# Team members install with:
/plugin marketplace add your-org/my-team-plugins
/plugin install unify_2_1
```

## Verification

After installation, verify the plugin:

```bash
# Check installed plugins
/plugin list

# Test a command
/prime-claude --analyze-only

# Test hooks (should see orchestrator analysis on complex prompts)
```

## Updating the Plugin

Users can update to the latest version:

```bash
# Update marketplace catalog
/plugin marketplace update linus-mcmanamey/unify_2_1_plugin

# Update installed plugin
/plugin update unify_2_1
```

## Uninstalling

To remove the plugin:

```bash
/plugin uninstall unify_2_1
```

## Support

For installation issues:
- 📖 Full documentation: [README.md](README.md)
- 🔧 Installation guide: [INSTALLATION.md](INSTALLATION.md)
- 🐛 Report issues: [GitHub Issues](https://github.com/linus-mcmanamey/unify_2_1_plugin/issues)

## License

MIT License - See [LICENSE](LICENSE) file

---

**Marketplace Version**: 1.0.0
**Last Updated**: 2025-11-10
**Repository**: https://github.com/linus-mcmanamey/unify_2_1_plugin
