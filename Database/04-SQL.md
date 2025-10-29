# 04 SQL

## Table of Contents

1. [Overview](#overview)
2. [SQL Language Categories](#sql-language-categories)
3. [Aggregate Functions](#aggregate-functions)
4. [String Operations](#string-operations)
5. [Output Control](#output-control)
6. [Nested Queries](#nested-queries)
7. [Window Functions](#window-functions)
8. [Common Table Expressions](#common-table-expressions)
10. [References](#references)

## Overview

**SQL (Structured Query Language)** is the standard language for interacting with relational database systems. It provides a declarative approach to data manipulation, allowing users to specify *what* data they want without detailing *how* to retrieve it.

### Key Characteristics

- **Declarative**: Specify the desired result, not the procedure
- **Set-Based**: Operates on sets of rows rather than individual records
- **Standardized**: ANSI/ISO standard with vendor-specific extensions
- **Comprehensive**: Covers data definition, manipulation, and control

### SQL Standards

| Standard | Year | Key Features |
|----------|------|--------------|
| **SQL-86** | 1986 | Initial standard |
| **SQL-89** | 1989 | Integrity constraints |
| **SQL-92** | 1992 | Joins, schema manipulation |
| **SQL:1999** | 1999 | Triggers, recursive queries, procedural extensions |
| **SQL:2003** | 2003 | Window functions, XML |
| **SQL:2016** | 2016 | JSON support, pattern matching |

## SQL Language Categories

SQL is divided into distinct categories based on functionality:

### Data Manipulation Language (DML)

**Purpose:** Query and modify data

| Statement | Operation | Description |
|-----------|-----------|-------------|
| **SELECT** | Query | Retrieve data from tables |
| **INSERT** | Create | Add new rows to a table |
| **UPDATE** | Modify | Change existing data |
| **DELETE** | Remove | Delete rows from a table |

**Example:**
```sql
-- Query data
SELECT name, salary FROM employees WHERE department = 'Engineering';

-- Insert data
INSERT INTO employees (id, name, department, salary)
VALUES (101, 'Alice', 'Engineering', 75000);

-- Update data
UPDATE employees SET salary = 80000 WHERE id = 101;

-- Delete data
DELETE FROM employees WHERE id = 101;
```

### Data Definition Language (DDL)

**Purpose:** Define and modify database structure

| Statement | Operation | Description |
|-----------|-----------|-------------|
| **CREATE** | Define | Create databases, tables, indexes, views |
| **ALTER** | Modify | Change structure of existing objects |
| **DROP** | Remove | Delete database objects |
| **TRUNCATE** | Clear | Remove all rows from a table (faster than DELETE) |

**Example:**
```sql
-- Create table
CREATE TABLE employees (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(50),
    salary DECIMAL(10, 2)
);

-- Alter table
ALTER TABLE employees ADD COLUMN hire_date DATE;

-- Create index
CREATE INDEX idx_department ON employees(department);

-- Create view
CREATE VIEW engineering_staff AS
SELECT id, name, salary FROM employees WHERE department = 'Engineering';

-- Drop table
DROP TABLE employees;
```

### Data Control Language (DCL)

**Purpose:** Control access to data

| Statement | Operation | Description |
|-----------|-----------|-------------|
| **GRANT** | Allow | Give privileges to users |
| **REVOKE** | Deny | Remove privileges from users |

**Example:**
```sql
-- Grant privileges
GRANT SELECT, INSERT ON employees TO user_alice;

-- Revoke privileges
REVOKE INSERT ON employees FROM user_alice;

-- Grant all privileges
GRANT ALL PRIVILEGES ON DATABASE company TO admin_user;
```

### Transaction Control Language (TCL)

**Purpose:** Manage transactions

| Statement | Operation | Description |
|-----------|-----------|-------------|
| **BEGIN/START** | Start | Begin a transaction |
| **COMMIT** | Finalize | Save changes permanently |
| **ROLLBACK** | Undo | Revert changes to last commit |
| **SAVEPOINT** | Checkpoint | Set a point to rollback to |

**Example:**
```sql
-- Transaction example
BEGIN TRANSACTION;

UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
UPDATE accounts SET balance = balance + 100 WHERE account_id = 2;

COMMIT;  -- If successful

-- Or ROLLBACK if error occurred
```

## Aggregate Functions

**Aggregate functions** compute a single result from a set of input values.

### Common Aggregate Functions

| Function | Description | Handles NULL |
|----------|-------------|--------------|
| **COUNT(col)** | Number of non-NULL values | Ignores NULL |
| **COUNT(*)** | Number of rows | Counts all rows |
| **SUM(col)** | Sum of values | Ignores NULL |
| **AVG(col)** | Average of values | Ignores NULL |
| **MIN(col)** | Minimum value | Ignores NULL |
| **MAX(col)** | Maximum value | Ignores NULL |

### Basic Usage

```sql
-- Count employees
SELECT COUNT(*) AS total_employees FROM employees;

-- Average salary
SELECT AVG(salary) AS avg_salary FROM employees;

-- Min and max salary
SELECT MIN(salary) AS min_sal, MAX(salary) AS max_sal FROM employees;

-- Sum of all salaries
SELECT SUM(salary) AS total_payroll FROM employees;
```

### DISTINCT Keyword

**Purpose:** Select only unique values

```sql
-- Count unique departments
SELECT COUNT(DISTINCT department) AS num_departments FROM employees;

-- Get unique departments
SELECT DISTINCT department FROM employees;

-- Multiple columns (unique combinations)
SELECT DISTINCT department, job_title FROM employees;
```

### GROUP BY Clause

**Purpose:** Group rows with the same values for aggregation

**Rule:** Non-aggregated columns in SELECT must appear in GROUP BY

```sql
-- Employees per department
SELECT department, COUNT(*) AS emp_count
FROM employees
GROUP BY department;

-- Average salary per department and job title
SELECT department, job_title, AVG(salary) AS avg_salary
FROM employees
GROUP BY department, job_title;

-- Total sales per year and quarter
SELECT YEAR(sale_date) AS year,
       QUARTER(sale_date) AS quarter,
       SUM(amount) AS total_sales
FROM sales
GROUP BY YEAR(sale_date), QUARTER(sale_date);
```

### HAVING Clause

**Purpose:** Filter groups based on aggregate conditions

**Difference from WHERE:**
- **WHERE** filters rows *before* grouping
- **HAVING** filters groups *after* aggregation

```sql
-- Departments with more than 10 employees
SELECT department, COUNT(*) AS emp_count
FROM employees
GROUP BY department
HAVING COUNT(*) > 10;

-- Departments with average salary above 70000
SELECT department, AVG(salary) AS avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 70000;

-- Combine WHERE and HAVING
SELECT department, AVG(salary) AS avg_salary
FROM employees
WHERE hire_date >= '2020-01-01'  -- Filter rows first
GROUP BY department
HAVING AVG(salary) > 60000;      -- Filter groups second
```

### Complete Query Structure

```sql
SELECT column1, AGG_FUNC(column2) AS alias
FROM table
WHERE condition                    -- Filter rows before grouping
GROUP BY column1                   -- Group rows
HAVING AGG_FUNC(column2) > value  -- Filter groups after aggregation
ORDER BY column1                   -- Sort results
LIMIT n;                          -- Limit number of results
```

## String Operations

SQL provides rich string manipulation capabilities.

### String Standards

**SQL Standard:**
- Strings are **case sensitive**
- Use **single quotes** only: `'text'`
- Double quotes for identifiers (column/table names)

**Vendor Variations:**
- MySQL: Case insensitive by default, allows double quotes for strings
- PostgreSQL: Case sensitive, follows standard strictly
- SQL Server: Case sensitivity depends on collation

### Pattern Matching with LIKE

**LIKE** operator matches patterns in strings.

**Wildcards:**
- **%** : Matches any substring (including empty string)
- **_** : Matches exactly one character

```sql
-- Names starting with 'A'
SELECT name FROM employees WHERE name LIKE 'A%';

-- Names ending with 'son'
SELECT name FROM employees WHERE name LIKE '%son';

-- Names containing 'ann'
SELECT name FROM employees WHERE name LIKE '%ann%';

-- Exactly 5 characters
SELECT name FROM employees WHERE name LIKE '_____';

-- Second letter is 'a'
SELECT name FROM employees WHERE name LIKE '_a%';

-- Pattern with both wildcards
SELECT email FROM users WHERE email LIKE '%@gmail.%';

-- Case insensitive (PostgreSQL)
SELECT name FROM employees WHERE name ILIKE 'alice%';
```

### String Concatenation

**Operator:** `||` (SQL standard)

**Vendor Alternatives:**
- MySQL: `CONCAT()` function
- SQL Server: `+` operator

```sql
-- Standard concatenation
SELECT first_name || ' ' || last_name AS full_name FROM employees;

-- With NULL handling (COALESCE)
SELECT first_name || ' ' || COALESCE(middle_name || ' ', '') || last_name
AS full_name FROM employees;

-- MySQL
SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM employees;

-- SQL Server
SELECT first_name + ' ' + last_name AS full_name FROM employees;
```

### String Functions

| Function | Description | Example |
|----------|-------------|---------|
| **SUBSTRING(S, B, E)** | Extract substring from position B, length E | `SUBSTRING('Hello', 1, 3)` → 'Hel' |
| **UPPER(S)** | Convert to uppercase | `UPPER('hello')` → 'HELLO' |
| **LOWER(S)** | Convert to lowercase | `LOWER('HELLO')` → 'hello' |
| **LENGTH(S)** | String length | `LENGTH('hello')` → 5 |
| **TRIM(S)** | Remove leading/trailing spaces | `TRIM('  hello  ')` → 'hello' |
| **REPLACE(S, F, R)** | Replace F with R in S | `REPLACE('hello', 'l', 'x')` → 'hexxo' |

**Examples:**
```sql
-- Extract domain from email
SELECT SUBSTRING(email, POSITION('@' IN email) + 1) AS domain
FROM users;

-- Standardize names to title case
SELECT UPPER(SUBSTRING(name, 1, 1)) || LOWER(SUBSTRING(name, 2)) AS proper_name
FROM employees;

-- Find string length
SELECT name, LENGTH(name) AS name_length FROM employees;

-- Remove extra spaces
SELECT TRIM(address) AS clean_address FROM customers;
```

## Output Control

### ORDER BY Clause

**Purpose:** Sort query results

**Syntax:**
```sql
ORDER BY column1 [ASC|DESC], column2 [ASC|DESC], ...
```

- **ASC**: Ascending order (default)
- **DESC**: Descending order

**Examples:**
```sql
-- Sort by salary ascending
SELECT name, salary FROM employees ORDER BY salary;

-- Sort by salary descending
SELECT name, salary FROM employees ORDER BY salary DESC;

-- Multiple columns
SELECT department, name, salary
FROM employees
ORDER BY department ASC, salary DESC;

-- Order by expression
SELECT name, salary, salary * 1.1 AS projected_salary
FROM employees
ORDER BY salary * 1.1 DESC;

-- Order by column position (not recommended)
SELECT name, salary FROM employees ORDER BY 2 DESC;

-- NULL handling
SELECT name, bonus FROM employees ORDER BY bonus NULLS LAST;
```

### LIMIT and OFFSET

**Purpose:** Restrict the number of rows returned

**Syntax:**
```sql
LIMIT n [OFFSET m]
```

- **LIMIT n**: Return at most n rows
- **OFFSET m**: Skip first m rows

**Examples:**
```sql
-- Top 5 highest paid employees
SELECT name, salary FROM employees
ORDER BY salary DESC
LIMIT 5;

-- Pagination: rows 11-20
SELECT name, salary FROM employees
ORDER BY name
LIMIT 10 OFFSET 10;

-- Second page of 25 records
SELECT * FROM products
ORDER BY product_id
LIMIT 25 OFFSET 25;
```

**Vendor Variations:**
```sql
-- SQL Server / Access
SELECT TOP 5 name, salary FROM employees ORDER BY salary DESC;

-- Oracle
SELECT * FROM (
    SELECT name, salary FROM employees ORDER BY salary DESC
) WHERE ROWNUM <= 5;

-- SQL Server (modern)
SELECT name, salary FROM employees
ORDER BY salary DESC
OFFSET 0 ROWS FETCH NEXT 5 ROWS ONLY;
```

## Nested Queries

**Nested queries** (subqueries) are queries within queries, enabling complex data retrieval.

### Subquery Operators

| Operator | Description | Returns True When |
|----------|-------------|-------------------|
| **IN** | Equal to any value | Value matches any in subquery (equivalent to = ANY) |
| **NOT IN** | Not equal to any value | Value doesn't match any in subquery |
| **EXISTS** | Subquery returns rows | At least one row returned |
| **NOT EXISTS** | Subquery returns no rows | No rows returned |
| **ANY** | Compare to any value | Condition true for at least one row |
| **ALL** | Compare to all values | Condition true for all rows |

### IN Operator

```sql
-- Employees in specific departments
SELECT name, department FROM employees
WHERE department IN ('Engineering', 'Sales', 'Marketing');

-- Employees in departments with more than 50 people (subquery)
SELECT name, department FROM employees
WHERE department IN (
    SELECT department FROM employees
    GROUP BY department
    HAVING COUNT(*) > 50
);

-- NOT IN
SELECT name FROM employees
WHERE department NOT IN ('HR', 'Admin');
```

### EXISTS Operator

**Characteristics:**
- Returns TRUE/FALSE (not data)
- Stops as soon as match is found (efficient)
- Better performance than IN for large datasets

```sql
-- Departments that have employees
SELECT department_name FROM departments d
WHERE EXISTS (
    SELECT 1 FROM employees e
    WHERE e.department_id = d.id
);

-- Employees who have made sales
SELECT name FROM employees e
WHERE EXISTS (
    SELECT 1 FROM sales s
    WHERE s.employee_id = e.id
);

-- NOT EXISTS (employees with no sales)
SELECT name FROM employees e
WHERE NOT EXISTS (
    SELECT 1 FROM sales s
    WHERE s.employee_id = e.id
);
```

### ANY Operator

**Syntax:** `value operator ANY (subquery)`

**Operators:** `=, <>, <, <=, >, >=`

```sql
-- Salary greater than any salary in HR department
SELECT name, salary FROM employees
WHERE salary > ANY (
    SELECT salary FROM employees
    WHERE department = 'HR'
);

-- Equal to any (equivalent to IN)
SELECT name FROM employees
WHERE department = ANY (
    SELECT department FROM departments WHERE location = 'New York'
);
```

### ALL Operator

**Syntax:** `value operator ALL (subquery)`

```sql
-- Salary greater than all salaries in HR department
SELECT name, salary FROM employees
WHERE salary > ALL (
    SELECT salary FROM employees
    WHERE department = 'HR'
);

-- Not equal to all (equivalent to NOT IN)
SELECT name FROM employees
WHERE department <> ALL ('HR', 'Admin');
```

### Scalar Subqueries

**Return single value** (one row, one column)

```sql
-- Employees earning more than average
SELECT name, salary FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);

-- Salary difference from average
SELECT name,
       salary,
       salary - (SELECT AVG(salary) FROM employees) AS diff_from_avg
FROM employees;
```

### Correlated Subqueries

**Subquery references outer query** (executed once per row)

```sql
-- Employees earning more than their department average
SELECT e1.name, e1.department, e1.salary
FROM employees e1
WHERE e1.salary > (
    SELECT AVG(e2.salary)
    FROM employees e2
    WHERE e2.department = e1.department
);

-- Products with above-average price in their category
SELECT p1.product_name, p1.category, p1.price
FROM products p1
WHERE p1.price > (
    SELECT AVG(p2.price)
    FROM products p2
    WHERE p2.category = p1.category
);
```

## Window Functions

**Window functions** perform calculations across a set of rows related to the current row, without collapsing rows like GROUP BY.

### Key Concepts

- **Window**: Set of rows related to current row
- **Partition**: Divide rows into groups
- **Order**: Define sequence within partition
- **Frame**: Subset of partition relative to current row

### Ranking Functions

| Function | Description | Handling Ties |
|----------|-------------|---------------|
| **ROW_NUMBER()** | Sequential number | Different numbers for ties |
| **RANK()** | Rank with gaps | Same rank, skip next numbers |
| **DENSE_RANK()** | Rank without gaps | Same rank, continue sequence |
| **NTILE(n)** | Divide into n buckets | Distribute as evenly as possible |

**Examples:**
```sql
-- Row number (always unique)
SELECT name, salary,
       ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num
FROM employees;

-- Rank with gaps
SELECT name, salary,
       RANK() OVER (ORDER BY salary DESC) AS rank
FROM employees;
-- Salary 100k, 100k, 90k → Ranks: 1, 1, 3

-- Dense rank without gaps
SELECT name, salary,
       DENSE_RANK() OVER (ORDER BY salary DESC) AS dense_rank
FROM employees;
-- Salary 100k, 100k, 90k → Ranks: 1, 1, 2

-- Quartiles
SELECT name, salary,
       NTILE(4) OVER (ORDER BY salary) AS quartile
FROM employees;
```

### PARTITION BY

**Purpose:** Divide result set into partitions for separate calculations

```sql
-- Rank within each department
SELECT name, department, salary,
       RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dept_rank
FROM employees;

-- Row number per department
SELECT name, department, hire_date,
       ROW_NUMBER() OVER (PARTITION BY department ORDER BY hire_date) AS hire_order
FROM employees;

-- Highest paid in each department
WITH ranked AS (
    SELECT name, department, salary,
           RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rank
    FROM employees
)
SELECT name, department, salary
FROM ranked
WHERE rank = 1;
```

### Aggregate Window Functions

**Difference from GROUP BY:**
- Window functions keep all rows
- GROUP BY collapses rows

```sql
-- Running total
SELECT date, amount,
       SUM(amount) OVER (ORDER BY date) AS running_total
FROM sales;

-- Average by department (without collapsing rows)
SELECT name, department, salary,
       AVG(salary) OVER (PARTITION BY department) AS dept_avg_salary
FROM employees;

-- Difference from department average
SELECT name, department, salary,
       salary - AVG(salary) OVER (PARTITION BY department) AS diff_from_avg
FROM employees;
```

### Offset Functions

| Function | Description |
|----------|-------------|
| **LAG(col, n)** | Value from n rows before |
| **LEAD(col, n)** | Value from n rows after |
| **FIRST_VALUE(col)** | First value in window |
| **LAST_VALUE(col)** | Last value in window |

```sql
-- Previous and next salary
SELECT name, salary,
       LAG(salary, 1) OVER (ORDER BY salary) AS prev_salary,
       LEAD(salary, 1) OVER (ORDER BY salary) AS next_salary
FROM employees;

-- Month-over-month change
SELECT month, revenue,
       revenue - LAG(revenue, 1) OVER (ORDER BY month) AS monthly_change
FROM monthly_revenue;

-- First and last in partition
SELECT name, department, salary,
       FIRST_VALUE(name) OVER (PARTITION BY department ORDER BY salary DESC) AS highest_paid,
       LAST_VALUE(name) OVER (PARTITION BY department ORDER BY salary DESC) AS lowest_paid
FROM employees;
```

### Window Frame Specification

**Syntax:**
```sql
OVER (
    PARTITION BY column
    ORDER BY column
    ROWS|RANGE BETWEEN frame_start AND frame_end
)
```

**Frame Bounds:**
- `UNBOUNDED PRECEDING`: Start of partition
- `n PRECEDING`: n rows before current
- `CURRENT ROW`: Current row
- `n FOLLOWING`: n rows after current
- `UNBOUNDED FOLLOWING`: End of partition

```sql
-- Moving average (3-row window)
SELECT date, amount,
       AVG(amount) OVER (
           ORDER BY date
           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
       ) AS moving_avg_3
FROM sales;

-- Cumulative sum
SELECT date, amount,
       SUM(amount) OVER (
           ORDER BY date
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS cumulative_sum
FROM sales;
```

## Common Table Expressions

**Common Table Expressions (CTEs)** create temporary named result sets that exist only during query execution.

### Basic CTE Syntax

```sql
WITH cte_name AS (
    SELECT ...
)
SELECT * FROM cte_name;
```

### Simple CTE Examples

```sql
-- Department averages
WITH dept_avg AS (
    SELECT department, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department
)
SELECT e.name, e.department, e.salary, d.avg_salary
FROM employees e
JOIN dept_avg d ON e.department = d.department
WHERE e.salary > d.avg_salary;

-- Multiple CTEs
WITH
sales_summary AS (
    SELECT product_id, SUM(quantity) AS total_sold
    FROM sales
    GROUP BY product_id
),
inventory_summary AS (
    SELECT product_id, SUM(quantity) AS total_stock
    FROM inventory
    GROUP BY product_id
)
SELECT p.product_name,
       s.total_sold,
       i.total_stock,
       i.total_stock - s.total_sold AS remaining
FROM products p
JOIN sales_summary s ON p.id = s.product_id
JOIN inventory_summary i ON p.id = i.product_id;
```

### Advantages of CTEs

| Advantage | Description |
|-----------|-------------|
| **Readability** | Break complex queries into logical steps |
| **Reusability** | Reference CTE multiple times in same query |
| **Recursion** | Enable recursive queries |
| **Maintenance** | Easier to debug and modify |

### Recursive CTEs

**Purpose:** Query hierarchical or tree-structured data

**Syntax:**
```sql
WITH RECURSIVE cte_name AS (
    -- Base case (anchor member)
    SELECT ...

    UNION ALL

    -- Recursive case (recursive member)
    SELECT ... FROM cte_name WHERE ...
)
SELECT * FROM cte_name;
```

**Examples:**

**Organization Hierarchy:**
```sql
-- Employee hierarchy
WITH RECURSIVE employee_hierarchy AS (
    -- Base: Top-level employees (no manager)
    SELECT id, name, manager_id, 1 AS level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive: Employees managed by previous level
    SELECT e.id, e.name, e.manager_id, eh.level + 1
    FROM employees e
    JOIN employee_hierarchy eh ON e.manager_id = eh.id
)
SELECT * FROM employee_hierarchy
ORDER BY level, name;
```

**Number Series:**
```sql
-- Generate numbers 1 to 10
WITH RECURSIVE numbers AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1 FROM numbers WHERE n < 10
)
SELECT * FROM numbers;
```

**Path Finding:**
```sql
-- Find all paths in a graph
WITH RECURSIVE paths AS (
    -- Base: Direct connections from starting node
    SELECT source, target, ARRAY[source, target] AS path
    FROM edges
    WHERE source = 'A'

    UNION ALL

    -- Recursive: Extend paths
    SELECT p.source, e.target, p.path || e.target
    FROM paths p
    JOIN edges e ON p.target = e.source
    WHERE NOT e.target = ANY(p.path)  -- Avoid cycles
)
SELECT * FROM paths;
```

**Date Series:**
```sql
-- Generate date range
WITH RECURSIVE date_series AS (
    SELECT DATE '2024-01-01' AS date
    UNION ALL
    SELECT date + INTERVAL '1 day'
    FROM date_series
    WHERE date < DATE '2024-01-31'
)
SELECT * FROM date_series;
```

## References

**Course Materials:**
- CS 6400: Database Systems Concepts and Design - Georgia Tech OMSCS
