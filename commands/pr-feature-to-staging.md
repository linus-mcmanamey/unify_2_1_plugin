---
model: claude-haiku-4-5-20251001
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git diff:*), Bash(git log:*), Bash(git push:*), Bash(git pull:*), Bash(git branch:*), mcp__*, mcp__ado__repo_list_branches_by_repo, mcp__ado__repo_search_commits, mcp__ado__repo_create_pull_request, mcp__ado__repo_get_pull_request_by_id, mcp__ado__repo_get_repo_by_name_or_id, mcp__ado__wit_add_work_item_comment, mcp__ado__wit_get_work_item, Read, Glob
argument-hint:
description: Automatically analyze changes and create PR from current feature branch to staging
---

# Create Feature PR to Staging

Automatically analyzes repository changes, generates appropriate commit message, and creates pull request to `staging`.

## Repository Configuration
- **Project**: Program Unify
- **Repository ID**: e030ea00-2f85-4b19-88c3-05a864d7298d
- **Repository Name**: unify_2_1_dm_synapse_env_d10
- **Target Branch**: `staging` (fixed)
- **Source Branch**: Current feature branch

## Current Repository State

- Git status: !`git status --short`
- Current branch: !`git branch --show-current`
- Staged changes: !`git diff --cached --stat`
- Unstaged changes: !`git diff --stat`
- Recent commits: !`git log --oneline -5`

## Implementation Logic

### 1. Validate Current Branch
- Get current branch: `git branch --show-current`
- **REQUIRE**: Branch must start with `feature/`
- **BLOCK**: `staging`, `develop`, `main` branches
- If validation fails: Show clear error and exit

