# Unify 2.1 Multi-Agent Orchestration Plugin

A comprehensive Claude Code plugin for PySpark data engineering with Azure Synapse Analytics, featuring multi-agent orchestration, medallion architecture ETL pipelines, and complete Azure DevOps integration.

## Overview

This plugin provides a complete development framework for the Unify 2.1 data migration project, including:

- **16 Specialized Agents** - Multi-agent orchestration with Chain of Verification
- **28 Slash Commands** - Complete workflow automation
- **9 Skills** - On-demand knowledge loading for detailed technical guidance
- **3 Hooks** - Intelligent prompt interception with automatic skill activation and orchestrator routing

## Key Features

### Multi-Agent Orchestration

Coordinate 2-8 specialized agents in parallel, sequential, or hybrid workflows:

- **master-orchestrator** - Coordinates complex multi-agent workflows
- **Chain of Verification** - Systematic validation strategy (Primary Task → Generate Output → Identify Weaknesses → Cite Evidence → Revise)
- **JSON Communication Protocol** - Standardized agent responses with role-specific metrics
- **Quality Gates** - Mandatory syntax, linting, formatting, and testing validation



# Agents

## Core Development Agents

**developer-pyspark** - PySpark ETL development for Azure Synapse
- Metrics: dataframes_created, tables_written, rows_processed
- Use for: Bronze/Silver/Gold layer development

**code-reviewer** - Comprehensive code quality review
- Metrics: files_reviewed, critical_issues, major_issues, minor_issues
- Use for: Pull request reviews, security audits

**test-engineer** - Pytest testing for PySpark data pipelines
- Metrics: test_cases_added, assertions_added, coverage_percentage
- Use for: Unit tests, integration tests, data validation

## Specialised Technical Agents

**developer-python** - Advanced Python development
- Metrics: decorators_added, async_functions_added, type_hints_added
- Use for: Async/await patterns, decorators, type hints

**developer-sql** - SQL query optimization and database development
- Metrics: queries_optimized, indexes_created, stored_procedures_added
- Use for: Query optimization, database design

**developer-azure-engineer** - Azure DevOps pipelines and PowerShell
- Metrics: pipelines_created, powershell_scripts_added, azure_resources_configured
- Use for: CI/CD pipelines, infrastructure automation

**performance-engineer** - Performance optimization and profiling
- Metrics: bottlenecks_identified, optimizations_applied, performance_improvement_percentage
- Use for: Performance bottlenecks, load testing

## Supporting Agents

**git-manager** - Azure DevOps git workflow specialist
- Metrics: branches_created, prs_created, commits_made
- Use for: Branch management, PR creation

**code-documenter** - Azure DevOps wiki documentation
- Metrics: docs_created, sections_added, examples_added
- Use for: Technical documentation, architecture guides

**powershell-test-engineer** - Pester v5 testing for PowerShell
- Metrics: pester_tests_added, mocks_created, coverage_percentage
- Use for: PowerShell test automation

**developer-bash-shell** - Robust shell scripting
- Metrics: scripts_created, error_handlers_added, posix_compliance
- Use for: Deployment scripts, automation

## Planning & Architecture Agents

**product-manager** - Product planning and feature specifications
- Metrics: user_personas_created, user_stories_created, features_defined
- Use for: User stories, product requirements

**business-analyst** - Azure DevOps user story analysis
- Metrics: user_stories_analyzed, requirements_identified, deployment_plans_created
- Use for: Deployment planning, technical requirements

**system-architect** - Technical architecture design
- Metrics: components_designed, api_endpoints_defined, data_models_created
- Use for: System architecture, API contracts

**security-analyst** - Security vulnerability assessment
- Metrics: vulnerabilities_found, security_issues_critical, security_issues_high
- Use for: Security reviews, compliance validation

## Commands

### Context Optimization (Start Here!)

**/prime-claude** [--analyze-only] | [--backup] | [--apply] - Optimize CLAUDE.md for efficiency
```
/prime-claude --analyze-only    # See what would be optimized
/prime-claude --backup --apply  # Distill CLAUDE.md, create skills
```

**What it does**: Reduces CLAUDE.md from 400+ lines to ~100 lines (80-90% context savings) by moving detailed knowledge into on-demand skills. Transforms "always-loaded" documentation into "load-when-needed" skills for faster responses and more room for actual work.

**Benefits**:
- Save 10,000+ tokens per conversation
- Faster Claude responses
- More context space for your work
- Better organized knowledge in focused skills

