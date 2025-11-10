# PySpark Error Fixing Command

## Objective
Execute `make gold_table` and systematically fix all errors encountered in the PySpark gold layer file using specialized agents. Errors may be code-based (syntax, type, runtime) or logical (incorrect joins, missing data, business rule violations).

## Agent Workflow (MANDATORY)

### Phase 1: Error Fixing with pyspark-engineer
**CRITICAL**: All PySpark error fixing MUST be performed by the `pyspark-engineer` agent. Do NOT attempt to fix errors directly.

1. Launch the `pyspark-engineer` agent with:
   - Full error stack trace and context
   - Target file path
   - All relevant schema information from MCP server
   - Data dictionary references

2. The pyspark-engineer will:
   - Validate MCP server connectivity
   - Query schemas and foreign key relationships
   - Analyze and fix all errors systematically
   - Apply fixes following project coding standards
   - Run quality gates (py_compile, ruff check, ruff format)

### Phase 2: Code Review with code-reviewer
**CRITICAL**: After pyspark-engineer completes fixes, MUST launch the `code-reviewer` agent.

1. Launch the `code-reviewer` agent with:
   - Path to the fixed file(s)
   - Context: "PySpark gold layer error fixes"
   - Request comprehensive review focusing on:
     - PySpark best practices
     - Join logic correctness
     - Schema alignment
     - Business rule implementation
     - Code quality and standards adherence

2. The code-reviewer will provide:
   - Detailed feedback on all issues found
   - Security vulnerabilities
   - Performance optimization opportunities
   - Code quality improvements needed

### Phase 3: Iterative Refinement (MANDATORY LOOP)
**CRITICAL**: The review-refactor cycle MUST continue until code-reviewer is 100% satisfied.

1. If code-reviewer identifies ANY issues:
   - Launch pyspark-engineer again with code-reviewer's feedback
   - pyspark-engineer implements all recommended changes
   - Launch code-reviewer again to re-validate

2. Repeat Phase 1 → Phase 2 → Phase 3 until:
   - code-reviewer explicitly states: "✓ 100% SATISFIED - No further changes required"
   - Zero issues, warnings, or concerns remain
   - All quality gates pass
   - All business rules validated

3. Only then is the error fixing task complete.

**DO NOT PROCEED TO COMPLETION** until code-reviewer gives explicit 100% satisfaction confirmation.

## Pre-Execution Requirements

### 1. Python Coding Standards (CRITICAL - READ FIRST)
**MANDATORY**: All code MUST follow `.claude/rules/python_rules.md` standards:
- **Line 19**: Use DataFrame API not Spark SQL
- **Line 20**: Do NOT use DataFrame aliases (e.g., `.alias("l")`) or `col()` function - use direct string references or `df["column"]` syntax
- **Line 8**: Limit line length to 240 characters
- **Line 9-10**: Single line per statement, no carriage returns mid-statement
- **Line 10, 12**: No blank lines inside functions
- **Line 11**: Close parentheses on the last line of code
- **Line 5**: Use type hints for all function parameters and return values
- **Line 18**: Import statements only at the start of file, never inside functions
- **Line 16**: Run `ruff check` and `ruff format` before finalizing
- Import only necessary PySpark functions: `from pyspark.sql.functions import when, coalesce, lit` (NO col() usage - use direct references instead)

### 2. Identify Target File
- Default target: `python_files/gold/<INSERT FILE NAME>.py`
- Override via Makefile: `G_RUN_FILE_NAME` variable (line 63)
- Verify file exists before execution

### 3. Environment Context
- **Runtime Environment**: Local development (not Azure Synapse)
- **Working Directory**: `/workspaces/unify_2_1_dm_synapse_env_d10`
- **Python Version**: 3.11+
- **Spark Mode**: Local cluster (`local[*]`)
- **Data Location**: `/workspaces/data` (parquet files)

