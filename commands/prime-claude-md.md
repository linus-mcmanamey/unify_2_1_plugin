---
name: prime-claude-md
description: Distill CLAUDE.md to essentials, moving detailed knowledge into skills for on-demand loading. Reduces context pollution by 80-90%.
args: [--analyze-only] | [--backup] | [--apply]
---

# Prime CLAUDE.md

Distill your CLAUDE.md file to only essential information, moving detailed knowledge into skills.

## Problem

Large CLAUDE.md files (400+ lines) are loaded into context for EVERY conversation:
- Wastes 5,000-15,000 tokens per conversation
- Reduces space for actual work
- Slows Claude's responses
- 80% of the content is rarely needed

## Solution

**Prime your CLAUDE.md**:
1. Keep only critical architecture and coding standards
2. Move detailed knowledge into skills (loaded on-demand)
3. Reduce from 400+ lines to ~100 lines
4. Save 80-90% context per conversation

## Usage

### Analyze Current CLAUDE.md
```bash
/prime-claude-md --analyze-only
```
Shows what would be moved to skills without making changes.

### Create Backup and Apply
```bash
/prime-claude-md --backup --apply
```
1. Backs up current CLAUDE.md to CLAUDE.md.backup
2. Creates supporting skills with detailed knowledge
3. Replaces CLAUDE.md with distilled version
4. Documents what was moved where

### Just Apply (No Backup)
```bash
/prime-claude-md --apply
```

## What Gets Distilled

### Kept in CLAUDE.md (Essential)
- Critical architecture concepts (high-level only)
- Mandatory coding standards (line length, blank lines, decorators)
- Quality gates (syntax check, linting, formatting)
- Essential commands (2-3 most common)
- References to skills for details

### Moved to Skills (Detailed Knowledge)

**project-architecture** skill:
- Detailed medallion architecture
- Pipeline execution flow
- Data source details
- Azure integration specifics
- Configuration management
- Testing architecture

**project-commands** skill:
- Complete make command reference
- All development workflows
- Azure operations
- Database operations
- Git operations
- Troubleshooting commands

**pyspark-patterns** skill:
- TableUtilities method documentation
- ETL class pattern details
- Logging standards
- DataFrame operation patterns
- JDBC connection patterns
- Performance tips

## Results

**Before Priming**:
- CLAUDE.md: 420 lines
- Context cost: ~12,000 tokens per conversation
- Skills: 0
- Knowledge: Always loaded

**After Priming**:
- CLAUDE.md: ~100 lines (76% reduction)
- Context cost: ~2,000 tokens per conversation (83% savings)
- Skills: 3 specialized skills
- Knowledge: Loaded only when needed

## Example Distilled CLAUDE.md

```markdown
# CLAUDE.md

**CRITICAL**: READ `.claude/rules/python_rules.md`

## Architecture
Medallion: Bronze → Silver → Gold
Core: `session_optimiser.py` (SparkOptimiser, NotebookLogger, TableUtilities)

## Essential Commands
python3 -m py_compile <file>  # Must run
ruff check python_files/       # Must pass
make run_all                   # Full pipeline

## Coding Standards
- Line length: 240 chars
- No blank lines in functions
- Use @synapse_error_print_handler
- Use logger (not print)

## Skills Available
- project-architecture: Detailed architecture
- project-commands: Complete command reference
- pyspark-patterns: PySpark best practices
```

## Benefits

1. **Faster conversations**: Less context overhead
2. **Better responses**: More room for actual work
3. **On-demand knowledge**: Load only what you need
4. **Maintainable**: Easier to update focused skills
5. **Reusable pattern**: Apply to any repository

## Applying to Other Repositories

This command is repository-agnostic. To use on another repo:

1. Run `/prime-claude-md --analyze-only` to see what you have
2. Command will identify:
   - Architectural concepts
   - Command references
   - Coding standards
   - Configuration details
3. Creates appropriate skills based on content
4. Run `/prime-claude-md --apply` when ready

## Files Created

```
.claude/
├── CLAUDE.md                          # Distilled (100 lines)
├── CLAUDE.md.backup                   # Original (if --backup used)
└── skills/
    ├── project-architecture/
    │   └── skill.md                   # Architecture details
    ├── project-commands/
    │   └── skill.md                   # Command reference
    └── pyspark-patterns/              # (project-specific)
        └── skill.md                   # Code patterns
```

## Philosophy

**CLAUDE.md should answer**: "What's special about this repo?"

**Skills should answer**: "How do I do X in detail?"

## Task Execution

I will:
1. Read current CLAUDE.md (both project and global if exists)
2. Analyze content and categorize
3. Create distilled CLAUDE.md (essential only)
4. Create supporting skills with detailed knowledge
5. If --backup: Save CLAUDE.md.backup
6. If --apply: Replace CLAUDE.md with distilled version
7. Generate summary report of changes

---

**Current Project**: Unify Data Migration (PySpark/Azure Synapse)

Let me analyze your CLAUDE.md and create the distilled version with supporting skills.
