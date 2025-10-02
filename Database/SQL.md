## Structured Query Language

- Data Manipulation Language (DML): SELECT, INSERT, UPDATE, and DELETE statements.
- Data Definition Language (DDL): Schema definitions for tables, indexes, views, and other objects.
- Data Control Language (DCL): Security, access controls.

### Aggregates

Types of Aggregates Functions:

- AVG(COL): The average of the values in COL
- MIN(COL): The minimum value in COL
- MAX(COL): The maximum value in COL
- COUNT(COL): The number of tuples in the relation

DISTINCT keyword: select different results

Non-aggregated values in SELECT output clause must appear in GROUP BY clause.

The HAVING clause filters output results based on aggregation computation. This make HAVING behave like a WHERE clause for a GROUP BY.

### String

The SQL standard says that strings are case sensitive and single-quotes only.

- Pattern Matching: The LIKE keyword is used for string matching in predicates. '%' matches any substrings, '_' matches any one character
- Concatenation: Two vertical bars (“||”) will concatenate two or more strings together into a single string.
- String Functions: Many database systems implement other functions in addition to those in the standard. Examples of standard string functions include SUBSTRING(S, B, E) and UPPER(S).

### Output Control

- ORDER BY: impose a sort on tuples, ASC for ascending results, DESC for descending results
- LIMIT: restrict the number of result tuples, use OFFSET to return a range in the results

### Nested Query

- ALL: Must satisfy expression for all rows in sub-query.
- ANY: Must satisfy expression for at least one row in sub-query.
- IN: Equivalent to =ANY().
- EXISTS: At least one row is returned.

### Window Function

- ROW NUMBER: assigns a number to each row in order, regardless of any ties
- RANK: assigns same rank to ties, and skips ahead to next number in position
- DENSE_RANK: assigns same rank to ties, but continues with the sequence
- PARTITION BY: Use PARTITION BY to specify group.
- ORDER BY: ORDER BY within OVER to ensure a deterministic ordering of results even if database changes internally.

### Common Table Expressions

CTEs can be thought of as a temporary table that is scoped to a single query.

WITH clause binds the output of the inner query to a temporary result with that name.

Adding the RECURSIVE keyword after WITH allows a CTE to reference itself.