### 4. Available Resources
- **Data Dictionary**: `.claude/data_dictionary/*.md` - schema definitions for all CMS, FVMS, NicheRMS tables
- **Configuration**: `configuration.yaml` - database lists, null replacements, Azure settings
- **MCP Schema Server**: `mcp-server-motherduck` - live schema access via MCP (REQUIRED for schema verification)
- **Utilities Module**: `python_files/utilities/session_optimiser.py` - TableUtilities, NotebookLogger, decorators
- **Example Files**: Other `python_files/gold/g_*.py` files for reference patterns

### 5. MCP Server Validation (CRITICAL)
**BEFORE PROCEEDING**, verify MCP server connectivity:

1. **Test MCP Server Connection**:
   - Attempt to query any known table schema via MCP
   - Example test: Query schema for a common table (e.g., `silver_cms.s_cms_offence_report`)

2. **Validation Criteria**:
   - MCP server must respond with valid schema data
   - Schema must include column names, data types, and nullability
   - Response must be recent (not cached/stale data)

3. **Failure Handling**:
   ```
   ⚠️  STOP: MCP Server Not Available

   The MCP server (mcp-server-motherduck) is not responding or not providing valid schema data.

   This command requires live schema access to:
   - Verify column names and data types
   - Validate join key compatibility
   - Check foreign key relationships
   - Ensure accurate schema matching

   Actions Required:
   1. Check MCP server status and configuration
   2. Verify MotherDuck connection credentials
   3. Ensure schema database is accessible
   4. Restart MCP server if necessary

   Cannot proceed with error fixing without verified schema access.
   Use data dictionary files as fallback, but warn user of potential schema drift.
   ```

4. **Success Confirmation**:
   ```
   ✓ MCP Server Connected
   ✓ Schema data available
   ✓ Proceeding with error fixing workflow
   ```

## Error Detection Strategy

### Phase 1: Execute and Capture Errors
1. Run: `make gold_table`
2. Capture full stack trace including:
   - Error type (AttributeError, KeyError, AnalysisException, etc.)
   - Line number and function name
   - Failed DataFrame operation
   - Column names involved
   - Join conditions if applicable

### Phase 2: Categorize Error Types

#### A. Code-Based Errors

**Syntax/Import Errors**
- Missing imports from `pyspark.sql.functions`
- Incorrect function signatures
- Type hint violations
- Decorator usage errors

**Runtime Errors**
- `AnalysisException`: Column not found, table doesn't exist
- `AttributeError`: Calling non-existent DataFrame methods
- `KeyError`: Dictionary access failures
- `TypeError`: Incompatible data types in operations

**DataFrame Schema Errors**
- Column name mismatches (case sensitivity)
- Duplicate column names after joins
- Missing required columns for downstream operations
- Incorrect column aliases

#### B. Logical Errors

**Join Issues**
- **Incorrect Join Keys**: Joining on wrong columns (e.g., `offence_report_id` vs `cms_offence_report_id`)
- **Missing Table Aliases**: Ambiguous column references after joins
- **Wrong Join Types**: Using `inner` when `left` is required (or vice versa)
- **Cartesian Products**: Missing join conditions causing data explosion
- **Broadcast Misuse**: Not using `broadcast()` for small dimension tables
- **Duplicate Join Keys**: Multiple rows with same key causing row multiplication

**Aggregation Problems**
- Incorrect `groupBy()` columns
- Missing aggregation functions (`first()`, `last()`, `collect_list()`)
- Wrong window specifications
- Aggregating on nullable columns without `coalesce()`

**Business Rule Violations**
- Incorrect date/time logic (e.g., using `reported_date_time` when `date_created` should be fallback)
- Missing null handling for critical fields
- Status code logic errors
- Incorrect coalesce order

**Data Quality Issues**
- Expected vs actual row counts (use `logger.info(f"Expected X rows, got {df.count()}")`)
- Null propagation in critical columns
- Duplicate records not being handled
- Missing deduplication logic

## Systematic Debugging Process

### Step 1: Schema Verification
For each source table mentioned in the error:

