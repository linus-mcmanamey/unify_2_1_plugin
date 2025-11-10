---
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, mcp__*
argument-hint: [test-type] | --test-local | --test-sync | --test-full | --cleanup
description: Test documentation generation locally to ./docs/TEST/ then sync to Azure wiki TEST/ (small subset)
model: sonnet
---

# Documentation Update Testing - Local-First Workflow

Test documentation functionality on a limited set of files using local-first approach: $ARGUMENTS

## Test Architecture

```
Source Code (5 files) → Generate Docs → ./docs/TEST/ → Sync to Wiki TEST/
```

**Safety Features:**
- Uses TEST/ subdirectory (no production impact)
- Tests on only 5 files (fast)
- Respects .docsignore patterns
- Easy cleanup after testing

## Test File Set

Using these files for testing:

1. **Utility files** (2):
   - `python_files/utilities/cms_enums.py`
   - `python_files/utilities/create_duckdb_database.py`

2. **Gold layer files** (2):
   - `python_files/gold/g_address.py`
   - `python_files/gold/g_cms_address.py`

3. **Configuration** (1):
   - `configuration.yaml`

**Total: 5 files for testing**

## Repository Information

- Repository: unify_2_1_dm_synapse_env_d10
- Local test docs: `./docs/TEST/` (isolated test directory)
- Wiki test path: 'Unify 2.1 Data Migration Technical Documentation'/'Data Migration Pipeline'/unify_2_1_dm_synapse_env_d10/TEST/
- Exclusions: @.docsignore

## Test Workflows

### --test-local: Generate Test Documentation Locally

Generate documentation for 5 test files and save to `./docs/TEST/` directory.

#### Step 1: Prepare Test Directory

```bash
# Create test directory structure
mkdir -p ./docs/TEST/python_files/{utilities,gold}
```

#### Step 2: Launch Code-Documenter Agent for Test Files

Use Task tool to launch code-documenter agent:

```
Generate comprehensive documentation for test files:

**Test Files:**
1. python_files/utilities/cms_enums.py
2. python_files/utilities/create_duckdb_database.py
3. python_files/gold/g_address.py
4. python_files/gold/g_cms_address.py
5. configuration.yaml

**Documentation Requirements:**
For Python files:
- File purpose and overview
- Architecture and design patterns
- Class/function documentation
- Data flow explanations (for ETL files)
- Business logic descriptions
- Dependencies and imports
- Usage examples
- Testing information
- Related work items (if applicable)

For Configuration files:
- Configuration structure
- Section explanations
- Environment variables
- Azure integration settings
- Usage examples

**Output Format:**
- Markdown format suitable for wiki
- File naming: source_file.py → docs/TEST/path/source_file.py.md
- Clear heading structure
- Code examples with syntax highlighting
- Cross-references to related files
- Professional, concise language
- NO attribution footers

**Output Location:**
Save to ./docs/TEST/ directory:
- python_files/utilities/cms_enums.py → docs/TEST/python_files/utilities/cms_enums.py.md
- python_files/utilities/create_duckdb_database.py → docs/TEST/python_files/utilities/create_duckdb_database.py.md
- python_files/gold/g_address.py → docs/TEST/python_files/gold/g_address.py.md
- python_files/gold/g_cms_address.py → docs/TEST/python_files/gold/g_cms_address.py.md
- configuration.yaml → docs/TEST/configuration.yaml.md

**Quality Focus:**
- Accurate technical details
- Clear explanations for maintainability
- Medallion architecture context (for ETL files)
- PySpark best practices
```

#### Step 3: Generate Test Index File

Create `./docs/TEST/README.md`:

