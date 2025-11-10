---
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, mcp__*
argument-hint: [doc-type] | --generate-local | --sync-to-wiki | --regenerate | --all | --validate
description: Generate documentation locally to ./docs/ then sync to Azure DevOps wiki (local-first workflow)
model: sonnet
---

# Data Pipeline Documentation - Local-First Workflow

Generate documentation locally in `./docs/` directory, then sync to Azure DevOps wiki: $ARGUMENTS

## Architecture: Local-First Documentation

```
Source Code → Generate Docs → ./docs/ (version controlled) → Sync to Wiki
```

**Benefits:**
- ✅ Documentation version controlled in git
- ✅ Review locally before wiki publish
- ✅ No regeneration needed for wiki sync
- ✅ Git diff shows doc changes
- ✅ Reusable across multiple targets (wiki, GitHub Pages, PDF)
- ✅ Offline access to documentation

## Repository Information

- Repository: unify_2_1_dm_synapse_env_d10
- Local docs: `./docs/` (mirrors repo structure)
- Wiki base: 'Unify 2.1 Data Migration Technical Documentation'/'Data Migration Pipeline'/unify_2_1_dm_synapse_env_d10/
- Exclusions: @.docsignore (similar to .gitignore)

## Documentation Workflows

### --generate-local: Generate Documentation Locally

Generate comprehensive documentation and save to `./docs/` directory.

#### Step 1: Scan Repository for Files

```bash
# Get all documentable files (exclude .docsignore patterns)
git ls-files "*.py" "*.yaml" "*.yml" "*.md" | grep -v -f <(git ls-files --ignored --exclude-standard --exclude-from=.docsignore)
```

**Target files:**
- Python files: `python_files/**/*.py`
- Configuration: `configuration.yaml`
- Existing markdown: `README.md` (validate/enhance)

**Exclude (from .docsignore):**
- `__pycache__/`, `*.pyc`, `.venv/`
- `.claude/`, `docs/`, `*.duckdb`
- See `.docsignore` for complete list

#### Step 2: Launch Code-Documenter Agent

Use Task tool to launch code-documenter agent:

```
Generate comprehensive documentation for repository files:

**Scope:**
- Target: All Python files in python_files/ (utilities, bronze, silver, gold, testing)
- Configuration files: configuration.yaml
- Exclude: Files matching .docsignore patterns

**Documentation Requirements:**
For Python files:
- File purpose and overview
- Architecture and design patterns (medallion, ETL, etc.)
- Class and function documentation
- Data flow explanations
- Business logic descriptions
- Dependencies and imports
- Usage examples
- Testing information
- Related Azure DevOps work items

For Configuration files:
- Configuration structure
- All configuration sections explained
- Environment variables
- Azure integration settings
- Usage examples

**Output Format:**
- Markdown format suitable for wiki
- File naming: source_file.py → docs/path/source_file.py.md
- Clear heading structure
- Code examples with syntax highlighting
- Cross-references to related files
- Professional, concise language
- NO attribution footers (e.g., "Documentation By: Claude Code")

**Output Location:**
Save all generated documentation to ./docs/ directory maintaining source structure:
- python_files/utilities/session_optimiser.py → docs/python_files/utilities/session_optimiser.py.md
- python_files/gold/g_address.py → docs/python_files/gold/g_address.py.md
- configuration.yaml → docs/configuration.yaml.md

**Directory Index Files:**
Generate README.md for each directory with:
- Directory purpose
- List of files with brief descriptions
- Architecture overview for layer directories
- Navigation links
```

#### Step 3: Generate Directory Index Files

Create `README.md` files for each directory:

**Root Index (docs/README.md):**
- Overall documentation structure
- Navigation to main sections
- Medallion architecture overview
- Link to wiki

**Layer Indexes:**
- `docs/python_files/README.md` - Pipeline overview
- `docs/python_files/utilities/README.md` - Core utilities index
- `docs/python_files/bronze/README.md` - Bronze layer overview
- `docs/python_files/silver/README.md` - Silver layer overview
  - `docs/python_files/silver/cms/README.md` - CMS tables index
  - `docs/python_files/silver/fvms/README.md` - FVMS tables index
  - `docs/python_files/silver/nicherms/README.md` - NicheRMS tables index
- `docs/python_files/gold/README.md` - Gold layer overview
- `docs/python_files/testing/README.md` - Testing documentation

#### Step 4: Validation

Verify generated documentation:
- All source files have corresponding .md files in ./docs/
- Directory structure matches source repository
- Index files (README.md) created for directories
- Markdown formatting is valid
- No files from .docsignore included
- Cross-references are valid

#### Step 5: Summary Report

