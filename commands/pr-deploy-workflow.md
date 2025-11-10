---
model: claude-haiku-4-5-20251001
allowed-tools: SlashCommand, Bash(git:*), mcp__ado__repo_get_pull_request_by_id, mcp__ado__repo_list_pull_requests_by_repo_or_project
argument-hint: [commit-message]
description: Complete deployment workflow - commit, PR to staging, review, then staging to develop
---


# Complete Deployment Workflow

Automates the full deployment workflow with integrated PR review:
1. Commit feature changes and create PR to staging
2. Automatically review the PR for quality and standards
3. Fix any issues identified in review (with iteration loop)
4. After PR is approved and merged, create PR from staging to develop

## What This Does

1. Calls `/pr-feature-to-staging` to commit and create feature → staging PR
2. Calls `/pr-review` to automatically review the PR
3. If review identifies issues → calls `/pr-fix-pr-review` and loops back to review
4. If review passes → waits for user to merge staging PR
5. Calls `/pr-staging-to-develop` to create staging → develop PR

## Implementation Logic

### Step 1: Create Feature PR to Staging
Use `SlashCommand` tool to execute:
```
/pr-feature-to-staging $ARGUMENTS
```

**Expected Output:**
- PR URL and PR ID
- Work item comments added
- Source and target branches confirmed

**Extract from output:**
- PR ID (needed for review step)
- PR number (for user reference)

### Step 2: Automated PR Review
Use `SlashCommand` tool to execute:
```
/pr-review [PR_ID]
```

**The review will evaluate:**
- Code quality and maintainability
- PySpark best practices
- ETL pattern compliance
- Standards compliance from `.claude/rules/python_rules.md`
- DevOps considerations
- Merge conflicts

**Review Outcomes:**

#### Outcome A: Review Passes (PR Approved)
Review output will indicate:
- "PR approved and set to auto-complete"
- No active review comments requiring changes
- All quality gates passed

**Action:** Proceed to Step 4

#### Outcome B: Review Requires Changes
Review output will indicate:
- Active review comments with specific issues
- Quality standards not met
- Files requiring modifications

**Action:** Proceed to Step 3

### Step 3: Fix Review Issues (if needed)
**Only execute if Step 2 identified issues**

Use `SlashCommand` tool to execute:
```
/pr-fix-pr-review [PR_ID]
```

**This will:**
1. Retrieve all active review comments
2. Make code changes to address feedback
3. Run quality gates (syntax, lint, format)
4. Commit fixes and push to feature branch
5. Reply to review threads
6. Update the PR automatically

**After fixes are applied:**
- Loop back to Step 2 to re-review
- Continue iterating until review passes

**Iteration Logic:**
```
LOOP while review has active issues:
  1. /pr-fix-pr-review [PR_ID]
  2. /pr-review [PR_ID]
  3. Check review outcome
  4. If approved → exit loop
  5. If still has issues → continue loop
END LOOP
```

### Step 4: Wait for Staging PR Merge
After PR review passes and is approved, inform user:
```
✅ PR Review Passed - PR Approved and Ready

PR #[PR_ID] has been reviewed and approved with auto-complete enabled.

Review Summary:
- Code quality: ✓ Passed
- PySpark best practices: ✓ Passed
- ETL patterns: ✓ Passed
- Standards compliance: ✓ Passed
- No merge conflicts

Next Steps:
1. The PR will auto-merge when all policies are satisfied
2. Once merged to staging, I'll create the staging → develop PR

Would you like me to:
a) Create the staging → develop PR now (if staging merge is complete)
b) Wait for you to confirm the staging merge
c) Check the PR status

Enter choice (a/b/c):
```

**User Responses:**
- **a**: Immediately proceed to Step 5
- **b**: Wait for user confirmation, then proceed to Step 5
- **c**: Use `mcp__ado__repo_get_pull_request_by_id` to check if PR is merged, then guide user

### Step 5: Create Staging to Develop PR
Use `SlashCommand` tool to execute:
```
/pr-staging-to-develop
```

**This will:**
1. Create PR: staging → develop
2. Handle any merge conflicts
3. Return PR URL for tracking

**Final Output:**
```
🚀 Deployment Workflow Complete

Feature → Staging:
- PR #[PR_ID] - Reviewed and Merged ✓

Staging → Develop:
- PR #[NEW_PR_ID] - Created and Ready for Review
- URL: [PR_URL]

Summary:
1. Feature PR created and reviewed
2. All quality gates passed
3. PR approved and merged to staging
4. Staging PR created for develop

The workflow is complete. The staging → develop PR is now ready for final review and deployment.
```

## Example Usage

### Full Workflow with Work Item
```bash
/deploy-workflow "feat(gold): add X_MG_Offender linkage table #45497"
```

**This will:**
1. Create commit on feature branch
2. Create PR: feature → staging
3. Comment on work item #45497
4. Automatically review PR for quality
5. Fix any issues identified (with iteration)
6. Wait for staging PR merge
7. Create PR: staging → develop

### Full Workflow Without Work Item
```bash
/deploy-workflow "refactor: optimise session management"
```

**This will:**
1. Create commit on feature branch
2. Create PR: feature → staging
3. Automatically review PR
4. Fix any issues (iterative)
5. Wait for merge confirmation
6. Create staging → develop PR

## Review Iteration Example

**Scenario:** Review finds 3 issues in the initial PR

```
Step 1: /pr-feature-to-staging "feat: add new table"
  → PR #5678 created

Step 2: /pr-review 5678
  → Found 3 issues:
    - Missing type hints in function
    - Line exceeds 240 characters
    - Missing @synapse_error_print_handler decorator

Step 3: /pr-fix-pr-review 5678
  → Fixed all 3 issues
  → Committed and pushed
  → PR updated

Step 2 (again): /pr-review 5678
  → All issues resolved
  → PR approved ✓

Step 4: Wait for merge confirmation

Step 5: /pr-staging-to-develop
  → PR #5679 created (staging → develop)

Complete!
```

## Error Handling

### PR Creation Fails
- Display error from `/pr-feature-to-staging`
- Guide user to resolve (branch validation, git issues)
- Do not proceed to review step

### Review Cannot Complete
- Display specific blocker (merge conflicts, missing files)
- Guide user to manual resolution
- Offer to retry review after fix

### Fix PR Review Fails
- Display specific errors (quality gates, git issues)
- Offer manual intervention option
- Allow user to fix locally and skip to next step

### Staging PR Already Exists
- Use `mcp__ado__repo_list_pull_requests_by_repo_or_project` to check existing PRs
- Inform user of existing PR
- Ask if they want to create anyway or use existing

## Notes

- **Automated Review**: Quality gates are enforced automatically
- **Iterative Fixes**: Will loop through fix → review until approved
- **Semi-Automated Merge**: User must confirm staging merge before final PR
- **Work Item Tracking**: Automatic comments on linked work items
- **Quality First**: Won't proceed if review fails and can't auto-fix
- **Graceful Degradation**: Offers manual intervention at each step if automatisation fails

## Quality Gates Enforced

The integrated `/pr-review` checks:
1. Code quality (type hints, line length, formatting)
2. PySpark best practices (DataFrame ops, logging, session mgmt)
3. ETL pattern compliance (class structure, decorators)
4. Standards from `.claude/rules/python_rules.md`
5. No merge conflicts
6. Proper error handling

All must pass before proceeding to staging → develop PR.