### 2. Analyze Changes and Generate Commit Message
- Run `git status --short` to see modified files
- Run `git diff --stat` to see change statistics
- Run `git diff` to analyze actual code changes
- **Automatically determine**:
  - **Type**: Based on file changes (feat, fix, refactor, docs, test, chore, etc.)
  - **Scope**: From file paths (bronze, silver, gold, utilities, pipeline, etc.)
  - **Description**: Concise summary of what changed (e.g., "add person address table", "fix deduplication logic")
  - **Work Items**: Extract from branch name pattern (e.g., feature/46225-description → #46225)
- **Analysis Rules**:
  - New files in gold/silver/bronze → `feat`
  - Modified transformation logic → `refactor` or `fix`
  - Test files → `test`
  - Documentation → `docs`
  - Utilities/session_optimiser → `refactor` or `feat`
  - Multiple file types → prioritize feat > fix > refactor
  - Gold layer → scope: `(gold)`
  - Silver layer → scope: `(silver)` or `(silver_<database>)`
  - Bronze layer → scope: `(bronze)`
- Generate commit message in format: `emoji type(scope): description #workitem`

### 3. Execute Commit Workflow
- Stage all changes: `git add .`
- Create commit with auto-generated emoji conventional format
- Run pre-commit hooks (ruff lint/format, YAML validation, etc.)
- Push to current feature branch

### 4. Create Pull Request
- Use `mcp__ado__repo_create_pull_request` with:
  - `repositoryId`: e030ea00-2f85-4b19-88c3-05a864d7298d
  - `sourceRefName`: Current feature branch (refs/heads/feature/*)
  - `targetRefName`: refs/heads/staging
  - `title`: Extract from auto-generated commit message
  - `description`: Brief summary with bullet points based on analyzed changes
- Return PR URL to user

### 5. Add Work Item Comments (Automatic)
If PR creation was successful:
- Get work items linked to PR using `mcp__ado__repo_get_pull_request_by_id`
- For each linked work item:
  - Verify work item exists with `mcp__ado__wit_get_work_item`
  - Generate comment with:
    - PR title and number
    - Commit message and SHA
    - File changes summary from `git diff --stat`
    - Link to PR in Azure DevOps
    - Link to commit in Azure DevOps
  - Add comment using `mcp__ado__wit_add_work_item_comment`
  - Use HTML format for rich formatting
- **IMPORTANT**: Do NOT include footer attribution text
- **IMPORTANT**: always use australian english in all messages and descriptions
- **IMPORTANT**: do not mention that you are using australian english in all messages and descriptions

## Commit Message Format

### Type + Emoji Mapping
- ✨ `feat`: New feature
- 🐛 `fix`: Bug fix
- 📝 `docs`: Documentation
- 💄 `style`: Formatting/style
- ♻️ `refactor`: Code refactoring
- ⚡️ `perf`: Performance improvements
- ✅ `test`: Tests
- 🔧 `chore`: Tooling, configuration
- 🚀 `ci`: CI/CD improvements
- 🗃️ `db`: Database changes
- 🔥 `fix`: Remove code/files
- 📦️ `chore`: Dependencies
- 🚸 `feat`: UX improvements
- 🦺 `feat`: Validation

### Example Format
```
✨ feat(gold): add X_MG_Offender linkage table #45497
```

### Auto-Generation Logic

**File Path Analysis**:
- `python_files/gold/*.py` → scope: `(gold)`
- `python_files/silver/s_fvms_*.py` → scope: `(silver_fvms)` or `(silver)`
- `python_files/silver/s_cms_*.py` → scope: `(silver_cms)` or `(silver)`
- `python_files/bronze/*.py` → scope: `(bronze)`
- `python_files/utilities/*.py` → scope: `(utilities)`
- `python_files/pipeline_operations/*.py` → scope: `(pipeline)`
- `python_files/testing/*.py` → scope: `(test)`
- `.claude/**`, `*.md` → scope: `(docs)`

**Change Type Detection**:
- New files (`A` in git status) → `feat` ✨
- Modified transformation/ETL files → `refactor` ♻️
- Bug fixes (keywords: fix, bug, error, issue) → `fix` 🐛
- Test files → `test` ✅
- Documentation files → `docs` 📝
- Configuration files → `chore` 🔧

**Description Generation**:
- Extract meaningful operation from file names and diffs
- New table: "add <table_name> table"
- Modified logic: "improve/update <functionality>"
- Bug fix: "fix <issue_description>"
- Refactor: "refactor <component> for <reason>"

**Work Item Extraction**:
- Branch name pattern: `feature/<number>-description` → `#<number>`
- Multiple numbers: Extract first occurrence
- No number in branch: No work item reference added

## What This Command Does

1. Validates you're on a feature branch (feature/*)
2. Analyzes git changes to determine type, scope, and description
3. Extracts work item numbers from branch name
4. Auto-generates commit message with conventional emoji format
5. Stages all modified files
6. Creates commit with auto-generated message
7. Runs pre-commit hooks (auto-fixes code quality issues)
8. Pushes to current feature branch
9. Creates PR from feature branch → staging
10. Automatically adds comments to linked work items with PR details

## Pre-Commit Hooks

Your project uses pre-commit with:
- **Ruff**: Linting with auto-fix + formatting
- **Standard hooks**: Trailing whitespace, YAML/JSON validation
- **Security**: Private key detection

Pre-commit hooks will auto-fix issues and may modify files. The commit process will:
1. Run hooks
2. Auto-stage modified files
3. Complete commit with fixes applied

## Example Usage

### Automatic Feature PR
```bash
/pr-feature-to-staging
```
**On branch**: `feature/46225-add-person-address-table`
**Changed files**: `python_files/gold/g_occ_person_address.py` (new file)

**Auto-generated commit**: `✨ feat(gold): add person address table #46225`

This will:
1. Analyze changes (new gold layer file)
2. Extract work item #46225 from branch name
3. Auto-generate commit message
4. Commit and push to feature branch
5. Create PR: `feature/46225-add-person-address-table → staging`
6. Link work item #46225
7. Add automatic comment to work item #46225 with PR details

### Multiple File Changes
**On branch**: `feature/46789-refactor-deduplication`
**Changed files**:
- `python_files/silver/s_fvms_incident.py` (modified)
- `python_files/silver/s_cms_offence_report.py` (modified)
- `python_files/utilities/session_optimiser.py` (modified)

**Auto-generated commit**: `♻️ refactor(silver): improve deduplication logic #46789`

### Fix Bug
**On branch**: `feature/47123-fix-timestamp-parsing`
**Changed files**: `python_files/utilities/session_optimiser.py` (modified, TableUtilities.clean_date_time_columns)

**Auto-generated commit**: `🐛 fix(utilities): correct timestamp parsing for null values #47123`

## Error Handling

### Not on Feature Branch
```bash
# Error: On staging branch
/pr-feature-to-staging
```
**Result**: ERROR - Must be on feature/* branch. Current: staging

### Invalid Branch
```bash
# Error: On develop or main branch
/pr-feature-to-staging
```
**Result**: ERROR - Cannot create feature PR from develop/main branch

### No Changes to Commit
```bash
# Error: Working directory clean
/pr-feature-to-staging
```
**Result**: ERROR - No changes to commit. Working directory is clean.

## Best Practices

1. **Work on feature branches** - Always create PRs from `feature/*` branches
2. **Include work item in branch name** - Use pattern `feature/<work-item>-description` (e.g., `feature/46225-add-person-address`)
3. **Make focused changes** - Keep changes related to a single feature/fix for accurate commit message generation
4. **Let pre-commit work** - Hooks maintain code quality automatically
5. **Review changes** - Check `git status` before running command to ensure only intended files are modified
6. **Trust the automation** - The command analyzes your changes and generates appropriate conventional commit messages