1. **PRIMARY: Query MCP Server for Schema** (MANDATORY FIRST STEP):
   - Use MCP tools to query table schema from MotherDuck
   - Extract column names, data types, nullability, and constraints
   - Verify foreign key relationships for join operations
   - Cross-reference with error column names

   **Example MCP Query Pattern**:
   ```
   Query: "Get schema for table silver_cms.s_cms_offence_report"
   Expected Response: Column list with types and constraints
   ```

   **If MCP Server Fails**:
   - STOP and warn user (see Section 4: MCP Server Validation)
   - Do NOT proceed with fixing without schema verification
   - Suggest user check MCP server configuration

2. **SECONDARY: Verify Schema Using Data Dictionary** (as supplementary reference):
   - Read `.claude/data_dictionary/{source}_{table}.md`
   - Compare MCP schema vs data dictionary for consistency
   - Note any schema drift or discrepancies
   - Alert user if schemas don't match

3. **Check Table Existence**:
   ```python
   spark.sql("SHOW TABLES IN silver_cms").show()
   ```

4. **Inspect Actual Runtime Schema** (validate MCP data):
   ```python
   df = spark.read.table("silver_cms.s_cms_offence_report")
   df.printSchema()
   df.select([col for col in df.columns[:10]]).show(5, truncate=False)
   ```

   **Compare**:
   - MCP schema vs Spark runtime schema
   - Report any mismatches to user
   - Use runtime schema as source of truth if conflicts exist

5. **Use DuckDB Schema** (if available, as additional validation):
   - Query schema.db for column definitions
   - Check foreign key relationships
   - Validate join key data types
   - Triangulate: MCP + DuckDB + Data Dictionary should align

### Step 2: Join Logic Validation

For each join operation:

1. **Use MCP Server to Validate Join Relationships**:
   - Query foreign key constraints from MCP schema server
   - Identify correct join column names and data types
   - Verify parent-child table relationships
   - Confirm join key nullability (affects join results)

   **Example MCP Queries**:
   ```
   Query: "Show foreign keys for table silver_cms.s_cms_offence_report"
   Query: "What columns link s_cms_offence_report to s_cms_case_file?"
   Query: "Get data type for column cms_offence_report_id in silver_cms.s_cms_offence_report"
   ```

   **If MCP Returns No Foreign Keys**:
   - Fall back to data dictionary documentation
   - Check `.claude/data_dictionary/` for relationship diagrams
   - Manually verify join logic with business analyst

2. **Verify Join Keys Exist** (using MCP-confirmed column names):
   ```python
   left_df.select("join_key_column").show(5)
   right_df.select("join_key_column").show(5)
   ```

3. **Check Join Key Data Type Compatibility** (cross-reference with MCP schema):
   ```python
   # Verify types match MCP schema expectations
   left_df.select("join_key_column").dtypes
   right_df.select("join_key_column").dtypes
   ```

4. **Check Join Key Uniqueness**:
   ```python
   left_df.groupBy("join_key_column").count().filter("count > 1").show()
   ```

5. **Validate Join Type**:
   - `left`: Keep all left records (most common for fact-to-dimension)
   - `inner`: Only matching records
   - Use `broadcast()` for small lookup tables (< 10MB)
   - Confirm join type matches MCP foreign key relationship (nullable FK → left join)

6. **Handle Ambiguous Columns**:
   ```python
   # BEFORE (causes ambiguity if both tables have same column names)
   joined_df = left_df.join(right_df, on="common_id", how="left")

   # AFTER (select specific columns to avoid ambiguity)
   left_cols = [c for c in left_df.columns]
   right_cols = ["dimension_field"]
   joined_df = left_df.join(right_df, on="common_id", how="left").select(left_cols + right_cols)
   ```

### Step 3: Aggregation Verification

1. **Check groupBy Columns**:
   - Must include all columns not being aggregated
   - Verify columns exist in DataFrame

2. **Validate Aggregation Functions**:
   ```python
   from pyspark.sql.functions import min, max, first, count, sum, coalesce, lit

   aggregated = df.groupBy("key").agg(min("date_column").alias("earliest_date"), max("date_column").alias("latest_date"), first("dimension_column", ignorenulls=True).alias("dimension"), count("*").alias("record_count"), coalesce(sum("amount"), lit(0)).alias("total_amount"))
   ```

