---
model: claude-haiku-4-5-20251001
allowed-tools: Bash(git branch:*), Bash(git status:*), Bash(git log:*), Bash(git diff:*), mcp__*, mcp__ado__repo_get_repo_by_name_or_id, mcp__ado__repo_list_pull_requests_by_repo_or_project, mcp__ado__repo_get_pull_request_by_id, mcp__ado__repo_list_pull_request_threads, mcp__ado__repo_list_pull_request_thread_comments, mcp__ado__repo_create_pull_request_thread, mcp__ado__repo_reply_to_comment, mcp__ado__repo_update_pull_request, mcp__ado__repo_search_commits, mcp__ado__pipelines_get_builds, Read, Task
argument-hint: [PR_ID] (optional - if not provided, will list all open PRs)
# PR Review and Approval
---
## Task
Review open pull requests in the current repository and approve/complete them if they meet quality standards.

## Instructions

### 1. Get Repository Information
- Use `mcp__ado__repo_get_repo_by_name_or_id` with:
  - Project: `Program Unify`
  - Repository: `unify_2_1_dm_synapse_env_d10`
- Extract repository ID: `d3fa6f02-bfdf-428d-825c-7e7bd4e7f338`

### 2. List Open Pull Requests
- Use `mcp__ado__repo_list_pull_requests_by_repo_or_project` with:
  - Repository ID: `d3fa6f02-bfdf-428d-825c-7e7bd4e7f338`
  - Status: `Active`
- If `$ARGUMENTS` provided, filter to that specific PR ID
- Display all open PRs with key details (ID, title, source/target branches, author)

### 3. Review Each Pull Request
For each PR (or the specified PR):

#### 3.1 Get PR Details
- Use `mcp__ado__repo_get_pull_request_by_id` to get full PR details
- Check merge status - if conflicts exist, stop and report

#### 3.2 Get PR Changes
- Use `mcp__ado__repo_search_commits` to get commits in the PR
- Identify files changed and scope of changes

#### 3.3 Review Code Quality
Read changed files and evaluate:
1. **Code Quality & Maintainability**
   - Proper use of type hints and descriptive variable names
   - Maximum line length (240 chars) compliance
   - No blank lines inside functions
   - Proper import organization
   - Use of `@synapse_error_print_handler` decorator
   - Proper error handling with meaningful messages

2. **PySpark Best Practices**
   - DataFrame operations over raw SQL
   - Proper use of `TableUtilities` methods
   - Correct logging with `NotebookLogger`
   - Proper session management

3. **ETL Pattern Compliance**
   - Follows ETL class pattern for Silver/Gold layers
   - Proper extract/transform/load method structure
   - Correct database and table naming conventions

4. **Standards Compliance**
   - Follows project coding standards from `.claude/rules/python_rules.md`
   - No missing docstrings (unless explicitly instructed to omit)
   - Proper use of configuration from `configuration.yaml`

#### 3.4 Review DevOps Considerations
1. **CI/CD Integration**
   - Changes compatible with existing pipeline
   - No breaking changes to deployment process

2. **Configuration & Infrastructure**
   - Proper environment detection pattern
   - Azure integration handled correctly
   - No hardcoded paths or credentials

3. **Testing & Quality Gates**
   - Syntax validation would pass
   - Linting compliance (ruff check)
   - Test coverage for new functionality

#### 3.5 Deep PySpark Analysis (Conditional)
**Only execute if PR modifies PySpark ETL code**

Check if PR changes affect:
- `python_files/pipeline_operations/bronze_layer_deployment.py`
- `python_files/pipeline_operations/silver_dag_deployment.py`
- `python_files/pipeline_operations/gold_dag_deployment.py`
- Any files in `python_files/silver/`
- Any files in `python_files/gold/`
- `python_files/utilities/session_optimiser.py`

**If PySpark files are modified, use Task tool to launch pyspark-engineer agent:**

