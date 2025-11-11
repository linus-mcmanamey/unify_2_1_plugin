# Unify 2.1 Plugin Hooks

Intelligent prompt interception system with dual-stage hook pipeline for automatic skill activation and orchestrator routing.

## Overview

This plugin provides **three hooks** that work together to enhance Claude Code's capabilities:

1. **skill-activation-prompt** - Detects domain-specific needs and recommends skills
2. **orchestrator-interceptor** - Analyzes complexity and routes to multi-agent orchestration
3. **combined-prompt-hook** - Chains both hooks seamlessly

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│ USER PROMPT SUBMITTED                                        │
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ▼
    ┌────────────────────────────────────┐
    │   combined-prompt-hook.py          │ ← Single entry point
    │   (Hook Orchestration Layer)       │
    └────────────────┬───────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌───────────────────┐   ┌──────────────────────┐
│  STAGE 1: SKILLS  │   │  STAGE 2: ORCHESTRATOR│
│  skill-activation │   │  orchestrator-       │
│  -prompt.py       │   │  interceptor.py      │
└────────┬──────────┘   └──────────┬───────────┘
         │                          │
         ▼                          ▼
   ┌─────────────┐           ┌──────────────┐
   │ Detects     │           │ Analyzes     │
   │ domain      │           │ complexity   │
   │ skills      │           │ & routing    │
   │ needed      │           │              │
   └─────────────┘           └──────────────┘
         │                          │
         └────────────┬─────────────┘
                      │
                      ▼
            ┌──────────────────────┐
            │ COMBINED CONTEXT     │
            │ injected into        │
            │ Claude's conversation│
            └──────────────────────┘
```

## Hook 1: Skill Activation

**File**: `skill-activation-prompt.py`

**Purpose**: Load domain-specific knowledge before execution

**Detection Rules** (from `../skills/skill-rules.json`):
- Keywords: `["pyspark", "schema", "bronze", "silver", "gold", "etl", "transform"]`
- Intent patterns: `["generate.*pyspark", "create.*table", "transform.*data"]`

**Example Output**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 SKILL ACTIVATION CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ CRITICAL SKILLS (REQUIRED):
  → schema-reference

📚 RECOMMENDED SKILLS:
  → pyspark-patterns

ACTION: Use Skill tool BEFORE responding
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Hook 2: Orchestrator Interceptor

**File**: `orchestrator_interceptor.py`

**Purpose**: Analyze complexity and route to optimal execution strategy

**Classification Rules**:

| Pattern | Reason | Complexity | Action |
|---------|--------|------------|--------|
| "what is", "explain", <20 words | Simple query | simple_query | Skip orchestration |
| Contains "bronze", "silver", "gold" (2+) | Cross-layer work | high_complexity | Multi-agent (6-8) |
| "all", "across", "entire", "multiple" | Broad scope | complex_task | Multi-agent (4-6) |
| "linting", "formatting" + "all"/"entire" | Quality sweep | high_complexity | Multi-agent (6-8) |
| "implement", "create", "build" + >10 words | Implementation | moderate_task | Single agent or 2-3 |

**Cost Estimates**:
- Simple query: ~500 tokens, $0.002
- Moderate task: ~6,000 tokens, $0.018
- Complex task: ~17,000 tokens, $0.051
- High complexity: ~43,000 tokens, $0.129

**Example Output**:
```
<orchestrator-analysis-required>
ORCHESTRATOR INTERCEPTION ACTIVE

BEFORE responding to the user, you MUST:

1. Launch the master-orchestrator agent
2. USER PROMPT: "Fix linting across bronze, silver, and gold layers"
3. Classification: Cross Layer Work (High Complexity)
4. COST ESTIMATION:
   - Total estimated: ~43,000 tokens
   - Approximate cost: $0.129 USD

