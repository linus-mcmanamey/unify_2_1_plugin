---
model: claude-haiku-4-5-20251001
allowed-tools: Bash(git:*), Read, Edit, Write, Task, mcp__*, mcp__ado__repo_get_pull_request_by_id, mcp__ado__repo_list_pull_request_threads, mcp__ado__repo_list_pull_request_thread_comments, mcp__ado__repo_reply_to_comment, mcp__ado__repo_resolve_comment, mcp__ado__repo_get_repo_by_name_or_id, mcp__ado__wit_add_work_item_comment
argument-hint: [PR_ID]
description: Address PR review feedback and update pull request
---

# Fix PR Review Issues

Address feedback from PR review comments, make necessary code changes, and update the pull request.

## Repository Configuration
- **Project**: Program Unify
- **Repository ID**: d3fa6f02-bfdf-428d-825c-7e7bd4e7f338
- **Repository Name**: unify_2_1_dm_synapse_env_d10

## What This Does

1. Retrieves PR details and all active review comments
2. Analyzes review feedback and identifies required changes
3. Makes code changes to address each review comment
4. Commits changes with descriptive message
5. Pushes to feature branch (automatically updates PR)
6. Replies to review threads confirming fixes
7. Resolves review threads when appropriate

## Implementation Logic

### 1. Get PR Information
- Use \`mcp__ado__repo_get_pull_request_by_id\` with PR_ID from \`$ARGUMENTS\`
- Extract source branch, target branch, and PR title
- Validate PR is still active

### 2. Retrieve Review Comments
- Use \`mcp__ado__repo_list_pull_request_threads\` to get all threads
- Filter for active threads (status = "Active")
- For each thread, use \`mcp__ado__repo_list_pull_request_thread_comments\` to get details
- Display all review comments with:
  - File path and line number
  - Reviewer name
  - Comment content
  - Thread ID (for later replies)

### 3. Checkout Feature Branch
\`\`\`bash
git fetch origin
git checkout <source-branch-name>
git pull origin <source-branch-name>
\`\`\`

### 4. Address Each Review Comment

**Categorise review comments first:**

#### Standard Code Quality Issues
Handle directly with Edit tool for:
- Type hints
- Line length violations
- Formatting issues
- Missing decorators
- Import organization
- Variable naming

**Implementation:**
1. Read affected file using Read tool
2. Analyze the feedback and determine required changes
3. Make code changes using Edit tool
4. Validate changes meet project standards

#### Complex PySpark Issues
**Use pyspark-engineer agent for:**
- Performance optimisation requests
- Partitioning strategy changes
- Shuffle optimisation
- Broadcast join refactoring
- Memory management improvements
- Medallion architecture violations
- Complex transformation logic

**Trigger criteria:**
- Review comment mentions: "performance", "optimisation", "partitioning", "shuffle", "memory", "medallion", "bronze/silver/gold layer"
- Files affected in: \`python_files/pipeline_operations/\`, \`python_files/silver/\`, \`python_files/gold/\`, \`python_files/utilities/session_optimiser.py\`

**Use Task tool to launch pyspark-engineer agent:**

\`\`\`
Task tool parameters:
- subagent_type: "pyspark-engineer"
- description: "Implement PySpark fixes for PR #[PR_ID]"
- prompt: "
  Address PySpark review feedback for PR #[PR_ID]:

  Review Comment Details:
  [For each PySpark-related comment, include:]
  - File: [FILE_PATH]
  - Line: [LINE_NUMBER]
  - Reviewer Feedback: [COMMENT_TEXT]
  - Thread ID: [THREAD_ID]

  Implementation Requirements:
  1. Read all affected files
  2. Implement fixes following these standards:
     - Maximum line length: 240 characters
     - No blank lines inside functions
     - Proper type hints for all functions
     - Use @synapse_error_print_handler decorator
     - PySpark DataFrame operations (not SQL)
     - Suffix _sdf for all DataFrames
     - Follow medallion architecture patterns
  3. Optimize for:
     - Performance and cost-efficiency
     - Data skew handling
     - Memory management
     - Proper partitioning strategies
  4. Ensure production readiness:
     - Error handling
     - Logging with NotebookLogger
     - Idempotent operations
  5. Run quality gates:
     - Syntax validation: python3 -m py_compile
     - Linting: ruff check python_files/
     - Formatting: ruff format python_files/

  Return:
  1. List of files modified
  2. Summary of changes made
  3. Explanation of how each review comment was addressed
  4. Any additional optimisations implemented
  "
\`\`\`

**Integration:**
- pyspark-engineer will read, modify, and validate files
- Agent will run quality gates automatically
- You will receive summary of changes
- Use summary for commit message and review replies

#### Validation for All Changes
Regardless of method (direct Edit or pyspark-engineer agent):
- Maximum line length: 240 characters
- No blank lines inside functions
- Proper type hints
- Use of \`@synapse_error_print_handler\` decorator
- PySpark best practices from \`.claude/rules/python_rules.md\`
- Document all fixes for commit message

### 5. Validate Changes
Run quality gates:
\`\`\`bash
# Syntax check
python3 -m py_compile <changed-file>

# Linting
ruff check python_files/

# Format
ruff format python_files/
\`\`\`

### 6. Commit and Push
\`\`\`bash
git add .
git commit -m "♻️ refactor: address PR review feedback - <brief-summary>"
git push origin <source-branch>
\`\`\`

**Commit Message Format:**
\`\`\`
♻️ refactor: address PR review feedback

Fixes applied:
- <file1>: <description of fix>
- <file2>: <description of fix>
- ...

Review comments addressed in PR #<PR_ID>
\`\`\`

### 7. Reply to Review Threads
For each addressed comment:
- Use \`mcp__ado__repo_reply_to_comment\` to add reply:
  \`\`\`
  ✅ Fixed in commit <SHA>

  Changes made:
  - <specific change description>
  \`\`\`
- Use \`mcp__ado__repo_resolve_comment\` to mark thread as resolved (if appropriate)

### 8. Report Results
Provide summary:
\`\`\`
PR Review Fixes Completed

PR: #<PR_ID> - <PR_Title>
Branch: <source-branch> → <target-branch>

Review Comments Addressed: <count>
Files Modified: <file-list>
Commit SHA: <sha>

Quality Gates:
✓ Syntax validation passed
✓ Linting passed
✓ Code formatting applied

The PR has been updated and is ready for re-review.
\`\`\`

## Error Handling

### No PR ID Provided
If \`$ARGUMENTS\` is empty:
- Use \`mcp__ado__repo_list_pull_requests_by_repo_or_project\` to list open PRs
- Display all PRs created by current user
- Prompt user to specify PR ID

### No Active Review Comments
If no active review threads found:
\`\`\`
No active review comments found for PR #<PR_ID>.

The PR may already be approved or have no feedback requiring changes.
Would you like me to re-run /pr-review to check current status?
\`\`\`

### Merge Conflicts
If \`git pull\` results in merge conflicts:
1. Display conflict files
2. Guide user through resolution:
   - Show conflicting sections
   - Suggest resolution based on context
   - Use Edit tool to resolve
3. Complete merge commit
4. Continue with review fixes

### Quality Gate Failures
If syntax check or linting fails:
1. Display specific errors
2. Fix automatically if possible
3. Re-run quality gates
4. Only proceed to commit when all gates pass

## Example Usage

### Fix Review for Specific PR
\`\`\`bash
/pr-fix-pr-review 5642
\`\`\`

### Fix Review for Latest PR
\`\`\`bash
/pr-fix-pr-review
\`\`\`
(Will list your open PRs if ID not provided)

## Best Practices

1. **Read all comments first** - Understand full scope before making changes
2. **Make targeted fixes** - Address each comment specifically
3. **Run quality gates** - Ensure changes meet project standards
4. **Descriptive replies** - Explain what was changed and why
5. **Resolve appropriately** - Only resolve threads when fix is complete
6. **Test locally** - Consider running relevant tests if available

## Integration with /deploy-workflow

This command is automatically called by \`/deploy-workflow\` when:
- \`/pr-review\` identifies issues requiring changes
- The workflow needs to iterate on PR quality before merging

The workflow will loop:
1. \`/pr-review\` → identifies issues (may include pyspark-engineer deep analysis)
2. \`/pr-fix-pr-review\` → addresses issues
   - Standard fixes: Direct Edit tool usage
   - Complex PySpark fixes: pyspark-engineer agent handles implementation
3. \`/pr-review\` → re-validates
4. Repeat until PR is approved

**PySpark-Engineer Integration:**
- Automatically triggered for performance and architecture issues
- Ensures optimised, production-ready PySpark code
- Maintains consistency with medallion architecture patterns
- Validates test coverage and quality gates

## Notes

- **Automatic PR Update**: Pushing to source branch automatically updates the PR
- **No New PR Created**: This updates the existing PR, doesn't create a new one
- **Preserves History**: All review iterations are preserved in commit history
- **Thread Management**: Replies and resolutions are tracked in Azure DevOps
- **Quality First**: Will not commit changes that fail quality gates
- **Intelligent Delegation**: Routes simple fixes to Edit tool, complex PySpark issues to specialist agent
- **Expert Optimisation**: pyspark-engineer ensures performance and architecture best practices