```
Task tool parameters:
- subagent_type: "pyspark-engineer"
- description: "Deep PySpark analysis for PR #[PR_ID]"
- prompt: "
  Perform expert-level PySpark analysis for PR #[PR_ID]:

  PR Details:
  - Title: [PR_TITLE]
  - Changed Files: [LIST_OF_CHANGED_FILES]
  - Source Branch: [SOURCE_BRANCH]
  - Target Branch: [TARGET_BRANCH]

  Review Requirements:
  1. Read all changed PySpark files
  2. Analyze transformation logic for:
     - Partitioning strategies and data skew
     - Shuffle optimisation opportunities
     - Broadcast join usage and optimisation
     - Memory management and caching strategies
     - DataFrame operation efficiency
  3. Validate Medallion Architecture compliance:
     - Bronze layer: Raw data preservation patterns
     - Silver layer: Cleansing and standardization
     - Gold layer: Business model optimisation
  4. Check performance considerations:
     - Identify potential bottlenecks
     - Suggest optimisation opportunities
     - Validate cost-efficiency patterns
  5. Verify test coverage:
     - Check for pytest test files
     - Validate test completeness
     - Suggest missing test scenarios
  6. Review production readiness:
     - Error handling for data pipeline failures
     - Idempotent operation design
     - Monitoring and logging completeness

  Provide detailed findings in this format:

  ## PySpark Analysis Results

  ### Critical Issues (blocking)
  - [List any critical performance or correctness issues]

  ### Performance Optimisations
  - [Specific optimisation recommendations]

  ### Architecture Compliance
  - [Medallion architecture adherence assessment]

  ### Test Coverage
  - [Test completeness and gaps]

  ### Recommendations
  - [Specific actionable improvements]

  Return your analysis for integration into the PR review.
  "
```

**Integration of PySpark Analysis:**
- If pyspark-engineer identifies critical issues → Add to review comments
- If optimisations suggested → Add as optional improvement comments
- If architecture violations found → Add as required changes
- Include all findings in final review summary

### 4. Provide Review Comments
- Use `mcp__ado__repo_list_pull_request_threads` to check existing review comments
- If issues found, use `mcp__ado__repo_create_pull_request_thread` to add:
  - Specific file-level comments with line numbers
  - Clear description of issues
  - Suggested improvements
  - Mark as `Active` status if changes required

### 5. Approve and Complete PR (if satisfied)
**Only proceed if ALL criteria met:**
- No merge conflicts
- Code quality standards met
- PySpark best practices followed
- ETL patterns correct
- No DevOps concerns
- Proper error handling and logging
- Standards compliant
- **PySpark analysis (if performed) shows no critical issues**
- **Performance optimisations either implemented or deferred with justification**
- **Medallion architecture compliance validated**

**If approved:**
1. Use `mcp__ado__repo_update_pull_request` with:
   - Set `autoComplete: true`
   - Set `mergeStrategy: "NoFastForward"` (or "Squash" if many small commits)
   - Set `deleteSourceBranch: false` (preserve branch history)
   - Set `transitionWorkItems: true`
   - Add approval comment explaining what was reviewed

2. Confirm completion with summary:
   - PR ID and title
   - Number of commits reviewed
   - Key changes identified
   - Approval rationale

### 6. Report Results
Provide comprehensive summary:
- Total open PRs reviewed
- PRs approved and completed (with IDs)
- PRs requiring changes (with summary of issues)
- PRs blocked by merge conflicts
- **PySpark analysis findings (if performed)**
- **Performance optimisation recommendations**

## Important Notes
- **No deferrals**: All identified issues must be addressed before approval
- **Immediate action**: If improvements needed, request them now - no "future work" comments
- **Thorough review**: Check both code quality AND DevOps considerations
- **Professional objectivity**: Prioritize technical accuracy over validation
- **Merge conflicts**: Do NOT approve PRs with merge conflicts - report them for manual resolution