3. **Test Aggregation Logic**:
   - Run aggregation on small sample
   - Compare counts before/after
   - Check for unexpected nulls

### Step 4: Business Rule Testing

1. **Verify Timestamp Logic**:
   ```python
   from pyspark.sql.functions import when

   df.select("reported_date_time", "date_created", when(df["reported_date_time"].isNotNull(), df["reported_date_time"]).otherwise(df["date_created"]).alias("final_timestamp")).show(10)
   ```

2. **Test Null Handling**:
   ```python
   from pyspark.sql.functions import coalesce, lit

   df.select("primary_field", "fallback_field", coalesce(df["primary_field"], df["fallback_field"], lit(0)).alias("result")).show(10)
   ```

3. **Validate Status/Lookup Logic**:
   - Check status code mappings against data dictionary
   - Verify conditional logic matches business requirements

## Common Error Patterns and Fixes

### Pattern 1: Column Not Found After Join
**Error**: `AnalysisException: Column 'offence_report_id' not found`

**Root Cause**: Incorrect column name - verify column exists using MCP schema

**Fix**:
```python
# BEFORE - wrong column name
df = left_df.join(right_df, on="offence_report_id", how="left")

# AFTER - MCP-verified correct column name
df = left_df.join(right_df, on="cms_offence_report_id", how="left")

# If joining on different column names between tables:
df = left_df.join(
    right_df,
    left_df["cms_offence_report_id"] == right_df["offence_report_id"],
    how="left"
)
```

### Pattern 2: Duplicate Column Names
**Error**: Multiple columns with same name causing selection issues

**Fix**:
```python
# BEFORE - causes duplicate 'id' column
joined = left_df.join(right_df, left_df["id"] == right_df["id"], how="left")

# AFTER - drop duplicate from right table before join
right_df_clean = right_df.drop("id")
joined = left_df.join(right_df_clean, left_df["id"] == right_df["id"], how="left")

# OR - rename columns to avoid duplicates
right_df_renamed = right_df.withColumnRenamed("id", "related_id")
joined = left_df.join(right_df_renamed, left_df["id"] == right_df_renamed["related_id"], how="left")
```

### Pattern 3: Incorrect Aggregation
**Error**: Column not in GROUP BY causing aggregation failure

**Fix**:
```python
from pyspark.sql.functions import min, first

# BEFORE - non-aggregated column not in groupBy
df.groupBy("key1").agg(min("date_field"), "non_aggregated_field")

# AFTER - all non-grouped columns must be aggregated
df = df.groupBy("key1").agg(min("date_field").alias("min_date"), first("non_aggregated_field", ignorenulls=True).alias("non_aggregated_field"))
```

### Pattern 4: Join Key Mismatch
**Error**: No matching records or unexpected cartesian product

**Fix**:
```python
left_df.select("join_key").show(20)
right_df.select("join_key").show(20)
left_df.select("join_key").dtypes
right_df.select("join_key").dtypes
left_df.filter(left_df["join_key"].isNull()).count()
right_df.filter(right_df["join_key"].isNull()).count()
result = left_df.join(right_df, left_df["join_key"].cast("int") == right_df["join_key"].cast("int"), how="left")
```

### Pattern 5: Missing Null Handling
**Error**: Unexpected nulls propagating through transformations

**Fix**:
```python
from pyspark.sql.functions import coalesce, lit

# BEFORE - NULL if either field is NULL
df = df.withColumn("result", df["field1"] + df["field2"])

# AFTER - handle nulls with coalesce
df = df.withColumn("result", coalesce(df["field1"], lit(0)) + coalesce(df["field2"], lit(0)))
```

## Validation Requirements

After fixing errors, validate:

1. **Row Counts**: Log and verify expected vs actual counts at each transformation
2. **Schema**: Ensure output schema matches target table requirements
3. **Nulls**: Check critical columns for unexpected nulls
4. **Duplicates**: Verify uniqueness of ID columns
5. **Data Ranges**: Check timestamp ranges and numeric bounds
6. **Join Results**: Sample joined records to verify correctness

