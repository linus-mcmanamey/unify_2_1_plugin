---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [target-file] | [test-type] | --unit | --integration | --data-validation | --medallion
description: Write comprehensive pytest tests for PySpark data pipelines with live data validation
model: sonnet
---

# Write Tests - pytest + PySpark with Live Data

Write comprehensive pytest tests for PySpark data pipelines using **LIVE DATA** sources: **$ARGUMENTS**

## Current Testing Context

- Test framework: !`[ -f pytest.ini ] && echo "pytest configured" || echo "pytest setup needed"`
- Target: $ARGUMENTS (file/layer to test)
- Test location: !`ls -d tests/ test/ 2>/dev/null | head -1 || echo "tests/ (will create)"`
- Live data available: Bronze/Silver/Gold layers with real FVMS, CMS, NicheRMS tables

## Core Principle: TEST WITH LIVE DATA

**ALWAYS use real data from Bronze/Silver/Gold layers**. No mocked data unless absolutely necessary.

## pytest Testing Framework

### 1. Test File Organization

```
tests/
├── conftest.py                    # Shared fixtures (Spark session, live data)
├── test_bronze_ingestion.py       # Bronze layer validation
├── test_silver_transformations.py # Silver layer ETL
├── test_gold_aggregations.py      # Gold layer analytics
├── test_utilities.py              # TableUtilities, NotebookLogger
└── integration/
    └── test_end_to_end_pipeline.py
```

### 2. Essential pytest Fixtures (conftest.py)

```python
import pytest
from pyspark.sql import SparkSession
from python_files.utilities.session_optimiser import SparkOptimiser

@pytest.fixture(scope="session")
def spark():
    """Shared Spark session for all tests - reuses SparkOptimiser"""
    session = SparkOptimiser.get_optimised_spark_session()
    yield session
    session.stop()

@pytest.fixture(scope="session")
def bronze_data(spark):
    """Live bronze layer data - REAL DATA"""
    return spark.table("bronze_fvms.b_vehicle_master")

@pytest.fixture(scope="session")
def silver_data(spark):
    """Live silver layer data - REAL DATA"""
    return spark.table("silver_fvms.s_vehicle_master")

@pytest.fixture
def sample_live_data(bronze_data):
    """Small sample from live data for fast tests"""
    return bronze_data.limit(100)
```

### 3. pytest Test Patterns

#### Pattern 1: Unit Tests (Individual Functions)

```python
# tests/test_utilities.py
import pytest
from python_files.utilities.session_optimiser import TableUtilities

class TestTableUtilities:
    def test_add_row_hash_creates_hash_column(self, spark, sample_live_data):
        """Verify add_row_hash() creates hash_key column"""
        result = TableUtilities.add_row_hash(sample_live_data, ["vehicle_id"])
        assert "hash_key" in result.columns
        assert result.count() == sample_live_data.count()

    def test_drop_duplicates_simple_removes_exact_duplicates(self, spark):
        """Test deduplication on live data"""
        # Use LIVE data with known duplicates
        raw_data = spark.table("bronze_fvms.b_vehicle_events")
        result = TableUtilities.drop_duplicates_simple(raw_data)
        assert result.count() <= raw_data.count()

    @pytest.mark.parametrize("date_col", ["created_date", "updated_date", "event_date"])
    def test_clean_date_time_columns_handles_all_formats(self, spark, bronze_data, date_col):
        """Parameterized test for date cleaning"""
        if date_col in bronze_data.columns:
            result = TableUtilities.clean_date_time_columns(bronze_data, [date_col])
            assert date_col in result.columns
```

#### Pattern 2: Integration Tests (End-to-End)

