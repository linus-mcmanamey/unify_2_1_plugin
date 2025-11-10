---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git diff:*), Bash(git log:*), Bash(git push:*), Bash(git pull:*), Bash(git branch:*), mcp__ado__repo_list_branches_by_repo, mcp__ado__repo_search_commits, mcp__ado__repo_create_pull_request, mcp__ado__repo_get_pull_request_by_id, mcp__ado__repo_get_repo_by_name_or_id, mcp__ado__wit_add_work_item_comment, mcp__ado__wit_get_work_item
argument-hint: [message] | --no-verify | --amend | --pr-s | --pr-d | --pr-m
description: Create well-formatted commits with conventional commit format and emoji, integrated with Azure DevOps
---

# Smart Git Commit with Azure DevOps Integration

Create well-formatted commit: $ARGUMENTS

## Repository Configuration
- **Project**: Program Unify
- **Repository ID**: e030ea00-2f85-4b19-88c3-05a864d7298d
- **Repository Name**: unify_2_1_dm_synapse_env_d10
- **Branch Structure**: `feature/* → staging → develop → main`
- **Main Branch**: main

## Implementation Logic for Claude

When processing this command, Claude should:

1. **Detect Repository**: Check if current repo is `unify_2_1_dm_synapse_env_d10`
   - Use `git remote -v` or check current directory path
   - Can also use `mcp__ado__repo_get_repo_by_name_or_id` to verify

2. **Parse Arguments**: Extract flags from `$ARGUMENTS`
   - **PR Flags**:
     - `--pr-s`: Set target = `staging`
     - `--pr-d`: Set target = `develop`
     - `--pr-m`: Set target = `main`
     - `--pr` (no suffix): ERROR if unify_2_1_dm_synapse_env_d10, else target = `develop`

3. **Validate Current Branch** (if PR flag provided):
   - Get current branch: `git branch --show-current`
   - For `--pr-s`: Require `feature/*` branch (reject `staging`, `develop`, `main`)
   - For `--pr-d`: Require `staging` branch exactly
   - For `--pr-m`: Require `develop` branch exactly
   - If validation fails: Show clear error and exit

4. **Execute Commit Workflow**:
   - Stage changes (`git add .` )
   - Create commit with emoji conventional format
   - Run pre-commit hooks (unless `--no-verify`)
   - Push to current branch

5. **Create Pull Request** (if PR flag):
   - Call `mcp__ado__repo_create_pull_request` with:
     - `repository_id`: e030ea00-2f85-4b19-88c3-05a864d7298d
     - `source_branch`: Current branch from step 3
     - `target_branch`: Target from step 2
     - `title`: Extract from commit message
     - `description`: Generate with summary and test plan
   - Return PR URL to user

6. **Add Work Item Comments Automatically** (if PR was created in step 5):
   - **Condition Check**: Only execute if:
     - A PR was created in step 5 (any `--pr-*` flag was used)
     - PR creation was successful and returned a PR ID
   - **Get Work Items from PR**:
     - Use `mcp__ado__repo_get_pull_request_by_id` with:
       - `repositoryId`: e030ea00-2f85-4b19-88c3-05a864d7298d
       - `pullRequestId`: PR ID from step 5
       - `includeWorkItemRefs`: true
     - Extract work item IDs from the PR response
     - If no work items found, log info message and skip to next step
   - **Add Comments to Each Work Item**:
     - For each work item ID extracted from PR:
       - Use `mcp__ado__wit_get_work_item` to verify work item exists
       - Generate comment with:
         - PR title and number
         - Commit message and SHA
         - File changes summary from `git diff --stat`
         - Link to PR in Azure DevOps
         - Link to commit in Azure DevOps
         - **IMPORTANT**: Do NOT include any footer text like "Automatically added by /local-commit command" or similar attribution
       - Call `mcp__ado__wit_add_work_item_comment` with:
         - `project`: "Program Unify"
         - `workItemId`: Current work item ID
         - `comment`: Generated comment with HTML formatting
         - `format`: "html"
     - Log success/failure for each work item
     - If ANY work item fails, warn but don't fail the commit

## Current Repository State

- Git status: !`git status --short`
- Current branch: !`git branch --show-current`
- Staged changes: !`git diff --cached --stat`
- Unstaged changes: !`git diff --stat`
- Recent commits: !`git log --oneline -5`

## What This Command Does

1. Analyzes current git status and changes
2. If no files staged, stages all modified files with `git add`
3. Reviews changes with `git diff`
4. Analyzes for multiple logical changes
5. For complex changes, suggests split commits
6. Creates commit with emoji conventional format
7. Automatically runs pre-commit hooks (ruff lint/format, trailing whitespace, etc.)
   - Pre-commit may modify files (auto-fixes)
   - If files are modified, they'll be re-staged automatically
   - Use `--no-verify` to skip hooks in emergencies only