---

### Orchestration Commands

**/orchestrate** [user-prompt] - Orchestrate multiple agents in parallel
```
/orchestrate "Optimize the customer ETL pipeline for performance"
```

**/multi-agent** [task-description] - Discuss multi-agent workflow strategy
```
/multi-agent "Plan deployment strategy for new gold layer tables"
```

**/background** [user-prompt] - Fire off agent in background
```
/background "Generate tests for all silver layer tables"
```

### Development Commands

**/write-tests** [target-file] - Write pytest tests for PySpark pipelines
```
/write-tests python_files/silver/cms/s_customer.py
```

**/code-review** [file-path] - Comprehensive code quality review
```
/code-review python_files/gold/g_customer_analytics.py
```

**/describe** [file-path] - Add descriptive comments to code
```
/describe python_files/silver/cms/s_order.py
```

**/create-feature** [feature-name] - Scaffold new feature with boilerplate
```
/create-feature customer_segmentation
```

**/explain-code** [file-path] - Explain code functionality and architecture
```
/explain-code python_files/utilities/session_optimiser.py
```

**/refactor-code** [file-path] - Refactor code for better quality
```
/refactor-code python_files/gold/g_customer_analytics.py
```

**/pyspark-errors** - Diagnose and fix common PySpark errors
```
/pyspark-errors
```

### Documentation Commands

**/update-docs** [doc-type] - Generate documentation and sync to Azure wiki
```
/update-docs --generate-local
/update-docs --sync-to-wiki
```

**/create-prd** [feature-name] - Create Product Requirements Document
```
/create-prd audit_logging_feature
```

### Azure DevOps & Git Commands

**/my-devops-tasks** - Retrieve all assigned Azure DevOps work items
```
/my-devops-tasks
```

**/local-commit** [message] - Create well-formatted commits
```
/local-commit "Add customer segmentation ETL pipeline"
```

**/pr-feature-to-staging** - Create PR from feature to staging
```
/pr-feature-to-staging
```

**/pr-staging-to-develop** - Create PR from staging to develop
```
/pr-staging-to-develop
```

**/pr-fix-pr-review** [PR_ID] - Address PR review feedback
```
/pr-fix-pr-review 12345
```

**/pr-deploy-workflow** [commit-message] - Complete deployment workflow
```
/pr-deploy-workflow "Deploy customer segmentation to production"
```

**/branch-cleanup** [--dry-run] | [--force] - Clean up merged branches
```
/branch-cleanup --dry-run
```

### Monitoring & Performance Commands

**/performance-monitoring** [monitoring-type] - Setup application performance monitoring
```
/performance-monitoring --apm
```

**/setup-docker-containers** [environment-type] - Setup Docker containerization
```
/setup-docker-containers --development
```

## Skills

Load skills on-demand for detailed technical guidance:

### Core Skills

**project-architecture** - Medallion architecture deep dive
```
Use skill: project-architecture
```

**project-commands** - Complete make command reference
```
Use skill: project-commands
```

**pyspark-patterns** - PySpark best practices and TableUtilities
```
Use skill: pyspark-patterns
```

**schema-reference** - Automatic schema validation and lookup
```
Use skill: schema-reference
```

### Integration Skills

**azure-devops** - Azure DevOps operations (PRs, work items, pipelines)
```
Use skill: azure-devops
```

**mcp-code-execution** - MCP integration patterns
```
Use skill: mcp-code-execution
```

### Framework Skills

**multi-agent-orchestration** - Multi-agent coordination patterns
```
Use skill: multi-agent-orchestration
```

**skill-creator** - Guide for creating new skills
```
Use skill: skill-creator
```

**Example: Creating a Database Schema Skill**
```
You: "I want to create a skill that provides detailed schema information for all database tables"

Claude loads skill-creator, then guides you through:

1. Skill purpose and scope
   → Centralized database schema reference
   → Column definitions, data types, constraints
   → Relationships and foreign keys

2. Skill structure
   → Create: .claude/skills/database-schemas.md
   → Organize by: database → table → columns
   → Include: sample queries and common patterns

3. Trigger configuration (skill-rules.json)
   → Keywords: ["schema", "table", "column", "database", "field"]
   → Intent patterns: ["what.*schema", "show.*table.*structure"]
   → Priority: critical (for data work)

4. Integration with existing skills
   → Works with: schema-reference, pyspark-patterns
   → Loads automatically when schema questions detected

Result: On-demand database schema knowledge that activates automatically
        when you ask schema-related questions, without polluting context
        for non-database work.
```