## Logging Requirements

Use `NotebookLogger` throughout:

```python
logger = NotebookLogger()

# Start of operation
logger.info(f"Starting extraction from {table_name}")

# After DataFrame creation
logger.info(f"Extracted {df.count()} records from {table_name}")

# After join
logger.info(f"Join completed: {joined_df.count()} records (expected ~X)")

# After transformation
logger.info(f"Transformation complete: {final_df.count()} records")

# On error
logger.error(f"Failed to process {table_name}: {error_message}")

# On success
logger.success(f"Successfully loaded {target_table_name}")
```

## Quality Gates (Must Run After Fixes)

```bash
# 1. Syntax validation
python3 -m py_compile python_files/gold/g_x_mg_cms_mo.py

# 2. Code quality check
ruff check python_files/gold/g_x_mg_cms_mo.py

# 3. Format code
ruff format python_files/gold/g_x_mg_cms_mo.py

# 4. Run fixed code
make gold_table
```

## Key Principles for PySpark Engineer Agent

1. **CRITICAL: Agent Workflow Required**: ALL error fixing must follow the 3-phase agent workflow (pyspark-engineer → code-reviewer → iterative refinement until 100% satisfied)
2. **CRITICAL: Validate MCP Server First**: Before starting, verify MCP server connectivity and schema availability. STOP and warn user if unavailable.
3. **Always Query MCP Schema First**: Use MCP server to get authoritative schema data before fixing any errors. Cross-reference with data dictionary.
4. **Use MCP for Join Validation**: Query foreign key relationships from MCP to ensure correct join logic and column names.
5. **DataFrame API Without Aliases or col()**: Use DataFrame API (NOT Spark SQL). NO DataFrame aliases. NO col() function. Use direct string references (e.g., `"column_name"`) or df["column"] syntax (e.g., `df["column_name"]`). Import only needed functions (e.g., `from pyspark.sql.functions import when, coalesce`)
6. **Test Incrementally**: Fix one error at a time, validate, then proceed
7. **Log Everything**: Add logging at every transformation step
8. **Handle Nulls**: Always consider null cases in business logic (check MCP nullability constraints)
9. **Verify Join Logic**: Check join keys, types, and uniqueness before implementing (use MCP data types)
10. **Use Utilities**: Leverage `TableUtilities` methods (add_row_hash, save_as_table, clean_date_time_columns)
11. **Follow Patterns**: Reference working gold layer files for established patterns
12. **Validate Business Rules**: Confirm logic with MCP schema, data dictionary, and user story requirements
13. **Clean Code**: Adhere to project standards (240 char line length, no blank lines in functions, type hints, single line per statement)
14. **Triple-Check Schemas**: When schema mismatch occurs, verify MCP → Runtime → Data Dictionary alignment and report discrepancies
15. **Code Review Loop**: Continue refactoring until code-reviewer explicitly confirms 100% satisfaction with zero remaining issues

## Example Workflow with MCP Integration

### Scenario: Fixing AnalysisException - Column 'offence_report_id' not found

**Step 1: MCP Server Validation**
```
Agent: Testing MCP server connectivity...
MCP Query: "List databases available"
MCP Response: ✓ [bronze_cms, silver_cms, silver_fvms, gold_data_model, ...]

Agent: ✓ MCP Server Connected
Agent: ✓ Schema data available
Agent: ✓ Proceeding with error fixing workflow
```

**Step 2: Query Schema via MCP**
```
Agent: Querying schema for silver_cms.s_cms_offence_report via MCP...
MCP Query: "DESCRIBE TABLE silver_cms.s_cms_offence_report"
MCP Response:
  - cms_offence_report_id (BIGINT, PRIMARY KEY, NOT NULL)
  - case_file_id (BIGINT, FOREIGN KEY → s_cms_case_file.cms_case_file_id, NULLABLE)
  - reported_date_time (TIMESTAMP, NULLABLE)
  - date_created (TIMESTAMP, NOT NULL)
  - status_code (VARCHAR, NULLABLE)
  ... (50+ more columns)

Agent: Found correct column name: 'cms_offence_report_id' (not 'offence_report_id')
```

