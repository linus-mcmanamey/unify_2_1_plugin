---
description: Fires off a  agent in the background to complete tasks autonomously
argument-hint: [user-prompt] | [task-file-name]
allowed-tools: Read, Task, TodoWrite
---

# Background PySpark Data Engineer Agent

Launch a PySpark data engineer agent to work autonomously in the background on ETL tasks, data pipeline fixes, or code reviews.

## Usage

**Option 1: Direct prompt**
```
/background "Fix the validation issues in g_xa_mg_statsclasscount.py"
```

**Option 2: Task file from .claude/tasks/**
```
/background code_review_fixes_task_list.md
```

## Variables

- `TASK_INPUT`: Either a direct prompt string or a task file name from `.claude/tasks/`
- `TASK_FILE_PATH`: Full path to task file if using a task file
- `PROMPT_CONTENT`: The actual prompt to send to the agent

## Instructions

### 1. Determine Task Source

Check if `$ARGUMENTS` looks like a file name (ends with `.md` or contains no spaces):
- If YES: It's a task file name from `.claude/tasks/`
- If NO: It's a direct user prompt

### 2. Load Task Content

**If using task file:**
1. List all available task files in `.claude/tasks/` directory
2. Find the task file matching the provided name (exact match or partial match)
3. Read the task file content
4. Use the full task file content as the prompt

**If using direct prompt:**
1. Use the `$ARGUMENTS` directly as the prompt

### 3. Launch PySpark Data Engineer Agent

Launch the specialized `pyspark-data-engineer` agent using the Task tool:

**Important Configuration:**
- **subagent_type**: `pyspark-data-engineer`
- **model**: `sonnet` (default) or `opus` for complex tasks
- **description**: Short 3-5 word description based on task type
- **prompt**: Complete, detailed instructions including:
  - The task content (from file or direct prompt)
  - Explicit instruction to follow `.claude/CLAUDE.md` best practices
  - Instruction to run quality gates (syntax check, linting, formatting)
  - Instruction to create a comprehensive final report

**Prompt Template:**
```
You are a PySpark data engineer working on the Unify 2.1 Data Migration project using Azure Synapse Analytics.

CRITICAL INSTRUCTIONS:
- Read and follow ALL guidelines in .claude/CLAUDE.md
- Use .claude/rules/python_rules.md for coding standards
- Maximum line length: 240 characters
- No blank lines inside functions
- Use @synapse_error_print_handler decorator on all methods
- Use NotebookLogger for all logging (not print statements)
- Use TableUtilities methods for DataFrame operations

TASK TO COMPLETE:
{TASK_CONTENT}

QUALITY GATES (MUST RUN BEFORE COMPLETION):
1. Syntax validation: python3 -m py_compile <file_path>
2. Linting: ruff check python_files/
3. Formatting: ruff format python_files/

FINAL REPORT REQUIREMENTS:
Provide a comprehensive report including:
1. Summary of changes made
2. Files modified with line numbers
3. Quality gate results (syntax, linting, formatting)
4. Testing recommendations
5. Any issues encountered and resolutions
6. Next steps or follow-up tasks

Work autonomously and complete all tasks in the list. Use your available tools to read files, make edits, run tests, and validate your work.
```

### 4. Inform User

After launching the agent, inform the user:
- Agent has been launched in the background
- Task being worked on (summary)
- Estimated completion time (if known from task file)
- The agent will work autonomously and provide a final report

## Task File Structure

Expected task file format in `.claude/tasks/`:

```markdown
# Task Title

**Date Created**: YYYY-MM-DD
**Priority**: HIGH/MEDIUM/LOW
**Estimated Total Time**: X minutes
**Files Affected**: N

## Task 1: Description
**File**: path/to/file.py
**Line**: 123
**Estimated Time**: X minutes
**Severity**: CRITICAL/HIGH/MEDIUM/LOW

**Current Code**:
```python
# code
```

**Required Fix**:
```python
# fixed code
```

**Reason**: Explanation
**Testing**: How to verify

---

(Repeat for each task)
```

## Examples

### Example 1: Using Task File
```
User: /background code_review_fixes_task_list.md

Agent Response:
1. Lists available task files
2. Finds and reads code_review_fixes_task_list.md
3. Launches pyspark-data-engineer agent with task content
4. Informs user: "PySpark data engineer agent launched to complete 9 code review fixes (est. 27 minutes)"
```

### Example 2: Using Direct Prompt
```
User: /background "Add data validation methods to the statsclasscount gold table and ensure they are called in the transform method"

Agent Response:
1. Uses the prompt directly
2. Launches pyspark-data-engineer agent with the prompt
3. Informs user: "PySpark data engineer agent launched to add data validation methods"
```

### Example 3: Partial Task File Name Match
```
User: /background code_review

Agent Response:
1. Lists task files and finds "code_review_fixes_task_list.md"
2. Confirms match with user or proceeds if unambiguous
3. Launches agent with task content
```

## Available Task Files

List available task files from `.claude/tasks/` directory when user runs the command without arguments or with "list" argument:

```
/background
/background list
```

Output:
```
Available task files in .claude/tasks/:
1. code_review_fixes_task_list.md (9 tasks, 27 min, HIGH priority)

Usage:
  /background <task-file-name>    - Run agent with task file
  /background "your prompt"       - Run agent with direct prompt
  /background list               - Show available task files
```

## Agent Workflow

The pyspark-data-engineer agent will:

1. **Read Context**: Load .claude/CLAUDE.md, .claude/rules/python_rules.md
2. **Analyze Tasks**: Break down task list into actionable items
3. **Execute Changes**: Read files, make edits, apply fixes
4. **Validate Work**: Run syntax checks, linting, formatting
5. **Test Changes**: Execute relevant tests if available
6. **Generate Report**: Comprehensive summary of all work completed

## Best Practices

### For Task Files
- Keep tasks atomic and well-defined
- Include file paths and line numbers
- Provide current code and required fix
- Specify testing requirements
- Estimate time for each task
- Prioritize tasks (CRITICAL, HIGH, MEDIUM, LOW)

### For Direct Prompts
- Be specific about files and functionality
- Reference table/database names
- Specify layer (bronze, silver, gold)
- Include any business requirements
- Mention quality requirements

## Success Criteria

Agent task completion requires:
- ✅ All code changes implemented
- ✅ Syntax validation passes (python3 -m py_compile)
- ✅ Linting passes (ruff check)
- ✅ Code formatted (ruff format)
- ✅ No new issues introduced
- ✅ Comprehensive final report provided

## Notes

- The agent has access to all project files and tools
- It follows medallion architecture patterns (bronze/silver/gold)
- It uses established utilities (SparkOptimiser, TableUtilities, NotebookLogger)
- It respects project coding standards (240 char lines, no blanks in functions)
- It works autonomously without requiring additional user input
- Results are reported back when complete