```python
# tests/integration/test_end_to_end_pipeline.py
import pytest
from python_files.silver.fvms.s_vehicle_master import VehicleMaster

class TestSilverVehicleMasterPipeline:
    def test_full_etl_with_live_bronze_data(self, spark):
        """Test complete Bronze → Silver transformation with LIVE data"""
        # Extract: Read LIVE bronze data
        bronze_table = "bronze_fvms.b_vehicle_master"
        bronze_df = spark.table(bronze_table)
        initial_count = bronze_df.count()

        # Transform & Load: Run actual ETL class
        etl = VehicleMaster(bronze_table_name=bronze_table)

        # Validate: Check LIVE silver output
        silver_df = spark.table("silver_fvms.s_vehicle_master")
        assert silver_df.count() > 0
        assert "hash_key" in silver_df.columns
        assert "load_timestamp" in silver_df.columns

        # Data quality: No nulls in critical fields
        assert silver_df.filter("vehicle_id IS NULL").count() == 0
```

#### Pattern 3: Data Validation (Live Data Checks)

```python
# tests/test_data_validation.py
import pytest

class TestBronzeLayerDataQuality:
    """Validate live data quality in Bronze layer"""

    def test_bronze_vehicle_master_has_recent_data(self, spark):
        """Verify bronze layer contains recent records"""
        from pyspark.sql.functions import max, datediff, current_date

        df = spark.table("bronze_fvms.b_vehicle_master")
        max_date = df.select(max("load_timestamp")).collect()[0][0]

        # Data should be less than 30 days old
        assert (current_date() - max_date).days <= 30

    def test_bronze_to_silver_row_counts_match_expectations(self, spark):
        """Validate row count transformation logic"""
        bronze = spark.table("bronze_fvms.b_vehicle_master")
        silver = spark.table("silver_fvms.s_vehicle_master")

        # After deduplication, silver <= bronze
        assert silver.count() <= bronze.count()

    @pytest.mark.slow
    def test_hash_key_uniqueness_on_live_data(self, spark):
        """Verify hash_key uniqueness in Silver layer (full scan)"""
        df = spark.table("silver_fvms.s_vehicle_master")
        total = df.count()
        unique = df.select("hash_key").distinct().count()

        assert total == unique, f"Duplicate hash_keys found: {total - unique}"
```

#### Pattern 4: Schema Validation

```python
# tests/test_schema_validation.py
import pytest
from pyspark.sql.types import StringType, IntegerType, TimestampType

class TestSchemaConformance:
    def test_silver_vehicle_schema_matches_expected(self, spark):
        """Validate Silver layer schema against business requirements"""
        df = spark.table("silver_fvms.s_vehicle_master")
        schema_dict = {field.name: field.dataType for field in df.schema.fields}

        # Critical fields must exist
        assert "vehicle_id" in schema_dict
        assert "hash_key" in schema_dict
        assert "load_timestamp" in schema_dict

        # Type validation
        assert isinstance(schema_dict["vehicle_id"], StringType)
        assert isinstance(schema_dict["load_timestamp"], TimestampType)
```

### 4. pytest Markers & Configuration

**pytest.ini**:
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    live_data: tests that require live data access
addopts =
    -v
    --tb=short
    --strict-markers
    --disable-warnings
```

**Run specific test types**:
```bash
pytest tests/test_utilities.py -v                    # Single file
pytest -m unit                                       # Only unit tests
pytest -m "not slow"                                 # Skip slow tests
pytest -k "vehicle"                                  # Tests matching "vehicle"
pytest --maxfail=1                                   # Stop on first failure
pytest -n auto                                       # Parallel execution (pytest-xdist)
```

### 5. Advanced pytest Features

#### Parametrized Tests
```python
@pytest.mark.parametrize("table_name,expected_min_count", [
    ("bronze_fvms.b_vehicle_master", 1000),
    ("bronze_cms.b_customer_master", 500),
    ("bronze_nicherms.b_booking_master", 2000),
])
def test_bronze_tables_have_minimum_rows(spark, table_name, expected_min_count):
    """Validate minimum row counts across multiple live tables"""
    df = spark.table(table_name)
    assert df.count() >= expected_min_count