Provide detailed report:
```markdown
## Documentation Generation Complete

### Files Documented:
- Python files: [count]
- Configuration files: [count]
- Total documentation files: [count]

### Directory Structure:
- Utilities: [file count]
- Bronze layer: [file count]
- Silver layer: [file count by database]
- Gold layer: [file count]
- Testing: [file count]

### Index Files Created:
- Root index: docs/README.md
- Layer indexes: [list]
- Database indexes: [list]

### Location:
All documentation saved to: ./docs/

### Next Steps:
1. Review generated documentation: `ls -R ./docs/`
2. Make any manual edits if needed
3. Commit to git: `git add docs/`
4. Sync to wiki: `/update-docs --sync-to-wiki`
```

---

### --sync-to-wiki: Sync Local Docs to Azure DevOps Wiki

Copy documentation from `./docs/` to Azure DevOps wiki (no regeneration).

#### Step 1: Scan Local Documentation

```bash
# Find all .md files in ./docs/
find ./docs -name "*.md" -type f
```

**Path Mapping Logic:**

Local path → Wiki path conversion:
```
./docs/python_files/utilities/session_optimiser.py.md
↓
Unify 2.1 Data Migration Technical Documentation/
  Data Migration Pipeline/
    unify_2_1_dm_synapse_env_d10/
      python_files/utilities/session_optimiser.py
```

**Mapping rules:**
1. Remove `./docs/` prefix
2. Remove `.md` extension (unless README.md → README)
3. Prepend wiki base path
4. Use forward slashes for wiki paths

#### Step 2: Read and Process Each Documentation File

For each `.md` file in `./docs/`:
1. Read markdown content
2. Extract metadata (if present)
3. Generate wiki path from local path
4. Prepare content for wiki format
5. Add footer with metadata:
   ```markdown
   ---
   **Metadata:**
   - Source: [file path in repo]
   - Last Updated: [date]
   - Related Work Items: [links if available]
   ```

#### Step 3: Create/Update Wiki Pages Using ADO MCP

Use Azure DevOps MCP to create or update each wiki page:

```bash
# For each documentation file:
# 1. Check if wiki page exists
# 2. Create new page if not exists
# 3. Update existing page if exists
# 4. Verify success

# Example for session_optimiser.py.md:
Local:  ./docs/python_files/utilities/session_optimiser.py.md
Wiki:   Unify 2.1 Data Migration Technical Documentation/Data Migration Pipeline/unify_2_1_dm_synapse_env_d10/python_files/utilities/session_optimiser.py
Action: Create/Update wiki page with content
```

**ADO MCP Operations:**
```python
# Pseudo-code for sync operation
for doc_file in find_all_docs():
    wiki_path = local_to_wiki_path(doc_file)
    content = read_file(doc_file)

    # Use MCP to create/update
    mcp__Azure_DevOps__create_or_update_wiki_page(
        path=wiki_path,
        content=content
    )
```

#### Step 4: Verification

After sync, verify:
- All .md files from ./docs/ have corresponding wiki pages
- Wiki path structure matches local structure
- Content is properly formatted in wiki
- No sync errors
- Wiki pages accessible in Azure DevOps

#### Step 5: Summary Report

Provide detailed sync report:
```markdown
## Wiki Sync Complete

### Pages Synced:
- Total pages: [count]
- Created new: [count]
- Updated existing: [count]

### By Directory:
- Utilities: [count] pages
- Bronze: [count] pages
- Silver: [count] pages
  - CMS: [count] pages
  - FVMS: [count] pages
  - NicheRMS: [count] pages
- Gold: [count] pages
- Testing: [count] pages

### Wiki Location:
Base: Unify 2.1 Data Migration Technical Documentation/Data Migration Pipeline/unify_2_1_dm_synapse_env_d10/

### Verification:
- All pages synced successfully: [✅/❌]
- Path structure correct: [✅/❌]
- Content formatting valid: [✅/❌]

### Errors:
[List any sync failures and reasons]

### Next Steps:
1. Verify pages in Azure DevOps wiki
2. Check navigation and cross-references
3. Share wiki URL with team
```

---

### --regenerate: Regenerate Specific File(s)

Update documentation for specific file(s) without full regeneration.

**Usage:**
```bash
# Single file
/update-docs --regenerate python_files/gold/g_address.py

# Multiple files
/update-docs --regenerate python_files/gold/g_address.py python_files/gold/g_cms_address.py

# Entire directory
/update-docs --regenerate python_files/utilities/
```

**Process:**
1. Launch code-documenter agent for specified file(s)
2. Generate updated documentation
3. Save to ./docs/ (overwrite existing)
4. Report files updated
5. Optionally sync to wiki

