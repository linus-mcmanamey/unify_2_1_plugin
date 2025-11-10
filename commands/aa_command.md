---
description: Discuss multi-agent workflow strategy for a specific task
argument-hint: [task-description]
allowed-tools: Read, Task, TodoWrite
---

# Multi-Agent Workflow Discussion

Prepare to discuss how you will use a multi-agent workflow to ${ARGUMENTS}.

## Instructions

1. **Analyze the Task**: ${ARGUMENTS}
   - Break down the complexity
   - Identify parallelizable components
   - Determine if multi-agent approach is optimal

2. **Evaluate Approach**:
   - Should this use `/background` (single agent) or `/orchestrate` (multiple agents)?
   - How many agents would be optimal?
   - What are the dependencies between subtasks?

3. **Design Strategy**:
   - Outline the orchestration plan
   - Define agent responsibilities
   - Specify communication format (JSON responses)
   - Identify quality gates

4. **Provide Recommendations**:
   - Best command to use (`/background` vs `/orchestrate`)
   - Number of agents (if using orchestrate: 2-8)
   - Subtask breakdown
   - Estimated completion time
   - Resource requirements

## Output Format

Provide a structured discussion covering:

1. **Task Analysis**: Understanding of "${ARGUMENTS}"
2. **Complexity Assessment**: Simple/Moderate/High
3. **Recommended Approach**: `/background` or `/orchestrate`
4. **Agent Breakdown** (if orchestrate):
   - Agent 1: Responsibility
   - Agent 2: Responsibility
   - ...
5. **Dependencies**: None / Sequential / Hybrid
6. **Estimated Time**: X minutes
7. **Next Steps**: Commands to run

## Examples

### Example 1: Simple Task
```
User: /aa_command "optimize the g_x_mg_statsclasscount table"

Output:
Task Analysis: Single gold table optimization - focused work
Complexity: Moderate
Recommended: /background
Reasoning: Single file, sequential optimization steps
Estimated Time: 15 minutes
Next Step: /background "Optimize g_x_mg_statsclasscount.py for performance"
```

### Example 2: Complex Task
```
User: /aa_command "implement data quality framework across all layers"

Output:
Task Analysis: Cross-layer feature implementation
Complexity: High
Recommended: /orchestrate
Agent Breakdown:
  - Agent 1: Design quality schema and base classes
  - Agent 2: Implement bronze layer validators
  - Agent 3: Implement silver layer validators
  - Agent 4: Implement gold layer validators
  - Agent 5: Create validation tests
  - Agent 6: Update documentation
Dependencies: Agent 1 must complete before 2-4 (hybrid approach)
Estimated Time: 45-60 minutes
Next Step: Create task file and run /orchestrate data_quality_framework.md
```

### Example 3: Medium Complexity
```
User: /aa_command "fix all linting errors in the silver layer"

Output:
Task Analysis: Code quality fixes across multiple files
Complexity: Moderate-High
Recommended: /orchestrate (if >15 files) or /background (if <15 files)
Agent Breakdown:
  - Agent 1: Fix linting in silver_cms files
  - Agent 2: Fix linting in silver_fvms files
  - Agent 3: Fix linting in silver_nicherms files
Dependencies: None (fully parallel)
Estimated Time: 20-30 minutes
Next Step: /orchestrate "Fix linting errors: silver_cms, silver_fvms, silver_nicherms in parallel"
```

## Usage

```bash
# Discuss strategy for any task
/aa_command "optimize all gold tables for performance"

# Get recommendations for feature implementation
/aa_command "add monitoring and alerting to the pipeline"

# Plan refactoring work
/aa_command "refactor all ETL classes to use new base class pattern"

# Evaluate testing strategy
/aa_command "write comprehensive tests for the medallion architecture"
```

## Notes

- This command helps you plan before executing
- Use this to determine optimal agent strategy
- Creates a blueprint for `/background` or `/orchestrate` commands
- Considers parallelism, dependencies, and complexity
- Provides concrete next steps and command examples