```markdown
# Documentation Test Suite

This directory contains test documentation for 5 sample files to validate the documentation generation workflow.

## Test Files:

### Utilities (2 files)
- **cms_enums.py** - CMS enumeration definitions
- **create_duckdb_database.py** - DuckDB database creation utility

### Gold Layer (2 files)
- **g_address.py** - Gold layer address table
- **g_cms_address.py** - Gold layer CMS address table

### Configuration (1 file)
- **configuration.yaml** - Project configuration

## Purpose:
- Validate code-documenter agent output
- Test documentation quality and format
- Verify wiki sync workflow
- Ensure path mapping works correctly

## Test Status:
- Documentation generated: [timestamp]
- Files documented: 5
- Wiki synced: [yes/no]
- Test result: [pending/pass/fail]

## Cleanup:
Run `/update-docs-test --cleanup` to remove test documentation after review.
```

#### Step 4: Validation

Verify test documentation:
```bash
# Check files exist
ls -la ./docs/TEST/python_files/utilities/
ls -la ./docs/TEST/python_files/gold/
ls -la ./docs/TEST/

# Verify file count (should be 6: 5 docs + 1 README)
find ./docs/TEST -name "*.md" -type f | wc -l

# Preview one file
cat ./docs/TEST/python_files/utilities/cms_enums.py.md | head -50
```

**Validation Checklist:**
- [ ] All 5 source files have .md documentation
- [ ] README.md created
- [ ] Directory structure correct (python_files/utilities/, python_files/gold/)
- [ ] Markdown formatting valid
- [ ] No attribution footers
- [ ] Professional quality content

#### Step 5: Test Summary

Provide detailed report:
```markdown
## Test Documentation Generation Complete

### Files Documented:
- Utilities: 2 files
- Gold layer: 2 files
- Configuration: 1 file
- Total: 5 documentation files + 1 README

### Location:
All test documentation saved to: ./docs/TEST/

### File Sizes:
- cms_enums.py.md: [size]
- create_duckdb_database.py.md: [size]
- g_address.py.md: [size]
- g_cms_address.py.md: [size]
- configuration.yaml.md: [size]
- README.md: [size]

### Quality Check:
- Documentation completeness: [✅/❌]
- Markdown formatting: [✅/❌]
- Professional quality: [✅/❌]
- No attribution footers: [✅/❌]

### Next Steps:
1. Review generated documentation: `ls -R ./docs/TEST/`
2. Read sample files: `cat ./docs/TEST/python_files/utilities/cms_enums.py.md`
3. If satisfied, test wiki sync: `/update-docs-test --test-sync`
4. If issues, regenerate or manually edit
```

---

### --test-sync: Sync Test Docs to Azure DevOps Wiki

Copy test documentation from `./docs/TEST/` to Azure DevOps wiki TEST/ directory.

**Pre-requisites:**
- Test documentation generated (./docs/TEST/ exists)
- Azure DevOps MCP configured
- Wiki access permissions verified

#### Step 1: Scan Test Documentation

```bash
# Find all .md files in ./docs/TEST/
find ./docs/TEST -name "*.md" -type f
```

**Expected files (6 total):**
```
./docs/TEST/README.md
./docs/TEST/python_files/utilities/cms_enums.py.md
./docs/TEST/python_files/utilities/create_duckdb_database.py.md
./docs/TEST/python_files/gold/g_address.py.md
./docs/TEST/python_files/gold/g_cms_address.py.md
./docs/TEST/configuration.yaml.md
```

#### Step 2: Path Mapping for Test Files

Local test path → Wiki test path conversion:

**Mapping Examples:**
```
./docs/TEST/README.md
→ Unify 2.1 Data Migration Technical Documentation/Data Migration Pipeline/unify_2_1_dm_synapse_env_d10/TEST/README

./docs/TEST/python_files/utilities/cms_enums.py.md
→ Unify 2.1 Data Migration Technical Documentation/Data Migration Pipeline/unify_2_1_dm_synapse_env_d10/TEST/python_files/utilities/cms_enums.py

./docs/TEST/python_files/gold/g_address.py.md
→ Unify 2.1 Data Migration Technical Documentation/Data Migration Pipeline/unify_2_1_dm_synapse_env_d10/TEST/python_files/gold/g_address.py

./docs/TEST/configuration.yaml.md
→ Unify 2.1 Data Migration Technical Documentation/Data Migration Pipeline/unify_2_1_dm_synapse_env_d10/TEST/configuration.yaml
```

