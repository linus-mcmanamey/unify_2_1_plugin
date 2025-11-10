# ADO MCP Task Retrieval Prompt

Use the Azure DevOps MCP tools to retrieve all user stories and tasks assigned to me that are currently in "New", "Active", "Committed", or "Backlog" states. Create a comprehensive markdown document with the following structure:

## Query Parameters
- **Assigned To**: @Me
- **Work Item Types**: User Story, Task, Bug
- **States**: New, Active, Committed, Backlog
- **Include**: All active iterations and backlog

## Required Output Format

```markdown
# My Active Work Items

## Summary
- **Total Items**: {count}
- **By Type**: {breakdown by work item type}
- **By State**: {breakdown by state}
- **Last Updated**: {current date}

## Work Items

### {Work Item Type} - {ID}: {Title}
**URL** {URL to work item}
**Status**: {State} | **Priority**: {Priority} | **Effort**: {Story Points/Original Estimate}
**Iteration**: S{Iteration Path} | **Area**: {Area Path}

**Description Summary**: 
{Provide a 2-3 sentence summary of the description/acceptance criteria}

**Key Details**:
- **Created**: {Created Date}
- **Tags**: {Tags if any}
- **Parent**: {Parent work item if applicable}

**[View in ADO]({URL to work item})**

---
```

## Specific Requirements

1. **Summarize Descriptions**: For each work item, provide a concise 2-3 sentence summary of the description and acceptance criteria, focusing on the core objective and deliverables.

2. **Clickable URLs**: Ensure all Azure DevOps URLs are properly formatted as clickable markdown links. including the actual work item

3. **Sort Order**: Sort by Priority (High to Low), then by State (Active, Committed, New, Backlog), then by Story Points/Effort (High to Low).

4. **Data Validation**: If any work items have missing key fields (Priority, Effort, etc.), note this in the output.

5. **Additional Context**: Include any relevant comments from the last 7 days if present.

Execute this query and generate the markdown document with all my currently assigned work items.