---
description: Orchestrate multiple generic agents working in parallel on complex tasks
argument-hint: [user-prompt] | [task-file-name]
allowed-tools: Read, Task, TodoWrite
---

# Multi-Agent Orchestrator

Launch an orchestrator agent that coordinates multiple generic agents working in parallel on complex, decomposable tasks. All agents communicate via JSON format for structured coordination.

## Usage

**Option 1: Direct prompt**
```
/orchestrate "Analyze all gold tables, identify optimization opportunities, and implement improvements across the codebase"
```

**Option 2: Task file from .claude/tasks/**
```
/orchestrate multi_agent_pipeline_optimization.md
```

**Option 3: List available orchestration tasks**
```
/orchestrate list
```

## Variables

- `TASK_INPUT`: Either a direct prompt string or a task file name from `.claude/tasks/`
- `TASK_FILE_PATH`: Full path to task file if using a task file
- `PROMPT_CONTENT`: The actual prompt to send to the orchestrator agent

## Instructions

### 1. Determine Task Source

Check if `$ARGUMENTS` looks like a file name (ends with `.md` or contains no spaces):
- If YES: It's a task file name from `.claude/tasks/`
- If NO: It's a direct user prompt
- If "list": Show available orchestration task files

### 2. Load Task Content

**If using task file:**
1. List all available task files in `.claude/tasks/` directory
2. Find the task file matching the provided name (exact match or partial match)
3. Read the task file content
4. Use the full task file content as the prompt

**If using direct prompt:**
1. Use the `$ARGUMENTS` directly as the prompt

**If "list" command:**
1. Show all available orchestration task files with metadata
2. Exit without launching agents

### 3. Launch Orchestrator Agent

Launch the orchestrator agent using the Task tool with the following configuration:

**Important Configuration:**
- **subagent_type**: `general-purpose`
- **model**: `sonnet` (default) or `opus` for highly complex orchestrations
- **description**: Short 3-5 word description (e.g., "Orchestrate pipeline optimization")
- **prompt**: Complete orchestrator instructions (see template below)

**Orchestrator Prompt Template:**
```
You are an ORCHESTRATOR AGENT coordinating multiple generic worker agents on a complex project task.

PROJECT CONTEXT:
- Project: Unify 2.1 Data Migration using Azure Synapse Analytics
- Architecture: Medallion pattern (Bronze/Silver/Gold layers)
- Primary Language: PySpark Python
- Follow: .claude/CLAUDE.md and .claude/rules/python_rules.md

YOUR ORCHESTRATOR RESPONSIBILITIES:
1. Analyze the main task and decompose it into 2-8 independent subtasks
2. Launch multiple generic worker agents (use Task tool with subagent_type="general-purpose")
3. Provide each worker agent with:
   - Clear, self-contained instructions
   - Required context (file paths, requirements)
   - Expected JSON response format
4. Collect and aggregate all worker responses
5. Validate completeness and consistency
6. Produce final consolidated report

MAIN TASK TO ORCHESTRATE:
{TASK_CONTENT}

WORKER AGENT COMMUNICATION PROTOCOL:
Each worker agent MUST return results in this JSON format:
```json
{
  "agent_id": "unique_identifier",
  "task_assigned": "brief description",
  "status": "completed|failed|partial",
  "results": {
    "files_modified": ["path/to/file1.py", "path/to/file2.py"],
    "changes_summary": "description of changes",
    "metrics": {
      "lines_added": 0,
      "lines_removed": 0,
      "functions_added": 0,
      "issues_fixed": 0
    }
  },
  "quality_checks": {
    "syntax_check": "passed|failed",
    "linting": "passed|failed",
    "formatting": "passed|failed"
  },
  "issues_encountered": ["issue1", "issue2"],
  "recommendations": ["recommendation1", "recommendation2"],
  "execution_time_seconds": 0
}
```

WORKER AGENT PROMPT TEMPLATE:
When launching each worker agent, use this prompt structure:

```
You are a WORKER AGENT (ID: {agent_id}) reporting to an orchestrator.

CRITICAL: You MUST return your results in JSON format as specified below.

PROJECT CONTEXT:
- Read and follow: .claude/CLAUDE.md and .claude/rules/python_rules.md
- Coding Standards: 240 char lines, no blanks in functions, type hints required
- Use: @synapse_error_print_handler decorator, NotebookLogger, TableUtilities

YOUR ASSIGNED SUBTASK:
{subtask_description}

FILES TO WORK ON:
{file_list}

REQUIREMENTS:
{specific_requirements}

QUALITY GATES (MUST RUN):
1. python3 -m py_compile <modified_files>
2. ruff check python_files/
3. ruff format python_files/

REQUIRED JSON RESPONSE FORMAT:
```json
{
  "agent_id": "{agent_id}",
  "task_assigned": "{subtask_description}",
  "status": "completed",
  "results": {
    "files_modified": [],
    "changes_summary": "",
    "metrics": {
      "lines_added": 0,
      "lines_removed": 0,
      "functions_added": 0,
      "issues_fixed": 0
    }
  },
  "quality_checks": {
    "syntax_check": "passed|failed",
    "linting": "passed|failed",
    "formatting": "passed|failed"
  },
  "issues_encountered": [],
  "recommendations": [],
  "execution_time_seconds": 0
}
```

Work autonomously, complete your task, run quality gates, and return the JSON response.
```

ORCHESTRATION WORKFLOW:
1. **Task Decomposition**: Break main task into 2-8 independent subtasks
2. **Agent Assignment**: Create unique agent IDs (agent_1, agent_2, etc.)
3. **Parallel Launch**: Launch all worker agents simultaneously using Task tool
4. **Monitor Progress**: Track each agent's completion
5. **Collect Results**: Parse JSON responses from each worker agent
6. **Validate Output**: Ensure all quality checks passed
7. **Aggregate Results**: Combine all worker outputs
8. **Generate Report**: Create comprehensive orchestration summary

FINAL ORCHESTRATOR REPORT FORMAT:
```json
{
  "orchestration_summary": {
    "main_task": "{original task description}",
    "total_agents_launched": 0,
    "successful_agents": 0,
    "failed_agents": 0,
    "total_execution_time_seconds": 0
  },
  "agent_results": [
    {worker_agent_json_response_1},
    {worker_agent_json_response_2},
    ...
  ],
  "consolidated_metrics": {
    "total_files_modified": 0,
    "total_lines_added": 0,
    "total_lines_removed": 0,
    "total_functions_added": 0,
    "total_issues_fixed": 0
  },
  "quality_validation": {
    "all_syntax_checks_passed": true,
    "all_linting_passed": true,
    "all_formatting_passed": true
  },
  "consolidated_issues": [],
  "consolidated_recommendations": [],
  "next_steps": []
}
```

BEST PRACTICES:
- Keep subtasks independent (no dependencies between worker agents)
- Provide complete context to each worker agent
- Launch all agents in parallel for maximum efficiency
- Validate JSON responses from each worker
- Aggregate metrics and results systematically
- Flag any worker failures or incomplete results
- Provide actionable next steps

Work autonomously and orchestrate the complete task execution.
```

### 4. Inform User

After launching the orchestrator, inform the user:
- Orchestrator agent has been launched
- Main task being orchestrated (summary)
- Expected number of worker agents to be spawned
- Estimated completion time (if known)
- The orchestrator will coordinate all work and provide a consolidated JSON report

## Task File Structure

Expected orchestration task file format in `.claude/tasks/`:

```markdown
# Orchestration Task Title

**Date Created**: YYYY-MM-DD
**Priority**: HIGH/MEDIUM/LOW
**Estimated Total Time**: X minutes
**Complexity**: High/Medium/Low
**Recommended Worker Agents**: N

## Main Objective
Clear description of the overall goal

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Suggested Subtask Decomposition

### Subtask 1: Title
**Scope**: Files/components affected
**Estimated Time**: X minutes
**Dependencies**: None or list other subtasks

**Description**: What needs to be done

**Expected Outputs**:
- Output 1
- Output 2

---

### Subtask 2: Title
**Scope**: Files/components affected
**Estimated Time**: X minutes
**Dependencies**: None or list other subtasks

**Description**: What needs to be done

**Expected Outputs**:
- Output 1
- Output 2

---

(Repeat for each suggested subtask)

## Quality Requirements
- All code must pass syntax validation
- All code must pass linting
- All code must be formatted
- All agents must return valid JSON

## Aggregation Requirements
- How to combine results from worker agents
- Validation steps for consolidated output
- Reporting requirements
```

## Examples

### Example 1: Pipeline Optimization
```
User: /orchestrate "Analyze and optimize all gold layer tables for performance"

Orchestrator launches 5 worker agents:
- agent_1: Analyze g_x_mg_* tables
- agent_2: Analyze g_xa_* tables
- agent_3: Review joins and aggregations
- agent_4: Check indexing strategies
- agent_5: Validate query plans

Each agent reports back with JSON results
Orchestrator aggregates findings and produces consolidated report
```

### Example 2: Code Quality Sweep
```
User: /orchestrate code_quality_improvement.md

Orchestrator reads task file with 8 categories
Launches 8 worker agents in parallel:
- agent_1: Fix linting issues in bronze layer
- agent_2: Fix linting issues in silver layer
- agent_3: Fix linting issues in gold layer
- agent_4: Add missing type hints
- agent_5: Update error handling
- agent_6: Improve logging
- agent_7: Optimize imports
- agent_8: Update documentation

Collects JSON from all 8 agents
Validates quality checks
Produces aggregated metrics report
```

### Example 3: Feature Implementation
```
User: /orchestrate "Implement data validation framework across all layers"

Orchestrator decomposes into:
- agent_1: Design validation schema
- agent_2: Implement bronze validators
- agent_3: Implement silver validators
- agent_4: Implement gold validators
- agent_5: Create validation tests
- agent_6: Update documentation

Coordinates execution
Collects results in JSON format
Validates completeness
Generates implementation report
```

## JSON Response Validation

The orchestrator MUST validate each worker agent response contains:

**Required Fields:**
- `agent_id`: String, unique identifier
- `task_assigned`: String, description of assigned work
- `status`: String, one of ["completed", "failed", "partial"]
- `results`: Object with:
  - `files_modified`: Array of strings
  - `changes_summary`: String
  - `metrics`: Object with numeric values
- `quality_checks`: Object with pass/fail values
- `issues_encountered`: Array of strings
- `recommendations`: Array of strings
- `execution_time_seconds`: Number

**Validation Checks:**
- All required fields present
- Status is valid enum value
- Arrays are properly formatted
- Metrics are numeric
- Quality checks are pass/fail
- JSON is well-formed and parseable

## Agent Coordination Patterns

### Pattern 1: Parallel Independent Tasks
```
Orchestrator launches all agents simultaneously
No dependencies between agents
Each agent works on separate files/components
Results aggregated at end
```

### Pattern 2: Sequential with Handoff (Not Recommended)
```
Orchestrator launches agent_1
Waits for agent_1 JSON response
Uses agent_1 results to inform agent_2 prompt
Launches agent_2 with context from agent_1
Continues chain
```

### Pattern 3: Hybrid (Parallel Groups)
```
Orchestrator identifies 2-3 independent groups
Launches all agents in group 1 in parallel
Waits for group 1 completion
Launches all agents in group 2 with context from group 1
Aggregates results from all groups
```

## Success Criteria

Orchestration task completion requires:
- ✅ All worker agents launched successfully
- ✅ All worker agents returned valid JSON responses
- ✅ All quality checks passed across all agents
- ✅ No unresolved issues or failures
- ✅ Consolidated metrics calculated correctly
- ✅ Comprehensive orchestration report provided
- ✅ All files syntax validated
- ✅ All files linted and formatted

## Best Practices

### For Orchestrator Design
- Keep worker tasks independent when possible
- Provide complete context to each worker
- Assign unique, meaningful agent IDs
- Specify clear JSON response requirements
- Validate all JSON responses
- Handle worker failures gracefully
- Aggregate results systematically
- Provide actionable consolidated report

### For Worker Agent Design
- Make each subtask self-contained
- Include all necessary context in prompt
- Specify exact file paths and requirements
- Define clear success criteria
- Require JSON response format
- Include quality gate validation
- Request execution metrics

### For Task Decomposition
- Break into 2-8 independent subtasks
- Avoid inter-agent dependencies
- Balance workload across agents
- Group related work logically
- Consider file/component boundaries
- Respect layer separation (bronze/silver/gold)

## Error Handling

### Worker Agent Failures
If a worker agent fails:
1. Orchestrator captures failure details
2. Marks agent status as "failed" in JSON
3. Continues with other agents
4. Reports failure in final summary
5. Suggests recovery steps

### JSON Parse Errors
If worker returns invalid JSON:
1. Orchestrator logs parse error
2. Attempts to extract partial results
3. Marks agent response as invalid
4. Flags for manual review
5. Continues with valid responses

### Quality Check Failures
If worker's quality checks fail:
1. Orchestrator flags the failure
2. Includes failure details in report
3. Prevents final approval
4. Suggests corrective actions
5. May relaunch worker with corrections

## Performance Optimization

### Parallel Execution
- Launch all independent agents simultaneously
- Use Task tool with multiple concurrent calls
- Maximize parallelism for faster completion
- Monitor resource utilization

### Agent Sizing
- 2-8 agents: Optimal for most tasks
- <2 agents: Consider using single agent instead
- >8 agents: May have coordination overhead
- Balance granularity vs overhead

### Context Management
- Provide minimal necessary context
- Avoid duplicating shared information
- Use references to shared documentation
- Keep prompts focused and concise

## Notes

- Orchestrator coordinates but doesn't do actual code changes
- Worker agents are general-purpose and autonomous
- All communication uses structured JSON format
- Quality validation is mandatory across all agents
- Failed agents don't block other agents
- Orchestrator produces human-readable summary
- JSON enables programmatic result processing
- Pattern scales from 2 to 8 parallel agents
- Best for complex, decomposable tasks
- Overkill for simple, atomic tasks