**Path Mapping Logic:**
```python
def test_local_to_wiki_path(local_path: str) -> str:
    """Convert test docs path to wiki path"""
    # Remove ./docs/ prefix
    relative = local_path.replace('./docs/', '')

    # Remove .md extension (keep README.md as README)
    if relative.endswith('/README.md'):
        relative = relative.replace('.md', '')
    elif relative.endswith('.md'):
        relative = relative[:-3]

    # Build wiki path with TEST prefix
    wiki_base = "Unify 2.1 Data Migration Technical Documentation/Data Migration Pipeline/unify_2_1_dm_synapse_env_d10"
    wiki_path = f"{wiki_base}/{relative}"

    return wiki_path
```

#### Step 3: Create Wiki Pages Using ADO MCP

For each test documentation file:

**File 1: README.md**
```python
Local:  ./docs/TEST/README.md
Wiki:   ...unify_2_1_dm_synapse_env_d10/TEST/README
Content: [read from file]
Action: Create wiki page
```

**File 2: cms_enums.py.md**
```python
Local:  ./docs/TEST/python_files/utilities/cms_enums.py.md
Wiki:   ...unify_2_1_dm_synapse_env_d10/TEST/python_files/utilities/cms_enums.py
Content: [read from file]
Action: Create wiki page
```

**File 3-6: Remaining files** (similar process)

#### Step 4: Verification

After sync, verify in Azure DevOps:

**Manual Verification Steps:**
1. Go to Azure DevOps > Program Unify > Wiki
2. Navigate to: "Unify 2.1 Data Migration Technical Documentation"
3. Find: "Data Migration Pipeline/unify_2_1_dm_synapse_env_d10/TEST/"
4. Verify structure:
   ```
   TEST/
   ├── README
   ├── python_files/
   │   ├── utilities/
   │   │   ├── cms_enums.py
   │   │   └── create_duckdb_database.py
   │   └── gold/
   │       ├── g_address.py
   │       └── g_cms_address.py
   └── configuration.yaml
   ```
5. Open each page and verify content formatting
6. Check code blocks render correctly
7. Verify headings and structure

**Automated Verification:**
```bash
# List wiki pages in TEST directory
mcp__Azure_DevOps__list_wiki_pages(
    path="Unify 2.1 Data Migration Technical Documentation/Data Migration Pipeline/unify_2_1_dm_synapse_env_d10/TEST"
)

# Should return 6 pages
```

#### Step 5: Test Sync Summary

Provide detailed sync report:
```markdown
## Test Wiki Sync Complete

### Pages Synced:
- Total pages: 6
- Created new: [count]
- Updated existing: [count]

### By Category:
- Index: 1 page (README)
- Utilities: 2 pages
- Gold layer: 2 pages
- Configuration: 1 page

### Wiki Location:
Base: Unify 2.1 Data Migration Technical Documentation/Data Migration Pipeline/unify_2_1_dm_synapse_env_d10/TEST/

### Path Structure:
✅ TEST/README
✅ TEST/python_files/utilities/cms_enums.py
✅ TEST/python_files/utilities/create_duckdb_database.py
✅ TEST/python_files/gold/g_address.py
✅ TEST/python_files/gold/g_cms_address.py
✅ TEST/configuration.yaml

### Verification:
- All 6 pages synced: [✅/❌]
- Path structure correct: [✅/❌]
- Content formatting valid: [✅/❌]
- Accessible in Azure DevOps: [✅/❌]

### Errors:
[List any sync failures]

### Next Steps:
1. **Manually verify** pages in Azure DevOps wiki
2. **Check quality** of content and formatting
3. **If satisfied**, proceed with full deployment: `/update-docs --all`
4. **Cleanup test pages**: `/update-docs-test --cleanup`

### Azure DevOps URL:
[Provide link to TEST wiki pages]
```