## Hooks

This plugin provides a **dual-stage hook pipeline** that intelligently routes prompts:

### 1. skill-activation-prompt
Detects domain-specific needs and recommends skills to load:
- Matches keywords and intent patterns from `skill-rules.json`
- Recommends critical, high, medium, or low priority skills
- Prevents context pollution by loading only when needed

### 2. orchestrator-interceptor
Analyzes complexity and routes to optimal execution strategy:
- Classifies prompts: Simple Query | Moderate Task | Complex Task | High Complexity
- Provides upfront cost estimates ($0.002 - $0.129 USD)
- Routes complex tasks through master-orchestrator agent
- Presents execution plan with user approval workflow

### 3. combined-prompt-hook
Chains both hooks seamlessly:
- Runs skill-activation first (domain knowledge)
- Runs orchestrator-interceptor second (execution strategy)
- Merges outputs into unified context injection
- Fail-safe design (errors don't block prompts)

**Example Flow**:
```
User: "Fix linting across bronze, silver, and gold layers"
  ↓
Skill Hook: Load project-architecture, pyspark-patterns
  ↓
Orchestrator: High complexity, 6-8 agents, $0.129 USD
  ↓
Claude: Presents execution plan for user approval
```

See `hooks/README.md` for detailed documentation, configuration, and testing.

## Configuration

### Coding Standards

- **Line Length**: 240 characters
- **Type Hints**: Mandatory for all parameters and returns
- **Blank Lines**: None inside functions, one between functions
- **Docstrings**: Only when explicitly requested
- **Error Handling**: Use `@synapse_error_print_handler` decorator

### Branch Workflow

```
feature → staging → develop → main
```

### Medallion Architecture

- **Bronze**: Raw parquet ingestion (`python_files/pipeline_operations/bronze_layer_deployment.py`)
- **Silver**: Validated, standardized data (`python_files/silver/`)
- **Gold**: Business-ready analytics (`python_files/gold/`)

## Examples

### Example 1: Multi-Agent PySpark Development

```
/orchestrate "Create a comprehensive ETL pipeline for customer order data with tests and documentation"
```

This will launch:
1. **developer-pyspark** - Create ETL pipeline
2. **test-engineer** - Write pytest tests
3. **code-documenter** - Generate documentation
4. **code-reviewer** - Review for quality

### Example 2: Security-First Feature Development

```
/orchestrate "Design and validate a secure audit logging system"
```

This will launch:
1. **product-manager** - Create user stories
2. **system-architect** - Design architecture
3. **security-analyst** - Security review
4. **code-documenter** - Document findings

### Example 3: Performance Optimization

```
/code-review python_files/gold/g_customer_analytics.py --full
/add-performance-monitoring --apm
```

Then review recommendations and apply optimizations.

## Testing

The plugin includes comprehensive testing across all 16 agents:

- **Phase 1**: Python utility enhancement (parallel execution)
- **Phase 2**: Data processor optimization (parallel execution)
- **Phase 3**: Deployment automation (hybrid execution)
- **Phase 4**: Audit logging planning (sequential execution)

All tests validate:
- JSON response format
- Role-specific metrics
- Quality gates execution
- Chain of Verification strategy

## Quality Gates

All agents enforce mandatory quality gates:

1. **Syntax Check**: `python3 -m py_compile <file>`
2. **Linting**: `ruff check python_files/`
3. **Formatting**: `ruff format python_files/`
4. **Tests**: `pytest python_files/testing/`

## Contributing

This plugin is part of the Unify 2.1 data migration project. All agents follow orchestration mode conventions with standardized JSON responses.

### Adding New Agents

See the **skill-creator** skill for guidance on creating new specialized agents.

### Adding New Commands

Create slash commands in `.claude/plugins/repos/unify_2_1/commands/` following the existing pattern.

## License

MIT License

## Version History

**1.0.0** (2025-11-10)
- Initial release
- 16 specialized agents with multi-agent orchestration
- 30 slash commands for complete workflow automation
- 9 skills for on-demand knowledge loading
- Chain of Verification strategy integrated
- Complete Phase 1-4 testing validation

## Support

For issues, questions, or contributions, please refer to the project documentation in the `.claude/` directory or contact the Unify development team.