Present execution plan with user approval options.
</orchestrator-analysis-required>
```

## Hook 3: Combined Hook

**File**: `combined-prompt-hook.py`

**Purpose**: Chain both hooks seamlessly in pure Python

**Logic**:
1. Read prompt once from stdin
2. Pass to skill-activation-prompt.py → Get skill recommendations (JSON)
3. Pass to orchestrator_interceptor.py → Get complexity analysis (JSON)
4. Parse and merge both JSON outputs
5. Return combined JSON context

**Benefits**:
- No bash/jq dependencies
- Better error handling
- Type-safe with proper JSON parsing
- Easier to debug and maintain

## Installation

### Option 1: Plugin-Level (Recommended)

Update `.claude/settings.json` to use the plugin hooks:

```json
{
  "hooks": {
    "user-prompt-submit": ".claude/plugins/repos/unify_2_1/hooks/combined-prompt-hook.py"
  }
}
```

### Option 2: Global Level

Copy hooks to global hooks directory:

```bash
cp -r .claude/plugins/repos/unify_2_1/hooks/* ~/.claude/hooks/
```

Then configure in `~/.claude/settings.json`:

```json
{
  "hooks": {
    "user-prompt-submit": ".claude/hooks/combined-prompt-hook.py"
  }
}
```

**Restart Claude Code** after configuration changes.

## Configuration

### Adjust Skill Detection

Edit `../skills/skill-rules.json`:

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

### Adjust Orchestrator Classification

Edit `orchestrator_interceptor.py`:

```python
# Add custom patterns
def should_orchestrate(prompt: str) -> tuple[bool, str, str]:
    # Your custom logic here
    if "custom_pattern" in prompt.lower():
        return True, "custom_reason", "high_complexity"
```

### Adjust Cost Estimates

Edit `orchestrator_interceptor.py`:

```python
token_estimates = {
    "moderate_task": {
        "orchestrator_analysis": 1000,
        "agent_execution": 5000,
        "total_estimated": 6000,
        "cost_usd": 0.018
    },
    # Adjust as needed
}
```

## Monitoring & Logs

### Log Location

All orchestrator decisions logged to:
```
~/.claude/hook_logs/orchestrator_hook.log
```

### View Logs

```bash
# Real-time monitoring
tail -f ~/.claude/hook_logs/orchestrator_hook.log

# Recent entries
tail -50 ~/.claude/hook_logs/orchestrator_hook.log

# Search classifications
grep "Classified as" ~/.claude/hook_logs/orchestrator_hook.log

# View cost estimates
grep "Cost estimate" ~/.claude/hook_logs/orchestrator_hook.log
```

### Log Format

```
2025-11-10 23:00:44 | INFO     | ================================================================================
2025-11-10 23:00:44 | INFO     | Hook triggered - Session: abc123
2025-11-10 23:00:44 | INFO     | CWD: /workspaces/unify_2_1_dm_niche_rms_build_d10
2025-11-10 23:00:44 | INFO     | Prompt: Fix all linting errors across bronze, silver, and gold layers
2025-11-10 23:00:44 | INFO     | Classified as CROSS-LAYER WORK (3 layers)
2025-11-10 23:00:44 | INFO     | Decision: ORCHESTRATE
2025-11-10 23:00:44 | INFO     | Reason: cross_layer_work
2025-11-10 23:00:44 | INFO     | Complexity: high_complexity
2025-11-10 23:00:44 | INFO     | Cost estimate: $0.129 USD (~43,000 tokens)
2025-11-10 23:00:44 | INFO     | Hook completed successfully
2025-11-10 23:00:44 | INFO     | ================================================================================
```

### Log Rotation

- **Rotation**: 10 MB
- **Retention**: 30 days
- **Location**: `~/.claude/hook_logs/orchestrator_hook.log`

## Examples

### Example 1: Simple Domain Query

**Prompt**: "What is TableUtilities?"

**Skill Hook**:
```
📚 RECOMMENDED SKILLS: → pyspark-patterns
```

**Orchestrator Hook**:
```
<simple-query-detected>
Handle directly without orchestration overhead.
</simple-query-detected>
```

**Result**: Skill loaded for accurate answer, no orchestration overhead

### Example 2: Complex Multi-Layer Task

**Prompt**: "Fix linting across bronze, silver, and gold layers"

**Skill Hook**:
```
📚 RECOMMENDED SKILLS:
  → project-architecture
  → pyspark-patterns
```

**Orchestrator Hook**:
```
Classification: Cross-layer work (High complexity)
Cost: $0.129 USD (~43,000 tokens)
Strategy: Multi-agent (6-8 agents in parallel)
```

**Result**: Architecture loaded + Multi-agent orchestration plan presented

### Example 3: PySpark ETL Implementation

**Prompt**: "Generate gold table g_x_mg_vehicle_stats from silver_cms and silver_fvms"

**Skill Hook**:
```
⚠️ CRITICAL SKILLS:
  → schema-reference (exact schemas)
📚 RECOMMENDED SKILLS:
  → pyspark-patterns (TableUtilities methods)
```

**Orchestrator Hook**:
```
Classification: Implementation task (Moderate)
Cost: $0.018 USD (~6,000 tokens)
Strategy: Single pyspark-developer agent
```

**Result**: Schemas + patterns loaded, orchestrator plans single-agent execution

## Testing

### Test Skill Hook Only

```bash
echo '{"prompt":"Generate PySpark table from bronze_cms","session_id":"test","cwd":"/workspaces"}' | \
  python3 .claude/plugins/repos/unify_2_1/hooks/skill-activation-prompt.py | jq
```

### Test Orchestrator Hook Only

```bash
echo '{"session_id":"test","cwd":"/workspaces","prompt":"Fix linting across all layers"}' | \
  python3 .claude/plugins/repos/unify_2_1/hooks/orchestrator_interceptor.py | jq
```

### Test Combined Hook

```bash
echo '{"session_id":"test","cwd":"/workspaces","prompt":"Generate gold table from silver data"}' | \
  python3 .claude/plugins/repos/unify_2_1/hooks/combined-prompt-hook.py | jq
```

## Troubleshooting

### Hook Not Running

1. **Verify configuration**:
   ```bash
   cat .claude/settings.json | grep -A 2 hooks
   ```

2. **Check executability**:
   ```bash
   ls -l .claude/plugins/repos/unify_2_1/hooks/*.{sh,py}
   ```

3. **Test directly**:
   ```bash
   echo '{"prompt":"test"}' | python3 .claude/plugins/repos/unify_2_1/hooks/orchestrator_interceptor.py
   ```

4. **Restart Claude Code** (required for settings changes)

### Dependencies Missing

```bash
# Check loguru
python3 -c "import loguru; print(f'loguru {loguru.__version__}')"

# Install if needed
pip install loguru

# Check jq
which jq || sudo apt-get install -y jq
```

### Hook Errors

Hooks are fail-safe - errors don't block prompts:
- Error logged to `orchestrator_hook.log`
- Prompt passes through unchanged
- Claude responds normally

Check logs:
```bash
tail -50 ~/.claude/hook_logs/orchestrator_hook.log | grep ERROR
```

## Performance Impact

### Minimal Overhead

- **Skill hook**: <50ms (keyword matching, local file read)
- **Orchestrator hook**: <100ms (regex patterns, logging)
- **Total**: ~150ms added to each prompt

### When Hooks Skip

- Simple queries: Both hooks run but skip actions (~100ms)
- Domain queries: Skill loads, orchestrator skips (~120ms)
- Complex tasks: Both hooks activate fully (~150ms)

### Fail-Safe Design

- Hooks never block prompts
- Errors are caught and logged
- Default action: allow prompt through unchanged

## Integration with Plugin

### Plugin Components Using Hooks

- **16 Agents** - All benefit from orchestrator routing
- **30 Commands** - Some trigger orchestrator explicitly (`/orchestrate`)
- **9 Skills** - Activated automatically by skill hook

### Workflow

```
User types prompt
    ↓
Combined hook analyzes
    ↓
Skills loaded (if needed)
    ↓
Orchestrator invoked (if complex)
    ↓
Specialized agents launched (if approved)
    ↓
Results aggregated
    ↓
User receives comprehensive response
```

## Files

```
.claude/plugins/repos/unify_2_1/hooks/
├── README.md                          # This file
├── combined-prompt-hook.py            # Main entry point (chains hooks in Python)
├── orchestrator_interceptor.py        # Complexity analysis + routing
└── skill-activation-prompt.py         # Skill detection (Python implementation)
```

## Version History

**1.0.0** (2025-11-10)
- Initial release
- Dual-stage hook pipeline
- Skill activation + orchestrator routing
- Cost estimation
- Comprehensive logging

## Support

For issues:
1. Check logs: `~/.claude/hook_logs/orchestrator_hook.log`
2. Test hooks individually (see Testing section)
3. Verify dependencies (Python, loguru)
4. Review this README

## License

MIT License (same as parent plugin)