```

#### Fixtures with Live Data Sampling
```python
@pytest.fixture
def stratified_sample(bronze_data):
    """Stratified sample from live data for statistical tests"""
    from pyspark.sql.functions import col
    return bronze_data.sampleBy("vehicle_type", fractions={"Car": 0.1, "Truck": 0.1})
```

### 6. Testing Best Practices

**DO**:
- ✅ Use `spark.table()` to read LIVE Bronze/Silver/Gold data
- ✅ Test with `.limit(100)` for speed, full dataset for validation
- ✅ Use `@pytest.fixture(scope="session")` for Spark session (reuse)
- ✅ Test actual ETL classes (e.g., `VehicleMaster()`)
- ✅ Validate data quality (nulls, duplicates, date ranges)
- ✅ Use `pytest.mark.parametrize` for testing multiple tables
- ✅ Clean up test outputs in teardown fixtures

**DON'T**:
- ❌ Create mock/fake data (use real data samples)
- ❌ Skip testing because "data is too large" (use `.limit()`)
- ❌ Write tests that modify production tables
- ❌ Ignore schema validation
- ❌ Forget to test error handling with real edge cases

### 7. Example: Complete Test File

```python
# tests/test_silver_vehicle_master.py
import pytest
from pyspark.sql.functions import col, count, when
from python_files.silver.fvms.s_vehicle_master import VehicleMaster

class TestSilverVehicleMaster:
    """Test Silver layer VehicleMaster ETL with LIVE data"""

    @pytest.fixture(scope="class")
    def silver_df(self, spark):
        """Live Silver data - computed once per test class"""
        return spark.table("silver_fvms.s_vehicle_master")

    def test_all_required_columns_exist(self, silver_df):
        """Validate schema completeness"""
        required = ["vehicle_id", "hash_key", "load_timestamp", "registration_number"]
        missing = [col for col in required if col not in silver_df.columns]
        assert not missing, f"Missing columns: {missing}"

    def test_no_nulls_in_primary_key(self, silver_df):
        """Primary key cannot be null"""
        null_count = silver_df.filter(col("vehicle_id").isNull()).count()
        assert null_count == 0

    def test_hash_key_generated_for_all_rows(self, silver_df):
        """Every row must have hash_key"""
        total = silver_df.count()
        with_hash = silver_df.filter(col("hash_key").isNotNull()).count()
        assert total == with_hash

    @pytest.mark.slow
    def test_deduplication_effectiveness(self, spark):
        """Compare Bronze vs Silver row counts"""
        bronze = spark.table("bronze_fvms.b_vehicle_master")
        silver = spark.table("silver_fvms.s_vehicle_master")

        bronze_count = bronze.count()
        silver_count = silver.count()
        dedup_rate = (bronze_count - silver_count) / bronze_count * 100

        print(f"Deduplication removed {dedup_rate:.2f}% of rows")
        assert silver_count <= bronze_count
```

## Execution Workflow

1. **Read target file** ($ARGUMENTS) - Understand transformation logic
2. **Identify live data sources** - Find Bronze/Silver tables used
3. **Create test file** - `tests/test_<target>.py`
4. **Write fixtures** - Setup Spark session, load live data samples
5. **Write unit tests** - Test individual utility functions
6. **Write integration tests** - Test full ETL with live data
7. **Write validation tests** - Check data quality on live tables
8. **Run tests**: `pytest tests/test_<target>.py -v`
9. **Verify coverage**: Ensure >80% coverage of transformation logic

## Output Deliverables

- ✅ pytest test file with 10+ test cases
- ✅ conftest.py with reusable fixtures
- ✅ pytest.ini configuration
- ✅ Tests use LIVE data from Bronze/Silver/Gold
- ✅ All tests pass: `pytest -v`
- ✅ Documentation comments showing live data usage