**Output:**
```markdown
## Documentation Regenerated

### Files Updated:
- python_files/gold/g_address.py → docs/python_files/gold/g_address.py.md

### Next Steps:
1. Review updated documentation
2. Commit changes: `git add docs/python_files/gold/g_address.py.md`
3. Sync to wiki: `/update-docs --sync-to-wiki --directory python_files/gold/`
```

---

### --all: Complete Workflow

Execute complete documentation workflow: generate local + sync to wiki.

**Process:**
1. Execute `--generate-local` workflow
2. Validate generated documentation
3. Execute `--sync-to-wiki` workflow
4. Provide comprehensive summary

**Use when:**
- Initial documentation setup
- Major refactoring or restructuring
- Adding new layers or modules
- Quarterly documentation refresh

---

### --validate: Documentation Validation

Validate documentation completeness and accuracy.

**Validation Checks:**

1. **Completeness:**
   - All source files have documentation
   - All directories have index files (README.md)
   - No missing cross-references

2. **Accuracy:**
   - Documented functions exist in source
   - Schema documentation matches actual tables
   - Configuration docs match configuration.yaml

3. **Quality:**
   - Valid markdown syntax
   - Proper heading structure
   - Code blocks properly formatted
   - No broken links

4. **Sync Status:**
   - ./docs/ files match wiki pages
   - No uncommitted documentation changes
   - Wiki pages up to date

**Validation Report:**
```markdown
## Documentation Validation Results

### Completeness: [✅/❌]
- Files without docs: [count]
- Missing index files: [count]
- Missing cross-references: [count]

### Accuracy: [✅/❌]
- Schema mismatches: [count]
- Outdated function docs: [count]
- Configuration drift: [count]

### Quality: [✅/❌]
- Markdown syntax errors: [count]
- Broken links: [count]
- Formatting issues: [count]

### Sync Status: [✅/❌]
- Out-of-sync files: [count]
- Uncommitted changes: [count]
- Wiki drift: [count]

### Actions Required:
[List of fixes needed]
```

---

## Optional Workflow Modifiers

### --layer: Target Specific Layer

Generate/sync documentation for specific layer only.

```bash
/update-docs --generate-local --layer utilities
/update-docs --generate-local --layer gold
/update-docs --sync-to-wiki --layer silver
```

### --directory: Target Specific Directory

Generate/sync documentation for specific directory.

```bash
/update-docs --generate-local --directory python_files/gold/
/update-docs --sync-to-wiki --directory python_files/utilities/
```

### --only-modified: Sync Only Changed Files

Sync only files modified since last sync (based on git status).

```bash
/update-docs --sync-to-wiki --only-modified
```

**Process:**
1. Check git status for modified .md files in ./docs/
2. Sync only those files to wiki
3. Faster than full sync

---

## Code-Documenter Agent Integration

### When to Use Code-Documenter Agent:

**Always use Task tool with subagent_type="code-documenter" for:**
1. **Initial documentation generation** (--generate-local)
2. **File regeneration** (--regenerate)
3. **Complex transformations** - ETL logic, medallion patterns
4. **Architecture documentation** - High-level system design

### Agent Invocation Pattern:

```markdown
Launch code-documenter agent with:
- Target files: [list of files or directories]
- Documentation scope: comprehensive documentation
- Focus areas: [medallion architecture | ETL logic | utilities | testing]
- Output format: Wiki-ready markdown
- Output location: ./docs/ (maintain source structure)
- Exclude patterns: Files from .docsignore
- Quality requirements: Professional, accurate, no attribution footers
```

---

## Path Mapping Reference

### Local to Wiki Path Conversion

**Function logic:**
```python
def local_to_wiki_path(local_path: str) -> str:
    """
    Convert local docs path to Azure DevOps wiki path

    Args:
        local_path: Path like ./docs/python_files/utilities/session_optimiser.py.md

    Returns:
        Wiki path like: Unify 2.1 Data Migration Technical Documentation/.../session_optimiser.py
    """
    # Remove ./docs/ prefix
    relative = local_path.replace('./docs/', '')

    # Handle README.md (keep as README)
    if relative.endswith('/README.md'):
        relative = relative  # Keep README.md
    elif relative.endswith('.md'):
        relative = relative[:-3]  # Remove .md extension

    # Build wiki path
    wiki_base = "Unify 2.1 Data Migration Technical Documentation/Data Migration Pipeline/unify_2_1_dm_synapse_env_d10"
    wiki_path = f"{wiki_base}/{relative}"

    return wiki_path
```