---

### --test-full: Complete Test Workflow

Execute complete test workflow: generate local test docs + sync to wiki TEST/.

#### Execution Flow:

**Phase 1: Local Documentation Generation**
1. Execute `--test-local` workflow
2. Generate docs for 5 test files
3. Save to ./docs/TEST/
4. Validate generation

**Phase 2: Review (Optional Pause)**
```markdown
Test documentation generated successfully.

Location: ./docs/TEST/

Would you like to:
1. Review documentation before wiki sync
2. Continue with wiki sync immediately
3. Abort test
```

**Phase 3: Wiki Synchronization**
1. Execute `--test-sync` workflow
2. Sync all test docs to wiki TEST/
3. Verify wiki pages created

**Phase 4: Validation**
1. Verify all 6 pages exist in wiki
2. Check path structure correct
3. Validate content formatting
4. Generate comprehensive test report

**Phase 5: Cleanup Decision**
```markdown
Test completed successfully!

Test results:
- Local docs: ./docs/TEST/ (6 files)
- Wiki pages: 6 pages in TEST/ directory

Would you like to:
1. Keep test docs for review (manual cleanup later)
2. Clean up test docs now (delete local + wiki)
3. Keep local docs but remove wiki pages
4. Move test docs to production (not recommended)
```

---

### --cleanup: Clean Up Test Documentation

Remove test documentation from local filesystem and Azure DevOps wiki.

#### Step 1: Confirm Cleanup

```markdown
This will delete:
- Local: ./docs/TEST/ directory (6 files)
- Wiki: All pages under TEST/ directory (6 pages)

Are you sure you want to proceed? [yes/no]
```

#### Step 2: Delete Local Test Documentation

```bash
# Remove local test directory
rm -rf ./docs/TEST/

# Verify deletion
ls ./docs/TEST/ 2>&1 | grep "No such file"
```

#### Step 3: Delete Wiki Test Pages

Use ADO MCP to delete all wiki pages in TEST/:

```python
# Get list of test wiki pages
test_pages = [
    "...TEST/README",
    "...TEST/python_files/utilities/cms_enums.py",
    "...TEST/python_files/utilities/create_duckdb_database.py",
    "...TEST/python_files/gold/g_address.py",
    "...TEST/python_files/gold/g_cms_address.py",
    "...TEST/configuration.yaml"
]

# Delete each page
for page_path in test_pages:
    mcp__Azure_DevOps__delete_wiki_page(path=page_path)
```

#### Step 4: Verification

Verify cleanup completed:
```bash
# Verify local directory deleted
test ! -d ./docs/TEST/ && echo "✅ Local test docs deleted"

# Verify wiki pages deleted (should return 0 pages)
mcp__Azure_DevOps__list_wiki_pages(
    path="...unify_2_1_dm_synapse_env_d10/TEST"
)
```

#### Step 5: Cleanup Summary

```markdown
## Test Cleanup Complete

### Local Cleanup:
- Deleted: ./docs/TEST/ directory
- Files removed: 6
- Status: [✅/❌]

### Wiki Cleanup:
- Pages deleted: 6
- TEST/ directory removed: [✅/❌]
- Status: [✅/❌]

### Verification:
- Local test docs removed: [✅/❌]
- Wiki test pages removed: [✅/❌]
- No residual test files: [✅/❌]

### Result:
Test environment cleaned successfully. Ready for next test or production deployment.

### Next Steps:
If test was successful, proceed with production:
`/update-docs --generate-local` (full repository)
`/update-docs --sync-to-wiki` (sync to production wiki)
```

---

## Validation Checklist

Use after running any test workflow:

### Documentation Generation Quality:
- [ ] All 5 source files have .md documentation
- [ ] README.md created
- [ ] Directory structure correct
- [ ] Markdown formatting valid
- [ ] Code blocks properly formatted
- [ ] Headings clear and hierarchical
- [ ] No attribution footers
- [ ] Professional quality
- [ ] Accurate technical content
- [ ] Cross-references work

