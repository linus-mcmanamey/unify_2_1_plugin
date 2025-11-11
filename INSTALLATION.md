# Unify 2.1 Plugin Installation Guide

## Quick Installation

### Step 1: Plugin is Already Installed

This plugin is **already configured** in this project at:
```
.claude/plugins/repos/unify_2_1/
```

### Step 2: Hook Configuration

The hooks are **already configured** in `.claude/settings.json`:

```json
{
  "hooks": {
    "user-prompt-submit": ".claude/plugins/repos/unify_2_1/hooks/combined-prompt-hook.py"
  }
}
```

### Step 3: Restart Claude Code

**Important**: After any changes to hooks or settings, restart Claude Code for changes to take effect.

```bash
# Close and reopen Claude Code
# OR use restart command if available
```

## Verification

### Test Hook Functionality

```bash
# Test simple query (should skip orchestration)
echo '{"prompt":"What is PySpark?"}' | \
  python3 .claude/plugins/repos/unify_2_1/hooks/orchestrator_interceptor.py | jq

# Test complex task (should trigger orchestration)
echo '{"prompt":"Fix linting across all layers"}' | \
  python3 .claude/plugins/repos/unify_2_1/hooks/orchestrator_interceptor.py | jq

# Test combined hook (skill + orchestrator)
echo '{"prompt":"Generate gold table from silver data"}' | \
  python3 .claude/plugins/repos/unify_2_1/hooks/combined-prompt-hook.py | jq
```

### Check Logs

```bash
# View recent hook activity
tail -50 ~/.claude/hook_logs/orchestrator_hook.log

# Monitor in real-time
tail -f ~/.claude/hook_logs/orchestrator_hook.log
```

## Plugin Components

### Directory Structure

```
.claude/plugins/repos/unify_2_1/
├── agents/                    # 16 specialized agents
│   ├── orchestrator.md
│   ├── pyspark-developer.md
│   ├── code-reviewer.md
│   └── ...
├── commands/                  # 30 slash commands
│   ├── orchestrate.md
│   ├── write-tests.md
│   ├── code-review.md
│   └── ...
├── skills/                    # 9 on-demand skills
│   ├── schema-reference.md
│   ├── pyspark-patterns.md
│   ├── project-architecture.md
│   └── skill-rules.json
├── hooks/                     # 3 intelligent hooks
│   ├── combined-prompt-hook.py
│   ├── orchestrator_interceptor.py
│   ├── skill-activation-prompt.py
│   └── README.md
├── plugin.json               # Plugin metadata
├── README.md                 # Plugin documentation
└── LICENSE
```

### What's Included

#### 16 Specialized Agents
- master-orchestrator
- developer-pyspark
- code-reviewer
- test-engineer
- developer-python
- developer-sql
- developer-azure-engineer
- performance-engineer
- git-manager
- code-documenter
- powershell-test-engineer
- developer-bash-shell
- business-analyst
- product-manager
- system-architect
- security-analyst

#### 30 Slash Commands
- /orchestrate - Multi-agent orchestration
- /write-tests - Pytest test generation
- /code-review - Comprehensive code review
- /describe - Add descriptive comments
- /local-commit - Well-formatted commits
- /pr-feature-to-staging - Create PR
- ... and 24 more

#### 9 Skills (On-Demand Knowledge)
- schema-reference - Automatic schema lookup
- pyspark-patterns - PySpark best practices
- project-architecture - Medallion architecture
- project-commands - Make command reference
- azure-devops - Azure DevOps operations
- mcp-code-execution - MCP integration
- multi-agent-orchestration - Coordination patterns
- skill-creator - Create new skills

#### 3 Intelligent Hooks
- **skill-activation-prompt** - Domain knowledge detection
- **orchestrator-interceptor** - Complexity analysis & routing
- **combined-prompt-hook** - Seamless chaining

## How It Works

### Automatic Prompt Routing

Every prompt you type goes through the dual-stage hook pipeline:

```
User Prompt
    ↓
┌───────────────────────┐
│ Stage 1: Skill Hook   │ → Detects domain needs
│ "Load schema-reference"
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Stage 2: Orchestrator │ → Analyzes complexity
│ "High complexity"     │
│ "$0.129 USD estimate" │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Claude Code           │ → Executes strategy
│ - Loads skills        │
│ - Launches orchestrator
│ - Presents plan       │
└───────────────────────┘
```

### Example: Simple Query

**Input**: "What is TableUtilities?"

**Hook Processing**:
- Skill: Load `pyspark-patterns` (keyword detected)
- Orchestrator: Skip orchestration (simple query)

**Result**: Direct answer with domain knowledge

### Example: Complex Task

**Input**: "Fix linting across bronze, silver, and gold layers"

**Hook Processing**:
- Skill: Load `project-architecture`, `pyspark-patterns`
- Orchestrator: High complexity (cross-layer work)
  - Cost: $0.129 USD (~43,000 tokens)
  - Strategy: Multi-agent (6-8 agents)

**Result**: Execution plan presented for approval

## Configuration

### Settings Location

**Project settings**: `.claude/settings.json`
```json
{
  "hooks": {
    "user-prompt-submit": ".claude/plugins/repos/unify_2_1/hooks/combined-prompt-hook.py"
  }
}
```

### Customize Skill Detection

Edit `.claude/plugins/repos/unify_2_1/skills/skill-rules.json`:

