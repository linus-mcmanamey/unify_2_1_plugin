# Unify 2.1 Multi-Agent Orchestration Plugin

A comprehensive Claude Code plugin for PySpark data engineering with Azure Synapse Analytics, featuring multi-agent orchestration, medallion architecture ETL pipelines, and complete Azure DevOps integration.

## Overview

This plugin provides a complete development framework for the Unify 2.1 data migration project, including:

- **16 Specialized Agents** - Multi-agent orchestration with Chain of Verification
- **30 Slash Commands** - Complete workflow automation
- **9 Skills** - On-demand knowledge loading for detailed technical guidance
- **3 Hooks** - Custom workflow integrations

## Key Features

### Multi-Agent Orchestration

Coordinate 2-8 specialized agents in parallel, sequential, or hybrid workflows:

- **master-orchestrator** - Coordinates complex multi-agent workflows
- **Chain of Verification** - Systematic validation strategy (Primary Task → Generate Output → Identify Weaknesses → Cite Evidence → Revise)
- **JSON Communication Protocol** - Standardized agent responses with role-specific metrics
- **Quality Gates** - Mandatory syntax, linting, formatting, and testing validation

### PySpark Development

Medallion architecture ETL pipelines for Azure Synapse Analytics:

- **Bronze Layer** - Raw parquet ingestion
- **Silver Layer** - Validated, standardized data
- **Gold Layer** - Business-ready analytics
- **Core Utilities** - SparkOptimiser, NotebookLogger, TableUtilities

### Azure DevOps Integration

Complete Azure DevOps workflow support:

- User story analysis and deployment planning
- CI/CD pipeline creation with PowerShell
- Pull request management and code review
- Work item tracking and sprint planning

## Installation

```bash
# Copy plugin to Claude Code plugins directory
cp -r .claude/plugins/repos/unify_2_1 ~/.claude/plugins/repos/

# Or use as local plugin (already configured in this project)
# Plugin is available at: .claude/plugins/repos/unify_2_1
```

## Getting Started

### Quick Start

1. **Run the interactive UI**:
   ```bash
   make ui
   ```

2. **Execute a slash command**:
   ```
   /orchestrate "Create a PySpark ETL pipeline for customer data"
   ```

3. **Launch a specialized agent**:
   ```
   /code-review python_files/silver/cms/
   ```

### Basic Workflows

**Full Pipeline Execution**:
```bash
make run_all  # Bronze → Silver → Gold → DuckDB
```

**Layer-Specific Execution**:
```bash
make bronze      # Bronze layer only
make run_silver  # Silver layer only
make gold        # Gold layer only
```

**Quality Gates** (mandatory before commit):
```bash
python3 -m py_compile <file>  # Syntax check
ruff check python_files/       # Linting
ruff format python_files/      # Formatting
```

## Agents

### Phase 1: Core Development Agents

**developer-pyspark** - PySpark ETL development for Azure Synapse
- Metrics: dataframes_created, tables_written, rows_processed
- Use for: Bronze/Silver/Gold layer development

**code-reviewer** - Comprehensive code quality review
- Metrics: files_reviewed, critical_issues, major_issues, minor_issues
- Use for: Pull request reviews, security audits

**test-engineer** - Pytest testing for PySpark data pipelines
- Metrics: test_cases_added, assertions_added, coverage_percentage
- Use for: Unit tests, integration tests, data validation

### Phase 2: Specialized Technical Agents

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

### Phase 3: Supporting Agents

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

### Phase 4: Planning & Architecture Agents

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

### Orchestration Commands

**/orchestrate** [user-prompt] - Orchestrate multiple agents in parallel
```
/orchestrate "Optimize the customer ETL pipeline for performance"
```

**/aa_command** [task-description] - Discuss multi-agent workflow strategy
```
/aa_command "Plan deployment strategy for new gold layer tables"
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

### Documentation Commands

**/update-docs** [doc-type] - Generate documentation and sync to Azure wiki
```
/update-docs --generate-local
/update-docs --sync-to-wiki
```

**/update-docs-test** [test-type] - Test documentation generation
```
/update-docs-test --test-local
```

**/create-prd** [feature-name] - Create Product Requirements Document
```
/create-prd audit_logging_feature
```

### Git & Deployment Commands

**/local-commit** [message] - Create well-formatted commits
```
/local-commit "Add customer segmentation ETL pipeline"
```

**/pr-feature-to-staging** - Create PR from feature to staging
```
/pr-feature-to-staging
```

**/commit-and-pr** [commit-message] - Commit and create PR in one step
```
/commit-and-pr "Implement customer analytics gold layer"
```

**/pr-deploy-workflow** [commit-message] - Complete deployment workflow
```
/pr-deploy-workflow "Deploy customer segmentation to production"
```

**/branch-cleanup** - Clean up merged branches
```
/branch-cleanup --dry-run
```

### Monitoring & Performance Commands

**/add-performance-monitoring** [monitoring-type] - Setup APM
```
/add-performance-monitoring --apm
```

**/setup-docker-containers** [environment-type] - Setup Docker
```
/setup-docker-containers --development
```

**/workflow-orchestrator** [workflow-name] - Complex automation workflows
```
/workflow-orchestrator create deployment-pipeline
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

## Hooks

**skill-activation-prompt** - Provides contextual skill recommendations

The hook automatically suggests relevant skills based on user queries:
- Detects when detailed knowledge would be helpful
- Recommends specific skills to load
- Prevents context pollution by loading only when needed

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