### Wiki Sync Quality:
- [ ] All 6 pages created in wiki
- [ ] Path structure matches local
- [ ] TEST/ directory isolated from production
- [ ] Content renders correctly in wiki
- [ ] Code syntax highlighting works
- [ ] Links and cross-references work
- [ ] No sync errors
- [ ] Pages accessible in Azure DevOps

### Path Mapping:
- [ ] Local paths correctly mapped to wiki paths
- [ ] TEST/ prefix maintained
- [ ] .md extensions removed correctly
- [ ] Directory structure preserved
- [ ] README.md handled correctly

### Error Handling:
- [ ] No unhandled exceptions
- [ ] Clear error messages
- [ ] Graceful failure recovery
- [ ] Rollback capability if needed

---

## Troubleshooting

### If documentation generation fails:
```bash
# Check files exist
ls -la python_files/utilities/cms_enums.py
ls -la python_files/gold/g_address.py

# Check for syntax errors
python3 -m py_compile python_files/utilities/cms_enums.py

# Check code-documenter agent availability
# Try with single file first
```

### If wiki sync fails:
```bash
# Verify ADO MCP connection
echo $AZURE_DEVOPS_PAT
echo $AZURE_DEVOPS_ORGANIZATION

# Check MCP server status
claude mcp list

# Test simple wiki operation
# Create single test page manually
```

### If path mapping is wrong:
```bash
# Verify local file exists
ls -la ./docs/TEST/python_files/utilities/cms_enums.py.md

# Check path conversion logic
# Ensure TEST/ prefix included
# Verify wiki base path correct
```

### If cleanup fails:
```bash
# Manual local cleanup
rm -rf ./docs/TEST/

# Manual wiki cleanup (via Azure DevOps UI)
# Navigate to wiki and delete TEST/ directory
```

---

## Test Results Template

After test completion, provide comprehensive results:

### Test Execution Summary:

**Test Type:** [--test-local | --test-sync | --test-full]

**Files Tested:** 5
1. python_files/utilities/cms_enums.py
2. python_files/utilities/create_duckdb_database.py
3. python_files/gold/g_address.py
4. python_files/gold/g_cms_address.py
5. configuration.yaml

**Test Results:**

1. **Documentation Generation:**
   - Status: [✅ Pass / ❌ Fail]
   - Files generated: [count]/6
   - Location: ./docs/TEST/
   - Quality: [Excellent / Good / Needs Improvement]
   - Issues: [list any issues]

2. **Wiki Synchronization:**
   - Status: [✅ Pass / ❌ Fail]
   - Pages synced: [count]/6
   - Wiki path: ...unify_2_1_dm_synapse_env_d10/TEST/
   - Formatting: [✅ Correct / ❌ Issues]
   - Errors: [list any errors]

3. **Path Mapping:**
   - Status: [✅ Pass / ❌ Fail]
   - Mapping accuracy: [100% / <100%]
   - Structure preserved: [✅ Yes / ❌ No]

4. **Overall Test Result:**
   - Result: [✅ PASS / ❌ FAIL]
   - Ready for production: [✅ Yes / ❌ No]
   - Confidence level: [High / Medium / Low]

**Recommendations:**
[List recommendations based on test results]

**Next Steps:**
[Specific actions to take based on test outcome]

---

## Documentation Standards

### Footer Guidelines:
- ❌ DO NOT include "Documentation By: Claude Code (Anthropic)" or similar attribution footers
- ✅ DO include: Source file, last updated, related work items
- ✅ Keep footers minimal and professional

### Content Quality:
- Technical accuracy over verbosity
- Clear, concise explanations
- Practical examples and usage
- Proper markdown formatting
- Professional tone

### File Naming:
- Maintain source file name with .md extension
- Examples:
  - `cms_enums.py` → `cms_enums.py.md`
  - `configuration.yaml` → `configuration.yaml.md`
  - Directory index → `README.md`