```json
{
  "skills": {
    "schema-reference": {
      "priority": "critical",
      "promptTriggers": {
        "keywords": ["schema", "table", "column"],
        "intentPatterns": ["generate.*table", "create.*etl"]
      }
    }
  }
}
```

### Customize Orchestrator Routing

Edit `.claude/plugins/repos/unify_2_1/hooks/orchestrator_interceptor.py`:

```python
# Add custom classification rules
def should_orchestrate(prompt: str) -> tuple[bool, str, str]:
    # Your custom patterns here
    if "my_pattern" in prompt.lower():
        return True, "my_reason", "high_complexity"
```

### Adjust Cost Estimates

Edit `.claude/plugins/repos/unify_2_1/hooks/orchestrator_interceptor.py`:

```python
token_estimates = {
    "moderate_task": {
        "orchestrator_analysis": 1000,
        "agent_execution": 5000,
        "total_estimated": 6000,
        "cost_usd": 0.018  # Adjust based on pricing
    }
}
```

## Troubleshooting

### Hooks Not Running

1. **Check settings**:
   ```bash
   cat .claude/settings.json | grep -A 2 hooks
   ```

2. **Verify hook files exist**:
   ```bash
   ls -l .claude/plugins/repos/unify_2_1/hooks/
   ```

3. **Check executability**:
   ```bash
   chmod +x .claude/plugins/repos/unify_2_1/hooks/*.sh
   chmod +x .claude/plugins/repos/unify_2_1/hooks/*.py
   ```

4. **Restart Claude Code** (required!)

### Dependencies Missing

```bash
# Check Python dependencies
python3 -c "import loguru; print('loguru OK')"
pip install loguru  # If missing
```

### Hook Errors

View logs for debugging:
```bash
tail -100 ~/.claude/hook_logs/orchestrator_hook.log | grep ERROR
```

Hooks are fail-safe - errors won't block your prompts.

## Monitoring

### View Hook Activity

```bash
# Real-time monitoring
tail -f ~/.claude/hook_logs/orchestrator_hook.log

# Recent decisions
tail -50 ~/.claude/hook_logs/orchestrator_hook.log

# Search for specific prompts
grep "Classified as" ~/.claude/hook_logs/orchestrator_hook.log

# View cost estimates
grep "Cost estimate" ~/.claude/hook_logs/orchestrator_hook.log
```

### Log Format

```
2025-11-10 23:27:22 | INFO | ================================================================
2025-11-10 23:27:22 | INFO | Hook triggered - Session: abc123
2025-11-10 23:27:22 | INFO | CWD: /workspaces/unify_2_1_dm_niche_rms_build_d10
2025-11-10 23:27:22 | INFO | Prompt: Generate gold table from silver_cms
2025-11-10 23:27:22 | INFO | Classified as CROSS-LAYER WORK (2 layers)
2025-11-10 23:27:22 | INFO | Decision: ORCHESTRATE
2025-11-10 23:27:22 | INFO | Reason: cross_layer_work
2025-11-10 23:27:22 | INFO | Complexity: high_complexity
2025-11-10 23:27:22 | INFO | Cost estimate: $0.129 USD (~43,000 tokens)
2025-11-10 23:27:22 | INFO | Hook completed successfully
2025-11-10 23:27:22 | INFO | ================================================================
```

## Advanced Usage

### Disable Hooks Temporarily

Comment out in `.claude/settings.json`:
```json
{
  // "hooks": {
  //   "user-prompt-submit": ".claude/plugins/repos/unify_2_1/hooks/combined-prompt-hook.py"
  // }
}
```

Then restart Claude Code.

### Test Individual Hooks

```bash
# Test skill hook only
echo '{"prompt":"Generate PySpark ETL","session_id":"test","cwd":"/workspaces"}' | \
  python3 .claude/plugins/repos/unify_2_1/hooks/skill-activation-prompt.py | jq

# Test orchestrator only
echo '{"prompt":"Fix linting everywhere"}' | \
  python3 .claude/plugins/repos/unify_2_1/hooks/orchestrator_interceptor.py

# Test combined
echo '{"prompt":"Complex task"}' | \
  python3 .claude/plugins/repos/unify_2_1/hooks/combined-prompt-hook.py
```

### Global vs Project Hooks

**Project hooks** (current setup):
- Configured in `.claude/settings.json`
- Uses project-local plugin
- Path: `.claude/plugins/repos/unify_2_1/hooks/`

**Global hooks** (alternative):
- Copy hooks to `~/.claude/hooks/`
- Configure in `~/.claude/settings.json`
- Available across all projects

## Documentation

- **Plugin README**: `.claude/plugins/repos/unify_2_1/README.md`
- **Hook Documentation**: `.claude/plugins/repos/unify_2_1/hooks/README.md`
- **Agent Reference**: `.claude/plugins/repos/unify_2_1/agents/`
- **Command Reference**: `.claude/plugins/repos/unify_2_1/commands/`
- **Skill Reference**: `.claude/plugins/repos/unify_2_1/skills/`

## Support

For issues or questions:
1. Check logs: `~/.claude/hook_logs/orchestrator_hook.log`
2. Review documentation in `.claude/plugins/repos/unify_2_1/`
3. Test hooks individually (see Testing section)
4. Verify dependencies and restart Claude Code

## License

MIT License - See LICENSE file in plugin directory

---

**Status**: ✅ Installed and configured
**Version**: 1.0.0
**Last Updated**: 2025-11-10