8. **NEW**: With PR flags, creates Azure DevOps pull request after push
   - Uses `mcp__ado__repo_create_pull_request` to create PR
   - Automatically links work items if commit message contains work item IDs
   - **IMPORTANT Branch Flow Rules** (unify_2_1_dm_synapse_env_d10 ONLY):
     - `--pr-s`: Feature branch → `staging` (standard feature PR)
     - `--pr-d`: `staging` → `develop` (promote staging to develop)
     - `--pr-m`: `develop` → `main` (promote develop to production)
     - `--pr`: **NOT ALLOWED** - must specify `-s`, `-d`, or `-m` for this repository
   - **For OTHER repositories**: `--pr` creates PR to `develop` branch (legacy behavior)
9. **NEW**: Automatically adds comments to linked work items after PR creation
   - Retrieves work items linked to the PR using `mcp__ado__repo_get_pull_request_by_id`
   - Automatically adds comment to each linked work item with:
     - PR title and number
     - Commit message and SHA
     - Summary of file changes
     - Direct link to PR in Azure DevOps
     - Direct link to commit in Azure DevOps
     - **IMPORTANT**: No footer attribution text (e.g., "Automatically added by /local-commit command")
   - Validates work items exist before commenting
   - Continues even if some work items fail (warns only) 

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
- ⏪️ `revert`: Reverting changes
- 🚨 `fix`: Compiler/linter warnings
- 🔒️ `fix`: Security issues
- 🩹 `fix`: Simple non-critical fix
- 🚑️ `fix`: Critical hotfix
- 🎨 `style`: Code structure/format
- 🔥 `fix`: Remove code/files
- 📦️ `chore`: Dependencies
- 🌱 `chore`: Seed files
- 🧑‍💻 `chore`: Developer experience
- 🏷️ `feat`: Types
- 💬 `feat`: Text/literals
- 🌐 `feat`: i18n/l10n
- 💡 `feat`: Business logic
- 📱 `feat`: Responsive design
- 🚸 `feat`: UX improvements
- ♿️ `feat`: Accessibility
- 🗃️ `db`: Database changes
- 🚩 `feat`: Feature flags
- ⚰️ `refactor`: Remove dead code
- 🦺 `feat`: Validation

## Commit Strategy

### Single Commit (Default)
```bash
git add .
git commit -m "✨ feat: implement user auth"
```

### Multiple Commits (Complex Changes)
```bash
# Stage and commit separately
git add src/auth.py
git commit -m "✨ feat: add authentication module"

git add tests/test_auth.py
git commit -m "✅ test: add auth unit tests"

git add docs/auth.md
git commit -m "📝 docs: document auth API"

# Push all commits
git push
```

## Pre-Commit Hooks

Your project uses pre-commit with:
- **Ruff**: Linting with auto-fix + formatting
- **Standard hooks**: Trailing whitespace, AST check, YAML/JSON/TOML validation
- **Security**: Private key detection
- **Quality**: Debug statement detection, merge conflict check

**Important**: Pre-commit hooks will auto-fix issues and may modify your files. The commit process will:
1. Run pre-commit hooks
2. If hooks modify files, automatically re-stage them
3. Complete the commit with all fixes applied

## Command Options

- `--no-verify`: Skip pre-commit checks (emergency use only)
- `--amend`: Amend previous commit
- **`--pr-s`**: Create PR to `staging` branch (feature → staging)
- **`--pr-d`**: Create PR to `develop` branch (staging → develop)
- **`--pr-m`**: Create PR to `main` branch (develop → main)
- `--pr`: Legacy flag for other repositories (creates PR to `develop`)
  - **NOT ALLOWED** in unify_2_1_dm_synapse_env_d10 - must use `-s`, `-d`, or `-m`
- Default: Run all pre-commit hooks and create new commit
- **Automatic Work Item Comments**: When using any PR flag, work items linked to the PR will automatically receive comments with commit details (no footer attribution)

## Azure DevOps Integration Features

### Pull Request Workflow (PR Flags)
When using PR flags, the command will:
1. Commit changes locally
2. Push to remote branch
3. Validate repository and branch configuration:
   - **THIS repo (unify_2_1_dm_synapse_env_d10)**: Requires explicit flag (`--pr-s`, `--pr-d`, or `--pr-m`)
     - `--pr-s`: Current feature branch → `staging`
     - `--pr-d`: Must be on `staging` branch → `develop`
     - `--pr-m`: Must be on `develop` branch → `main`
     - `--pr` alone: **ERROR** - must specify target
   - **OTHER repos**: `--pr` creates PR to `develop` (all other flags ignored)