**Step 3: Verify Join Relationship via MCP**
```
Agent: Checking foreign key relationship for join...
MCP Query: "Show foreign keys from s_cms_offence_report to s_cms_case_file"
MCP Response:
  - s_cms_offence_report.case_file_id → s_cms_case_file.cms_case_file_id
  - Relationship: MANY-TO-ONE
  - Nullability: case_file_id is NULLABLE → Use LEFT JOIN

Agent: ✓ Join should be: LEFT JOIN on case_file_id = cms_case_file_id
```

**Step 4: Apply Fix with MCP-Verified Schema**
```python
# BEFORE (error)
offence_df = spark.read.table("silver_cms.s_cms_offence_report")
case_df = spark.read.table("silver_cms.s_cms_case_file")
joined = offence_df.join(case_df, on="offence_report_id", how="left")

# AFTER (MCP-verified) - Use DataFrame API with correct column names
# MCP-confirmed FK: case_file_id → cms_case_file_id
# MCP-confirmed nullable FK → LEFT JOIN
# MCP-confirmed PK: cms_offence_report_id
case_df_subset = case_df.select("cms_case_file_id", "case_file_number")
joined = offence_df.join(case_df_subset, offence_df["case_file_id"] == case_df_subset["cms_case_file_id"], how="left")
joined = joined.withColumnRenamed("cms_offence_report_id", "offence_report_id")
```

**Step 5: Validate Fix**
```
Agent: Running fixed code...
Agent: ✓ No AnalysisException
Agent: ✓ Join executed successfully
Agent: Row count: 45,823 (expected ~45,000)
Agent: ✓ Schema matches MCP expectations
```

## Success Criteria

### Phase 1: Initial Error Fixing (pyspark-engineer)
- [ ] **MCP Server validated and responding** (MANDATORY FIRST CHECK)
- [ ] Schema verified via MCP server for all source tables
- [ ] Foreign key relationships confirmed via MCP queries
- [ ] All syntax errors resolved
- [ ] All runtime errors fixed
- [ ] Join logic validated and correct (using MCP-confirmed column names and types)
- [ ] DataFrame API used (NOT Spark SQL) per python_rules.md line 19
- [ ] NO DataFrame aliases or col() function used - direct string references or df["column"] syntax only (per python_rules.md line 20)
- [ ] Code follows python_rules.md standards: 240 char lines, no blank lines in functions, single line per statement, imports at top only
- [ ] Row counts logged and reasonable
- [ ] Business rules implemented correctly
- [ ] Output schema matches requirements (cross-referenced with MCP schema)
- [ ] Code passes quality gates (py_compile, ruff check, ruff format)
- [ ] `make gold_table` executes successfully
- [ ] Target table created/updated in `gold_data_model` database
- [ ] No schema drift reported between MCP, Runtime, and Data Dictionary sources

### Phase 2: Code Review (code-reviewer)
- [ ] code-reviewer agent launched with fixed code
- [ ] Comprehensive review completed covering:
  - [ ] PySpark best practices adherence
  - [ ] Join logic correctness
  - [ ] Schema alignment validation
  - [ ] Business rule implementation accuracy
  - [ ] Code quality and standards compliance
  - [ ] Security vulnerabilities (none found)
  - [ ] Performance optimization opportunities addressed

### Phase 3: Iterative Refinement (MANDATORY UNTIL 100% SATISFIED)
- [ ] All code-reviewer feedback items addressed by pyspark-engineer
- [ ] Re-review completed by code-reviewer
- [ ] Iteration cycle repeated until code-reviewer explicitly confirms:
  - [ ] **"✓ 100% SATISFIED - No further changes required"**
  - [ ] Zero remaining issues, warnings, or concerns
  - [ ] All quality gates pass
  - [ ] All business rules validated
  - [ ] Code meets production-ready standards

### Final Approval
- [ ] **code-reviewer has explicitly confirmed 100% satisfaction**
- [ ] No outstanding issues or concerns remain
- [ ] Task is complete and ready for production deployment
