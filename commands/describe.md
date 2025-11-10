---
allowed-tools: Read, mcp__mcp-server-motherduck__query, Grep, Glob, Bash
argument-hint: [file-path] (optional - defaults to currently open file)
description: Add comprehensive descriptive comments to code files, focusing on data flow, joining logic, and business context
---

# Add Descriptive Comments to Code

Add detailed, descriptive comments to the selected file: $ARGUMENTS

## Current Context

- Currently open file: !`echo $CLAUDE_OPEN_FILE`
- File layer detection: !`basename $(dirname $CLAUDE_OPEN_FILE) 2>/dev/null || echo "unknown"`
- Git status: !`git status --porcelain $CLAUDE_OPEN_FILE 2>/dev/null || echo "Not in git"`

## Task

You will add comprehensive descriptive comments to the **currently open file** (or the file specified in $ARGUMENTS if provided).

### Instructions

1. **Determine Target File**
   - If $ARGUMENTS contains a file path, use that file
   - Otherwise, use the currently open file from the IDE
   - Verify the file exists and is readable

2. **Analyze File Context**
   - Identify the file type (silver/gold layer transformation, utility, pipeline operation)
   - Read and understand the complete file structure
   - Identify the ETL pattern (extract, transform, load methods)
   - Map out all DataFrame operations and transformations

3. **Analyze Data Sources and Schemas**
   - Use DuckDB MCP to query relevant source tables if available:
     ```sql
     -- Example: Check schema of source table
     DESCRIBE table_name;
     SELECT * FROM table_name LIMIT 5;
     ```
   - Reference `.claude/memory/data_dictionary/` for column definitions and business context
   - Identify all source tables being read (bronze/silver layer)
   - Document the schema of input and output DataFrames

4. **Document Joining Logic (Priority Focus)**
   - For each join operation, add comments explaining:
     - **WHY** the join is happening (business reason)
     - **WHAT** tables are being joined
     - **JOIN TYPE** (left, inner, outer) and why that type was chosen
     - **JOIN KEYS** and their meaning
     - **EXPECTED CARDINALITY** (1:1, 1:many, many:many)
     - **NULL HANDLING** strategy for unmatched records

   Example format:
   ```python
   # JOIN: Link incidents to persons involved
   # Type: LEFT JOIN (preserve all incidents even if person data missing)
   # Keys: incident_id (unique identifier from FVMS system)
   # Expected: 1:many (one incident can have multiple persons)
   # Nulls: Person details will be NULL for incidents with no associated persons
   joined_df = incident_df.join(person_df, on="incident_id", how="left")
   ```

5. **Document Transformations Step-by-Step**
   - Add inline comments explaining each transformation
   - Describe column derivations and calculations
   - Explain business rules being applied
   - Document any data quality fixes or cleansing
   - Note any deduplication logic

6. **Document Data Quality Patterns**
   - Explain null handling strategies
   - Document default values and their business meaning
   - Describe validation rules
   - Note any data type conversions

7. **Add Function/Method Documentation**
   - Add docstring-style comments at the start of each method explaining:
     - Purpose of the method
     - Input: Source tables and their schemas
     - Output: Resulting table and schema
     - Business logic summary

   Example format:
   ```python
   def transform(self) -> DataFrame:
       """
       Transform incident data with person and location enrichment.

       Input: bronze_fvms.b_fvms_incident (raw incident records)
       Output: silver_fvms.s_fvms_incident (validated, enriched incidents)

       Transformations:
       1. Join with person table to add demographic details
       2. Join with address table to add location coordinates
       3. Apply business rules for incident classification
       4. Deduplicate based on incident_id and date_created
       5. Add row hash for change detection

       Business Context:
       - Incidents represent family violence events recorded in FVMS
       - Each incident may involve multiple persons (victims, offenders)
       - Location data enables geographic analysis and reporting
       """
   ```

8. **Add Header Comments**
   - Add a comprehensive header at the top of the file explaining:
     - File purpose and business context
     - Source systems and tables
     - Target table and database
     - Key transformations and business rules
     - Dependencies on other tables or processes

9. **Variable Naming Context**
   - When variable names are abbreviated or unclear, add comments explaining:
     - What the variable represents
     - The business meaning of the data
     - Expected data types and formats
     - Reference data dictionary entries if available

10. **Use Data Dictionary References**
    - Check `.claude/memory/data_dictionary/` for column definitions
    - Reference these definitions in comments to explain field meanings
    - Link business terminology to technical column names
    - Example: `# offence_code: Maps to ANZSOC classification system (see data_dict/cms_offence_codes.md)`

11. **Query DuckDB for Context (When Available)**
    - Use MCP DuckDB tool to inspect actual data patterns:
    - Check distinct values: `SELECT DISTINCT column_name FROM table LIMIT 20;`
    - Verify join relationships: `SELECT COUNT(*) FROM table1 JOIN table2 ...`
    - Understand data distributions: `SELECT column, COUNT(*) FROM table GROUP BY column;`
    - Use insights from queries to write more accurate comments

12. **Preserve Code Formatting Standards**
    - Do NOT add blank lines inside functions (project standard)
    - Maximum line length: 240 characters
    - Maintain existing indentation
    - Keep comments concise but informative
    - Use inline comments for single-line explanations
    - Use block comments for multi-step processes

13. **Focus Areas by File Type**

    **Silver Layer Files (`python_files/silver/`):**
    - Document source bronze tables
    - Explain validation rules
    - Describe enumeration mappings
    - Note data cleansing operations

    **Gold Layer Files (`python_files/gold/`):**
    - Document all source silver tables
    - Explain aggregation logic
    - Describe business metrics calculations
    - Note analytical transformations

    **Utility Files (`python_files/utilities/`):**
    - Explain helper function purposes
    - Document parameter meanings
    - Describe return values
    - Note edge cases handled

14. **Comment Quality Guidelines**
    - Comments should explain **WHY**, not just **WHAT**
    - Avoid obvious comments (e.g., don't say "create dataframe" for `df = spark.createDataFrame()`)
    - Focus on business context and data relationships
    - Use proper grammar and complete sentences
    - Be concise but thorough
    - Think like a new developer reading the code for the first time

15. **Final Validation**
    - Run syntax check: `python3 -m py_compile <file>`
    - Run linting: `ruff check <file>`
    - Format code: `ruff format <file>`
    - Ensure all comments are accurate and helpful

## Example Output Structure

After adding comments, the file should have:
- ✅ Comprehensive header explaining file purpose
- ✅ Method-level documentation for extract/transform/load
- ✅ Detailed join operation comments (business reason, type, keys, cardinality)
- ✅ Step-by-step transformation explanations
- ✅ Data quality and validation logic documented
- ✅ Variable context for unclear names
- ✅ References to data dictionary where applicable
- ✅ Business context linking technical operations to real-world meaning

## Important Notes
- **ALWAYS** use Australian English spelling conventions throughout the comments and documentation
- **DO NOT** remove or modify existing functionality
- **DO NOT** change code structure or logic
- **ONLY** add descriptive comments
- **PRESERVE** all existing comments
- **MAINTAIN** project coding standards (no blank lines in functions, 240 char max)
- **USE** the data dictionary and DuckDB queries to provide accurate context
- **THINK** about the user who will read this code - walk them through the logic clearly