4. Use `mcp__ado__repo_create_pull_request` to create PR with:
   - **Title**: Extracted from commit message
   - **Description**: Full commit details with summary and test plan
   - **Source Branch**: Current branch
   - **Target Branch**: Determined by flag and repository
   - **Work Items**: Auto-linked from commit message (e.g., "fixes #12345")

### Viewing Commit History
You can view commit history using:
- `mcp__ado__repo_search_commits` - Search commits by branch, author, date range
- Traditional `git log` - For local history

### Branch Management
- `mcp__ado__repo_list_branches_by_repo` - View all Azure DevOps branches
- `git branch` - View local branches

## Branch Validation Rules (unify_2_1_dm_synapse_env_d10)

Before creating a PR, the command validates:

### --pr-s (Feature → Staging)
- ✅ **ALLOWED**: Any `feature/*` branch
- ❌ **BLOCKED**: `staging`, `develop`, `main` branches
- **Target**: `staging`

### --pr-d (Staging → Develop)
- ✅ **ALLOWED**: Only `staging` branch
- ❌ **BLOCKED**: All other branches (including `feature/*`)
- **Target**: `develop`

### --pr-m (Develop → Main)
- ✅ **ALLOWED**: Only `develop` branch
- ❌ **BLOCKED**: All other branches (including `staging`, `feature/*`)
- **Target**: `main`

### --pr (Legacy - NOT ALLOWED)
- ❌ **BLOCKED**: All branches in unify_2_1_dm_synapse_env_d10
- 💡 **Error Message**: "Must use --pr-s, --pr-d, or --pr-m for this repository"
- ✅ **ALLOWED**: All other repositories (targets `develop`)

## Best Practices

1. **Let pre-commit work** - Don't use `--no-verify` unless absolutely necessary
2. **Atomic commits** - One logical change per commit
3. **Descriptive messages** - Emoji + type + clear description
4. **Review before commit** - Always check `git diff`
5. **Clean history** - Split complex changes into multiple commits
6. **Trust the hooks** - They maintain code quality automatically
7. **Use correct PR flag** - `--pr-s` for features, `--pr-d` for staging promotion, `--pr-m` for production
8. **Link work items** - Reference Azure DevOps work items in commit messages (e.g., "#43815") to enable automatic PR linking
9. **Validate branch** - Ensure you're on the correct branch before using `--pr-d` or `--pr-m`
10. **Work item linking** - Work items linked to PRs will automatically receive comments with commit details
11. **Keep stakeholders informed** - Use PR flags to ensure work items are automatically updated with progress

## Example Workflows

### Simple Commit
```bash
/commit "fix: resolve enum import error"
```

### Commit with Work Item
```bash
/commit "feat: add enum imports for Synapse environment"
```

### Commit and Create PR (Feature to Staging)
```bash
/commit --pr-s "feat: refactor commit command with ADO MCP integration"
```
This will:
1. Create commit locally
2. Push to current branch
3. Create PR: `feature/xyz → staging`
4. Link work items automatically if mentioned in commit message

### Promote Staging to Develop
```bash
# First checkout staging branch
git checkout staging
git pull origin staging

# Then commit and create PR
/commit --pr-d "release: promote staging changes to develop"
```
This will:
1. Create commit on `staging` branch
2. Push to `staging`
3. Create PR: `staging → develop`

### Promote Develop to Main (Production)
```bash
# First checkout develop branch
git checkout develop
git pull origin develop

# Then commit and create PR
/commit --pr-m "release: promote develop to production"
```
This will:
1. Create commit on `develop` branch
2. Push to `develop`
3. Create PR: `develop → main`

### Error: Using --pr without suffix
```bash
/commit --pr "feat: some feature"
```
**Result**: ERROR - unify_2_1_dm_synapse_env_d10 requires explicit PR target (`--pr-s`, `--pr-d`, or `--pr-m`)

### Feature PR with Automatic Work Item Comments
```bash
# On feature/xyz branch
/commit --pr-s "feat(user-auth): implement OAuth2 authentication #12345"
```
This will:
1. Create commit on feature branch
2. Push to feature branch
3. Create PR: `feature/xyz → staging`
4. Link work item #12345 to the PR
5. Automatically add comment to work item #12345 with:
   - PR title and number
   - Commit message and SHA
   - File changes summary
   - Link to PR in Azure DevOps
   - Link to commit in Azure DevOps
   - (No footer attribution text)

### Staging to Develop PR with Multiple Work Items
```bash
# On staging branch
/commit --pr-d "release: promote staging to develop - fixes #12345, #67890"
```
This will:
1. Create commit on `staging` branch
2. Push to `staging`
3. Create PR: `staging → develop`
4. Link work items #12345 and #67890 to the PR
5. Automatically add comments to both work items with PR and commit details (without footer attribution)

**Note**: Work items are automatically detected from commit message and linked to PR. Comments are added automatically to all linked work items without any footer text.