**Examples:**
```
./docs/README.md
→ Unify 2.1 Data Migration Technical Documentation/Data Migration Pipeline/unify_2_1_dm_synapse_env_d10/README

./docs/python_files/utilities/session_optimiser.py.md
→ Unify 2.1 Data Migration Technical Documentation/Data Migration Pipeline/unify_2_1_dm_synapse_env_d10/python_files/utilities/session_optimiser.py

./docs/python_files/gold/g_address.py.md
→ Unify 2.1 Data Migration Technical Documentation/Data Migration Pipeline/unify_2_1_dm_synapse_env_d10/python_files/gold/g_address.py

./docs/configuration.yaml.md
→ Unify 2.1 Data Migration Technical Documentation/Data Migration Pipeline/unify_2_1_dm_synapse_env_d10/configuration.yaml
```

---

## Azure DevOps MCP Commands

### Wiki Operations:

```bash
# Create wiki page
mcp__Azure_DevOps__create_wiki_page(
    path="Unify 2.1 Data Migration Technical Documentation/Data Migration Pipeline/unify_2_1_dm_synapse_env_d10/python_files/utilities/session_optimiser.py",
    content="[markdown content]"
)

# Update wiki page
mcp__Azure_DevOps__update_wiki_page(
    path="[wiki page path]",
    content="[updated markdown content]"
)

# List wiki pages in directory
mcp__Azure_DevOps__list_wiki_pages(
    path="Unify 2.1 Data Migration Technical Documentation/Data Migration Pipeline/unify_2_1_dm_synapse_env_d10/python_files/gold"
)

# Delete wiki page (cleanup)
mcp__Azure_DevOps__delete_wiki_page(
    path="[wiki page path]"
)
```

---

## Guidelines

### DO:
- ✅ Generate documentation locally first (./docs/)
- ✅ Review and edit documentation before wiki sync
- ✅ Commit documentation to git with code changes
- ✅ Use code-documenter agent for comprehensive docs
- ✅ Respect .docsignore patterns
- ✅ Maintain directory structure matching source repo
- ✅ Generate index files (README.md) for directories
- ✅ Use --only-modified for incremental wiki updates
- ✅ Validate documentation regularly
- ✅ Link to Azure DevOps work items in docs

### DO NOT:
- ❌ Generate documentation directly to wiki (bypass ./docs/)
- ❌ Skip local review before wiki publish
- ❌ Document files in .docsignore (__pycache__/, *.pyc, .env)
- ❌ Include attribution footers ("Documentation By: Claude Code")
- ❌ Duplicate documentation in multiple locations
- ❌ Create wiki pages without proper path structure
- ❌ Forget to update documentation when code changes
- ❌ Sync to wiki without validating locally first

---

## Documentation Quality Standards

### For Python Files:
- Clear file purpose and overview
- Architecture and design pattern explanations
- Class and function documentation with type hints
- Data flow diagrams for ETL transformations
- Business logic explanations
- Usage examples with code snippets
- Testing information and coverage
- Dependencies and related files
- Related Azure DevOps work items

### For Configuration Files:
- Section-by-section explanation
- Environment variable documentation
- Azure integration details
- Usage examples
- Valid value ranges and constraints

### For Index Files (README.md):
- Directory purpose and overview
- File listing with brief descriptions
- Architecture context (for layers)
- Navigation links to sub-sections
- Key concepts and patterns

### Markdown Quality:
- Clear heading hierarchy (H1 → H2 → H3)
- Code blocks with language specification
- Tables for structured data
- Cross-references using relative links
- No broken links
- Professional, concise language
- Valid markdown syntax

---

## Git Integration

### Commit Documentation with Code:

```bash
# Add both code and documentation
git add python_files/gold/g_address.py docs/python_files/gold/g_address.py.md
git commit -m "feat(gold): add g_address table with documentation"

# View documentation changes
git diff docs/

# Documentation visible in PR reviews
```

### Pre-commit Hook (Optional):

```bash
# Validate documentation before commit
# In .git/hooks/pre-commit:
/update-docs --validate
```

---

## Output Summary Template

After any workflow completion, provide:

### 1. Workflow Executed:
- Command: [command used]
- Scope: [what was processed]
- Duration: [time taken]

### 2. Documentation Generated/Updated:
- Files processed: [count and list]
- Location: ./docs/
- Size: [total documentation size]

### 3. Wiki Sync Results (if applicable):
- Pages created: [count]
- Pages updated: [count]
- Wiki path: [base path]
- Status: [success/partial/failed]

### 4. Validation Results:
- Completeness: [✅/❌]
- Accuracy: [✅/❌]
- Quality: [✅/❌]
- Issues found: [count and details]

### 5. Next Steps:
- Recommended actions
- Areas needing attention
- Suggested improvements
