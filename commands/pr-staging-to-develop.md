---
model: claude-haiku-4-5-20251001
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git diff:*), Bash(git log:*), Bash(git push:*), Bash(git pull:*), Bash(git branch:*), mcp__*, mcp__ado__repo_list_branches_by_repo, mcp__ado__repo_search_commits, mcp__ado__repo_create_pull_request, mcp__ado__repo_get_pull_request_by_id, mcp__ado__repo_get_repo_by_name_or_id, mcp__ado__wit_add_work_item_comment, mcp__ado__wit_get_work_item
argument-hint: [message] | --no-verify | --amend | --pr-s | --pr-d | --pr-m
# Create Remote PR: staging → develop
---
## Task
Create a pull request from remote `staging` branch to remote `develop` branch using Azure DevOps MCP tools.

## Instructions

### 1. Create PR
- Use `mcp__ado__repo_create_pull_request` tool
- Source: `refs/heads/staging` (remote only - do NOT push local branches)
- Target: `refs/heads/develop`
- Repository ID: `d3fa6f02-bfdf-428d-825c-7e7bd4e7f338`
- Title: Clear, concise description with conventional commit emoji
- Description: Brief bullet points summarising changes (keep short)

### 2. Check for Merge Conflicts
- Use `mcp__ado__repo_get_pull_request_by_id` to verify PR status
- If merge conflicts exist, resolve them:
  1. Create temporary branch from `origin/staging`
  2. Merge `origin/develop` into temp branch
  3. Resolve conflicts using Edit tool
  4. Commit resolution: `🔀 Merge origin/develop into staging - resolve conflicts for PR #XXXX`
  5. Push resolved merge to `origin/staging`
  6. Clean up temp branch

### 3. Success Criteria
- PR created successfully
- No merge conflicts preventing approval
- PR ready for reviewer approval

storageexplorer://v=1&accountid=%2Fsubscriptions%2F646e3673-7a99-4617-9f7e-47857fa18002%2FresourceGroups%2FAuE-Atlas-DataPlatform-DEV-RG%2Fproviders%2FMicrosoft.Storage%2FstorageAccounts%2Fauedatamigdevlake&subscriptionid=646e3673-7a99-4617-9f7e-47857fa18002&resourcetype=Azure.FileShare&resourcename=atldev01ndsdb1