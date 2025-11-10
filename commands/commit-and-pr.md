---
allowed-tools: SlashCommand
argument-hint: [commit-message]
description: Shortcut to commit and create PR to staging (calls pr-feature-to-staging)
---

# Commit and PR to Staging (Shortcut)

This is a shortcut command that calls `/pr-feature-to-staging` with your commit message.

## What This Does

Simply passes all arguments to the `/pr-feature-to-staging` command.

## Implementation

Execute the following command with the provided arguments:

```
/pr-feature-to-staging $ARGUMENTS
```

Use the `SlashCommand` tool to invoke `/pr-feature-to-staging` with the user's message.

## Example Usage

```bash
/commit-and-pr "feat: add new feature #12345"
```

This is equivalent to:
```bash
/pr-feature-to-staging "feat: add new feature #12345"
```
