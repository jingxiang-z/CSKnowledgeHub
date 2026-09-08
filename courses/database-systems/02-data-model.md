# 02 Data Model

## Table of Contents

1. [Overview](#overview)
2. [Extended Entity-Relationship Model](#extended-entity-relationship-model)
3. [E-R Diagram Notation](#e-r-diagram-notation)
4. [Relational Model](#relational-model)
5. [Relation Mapping](#relation-mapping)
7. [References](#references)

## Overview

Data modeling is the process of creating a conceptual representation of data structures and their relationships. The **Extended Entity-Relationship (E-R) Model** is a high-level conceptual model used during database design, while the **Relational Model** is the implementation model used in actual database systems.

This chapter covers both models and the transformation (mapping) between them.

## Extended Entity-Relationship Model

The E-R model provides a graphical representation of the logical structure of a database. It consists of entities, attributes, and relationships.

### Entity

**Entities** represent real-world objects, concepts, or things that are important to the database. They are typically nouns and have attributes that describe their properties.

**Characteristics:**
- Represent distinct objects or concepts
- Have unique identity
- Possess attributes
- Participate in relationships

**Examples:**
- Student
- Course
- Employee
- Department
- Product

### Attributes

**Attributes** are characteristics or properties of an entity that provide additional information.

#### Attribute Types

| Type | Description | Notation |
|------|-------------|----------|
| **Single-Valued** | Has only one value | Single ellipse |
| **Multi-Valued** | Can have multiple values | Double ellipse |
| **Composite** | Combines two or more properties | Ellipse with sub-ellipses |
| **Derived** | Calculated from other attributes | Dashed ellipse |
| **Key Attribute** | Uniquely identifies entity | Underlined |

**Examples:**

**Single-Valued:**
- StudentID (one ID per student)
- Name
- DateOfBirth

**Multi-Valued:**
- PhoneNumbers (a person may have multiple phones)
- EmailAddresses
- Skills

**Composite:**
- Address (Street, City, State, ZipCode)
- Name (FirstName, MiddleName, LastName)

**Derived:**
- Age (derived from DateOfBirth)
- TotalPrice (derived from Quantity × UnitPrice)

#### Union Entity

**Union types** represent attributes that can have multiple types. They are useful when an attribute's data type varies depending on context.

**Example:**
```
Payment (entity)
  PaymentMethod (union type)
    - CreditCard
    - BankAccount
    - DigitalWallet
```

### Relationships

**Relationships** represent associations or connections between entities, describing how entities interact with each other.

#### Cardinality

**Cardinality** defines the number of instances of one entity that can be related to instances of another entity.

| Cardinality | Description | Notation | Example |
|-------------|-------------|----------|---------|
| **One-to-One (1:1)** | Each instance relates to exactly one instance | 1 ---- 1 | Person ↔ Passport |
| **One-to-Many (1:N)** | One instance relates to many instances | 1 ---- N | Department ↔ Employees |
| **Many-to-Many (M:N)** | Multiple instances relate to multiple instances | M ---- N | Students ↔ Courses |

#### Relationship Types

**Binary Relationship:**
Connects two entities.
```
Student --- Enrolls --- Course
```

**N-ary (Ternary) Relationship:**
The relationship is defined between multiple entities simultaneously.

**Example:**
```
Student --- Enrolls --- Course
            |
          Professor
```
A student enrolls in a course taught by a specific professor.

**Identifying Relationship:**
The existence of a relationship depends on the existence of certain entities.

**Characteristics:**
- Primary key of child entity includes the primary key of parent entity
- Child entity is a **weak entity type**
- Represented with double diamond

**Example:**
```
Building (strong) --- Contains --- Room (weak)
Room's key: (BuildingID, RoomNumber)
```

**Recursive Relationship:**
An entity is related to itself through a relationship.

**Examples:**
- Employee --- Supervises --- Employee
- Course --- Prerequisite --- Course
- Person --- MarriedTo --- Person

### Constraints

Constraints ensure data integrity and enforce business rules.

#### Entity Integrity Constraint

The primary key attribute of an entity:
- Must have a unique value
- Cannot be null
- Uniquely identifies each instance

#### Referential Integrity Constraint

Foreign key values in a relationship must:
- Match the primary key values of the related entity, OR
- Be null (if allowed)

**Example:**
```sql
-- Orders table has CustomerID as foreign key
-- Every CustomerID in Orders must exist in Customers table
```

#### Domain Constraint

Values stored in an attribute must:
- Adhere to specific data types
- Follow format restrictions
- Fall within value restrictions

**Examples:**
- Age: INTEGER between 0 and 150
- Email: VARCHAR(255) matching email format
- Status: ENUM('active', 'inactive', 'suspended')

#### Cardinality Constraint

Specify the minimum and maximum number of occurrences allowed in a relationship.

**Notation:** (min, max)

**Examples:**
- (1, 1): Exactly one (mandatory, single)
- (0, 1): Zero or one (optional, single)
- (1, N): One or more (mandatory, multiple)
- (0, N): Zero or more (optional, multiple)

```
Employee (1,1) --- WorksIn --- (1,1) Department
Every employee works in exactly one department
Every department has at least one employee
```

#### Nullability Constraint

Determines whether an attribute can have null values or must have non-null values.

- **NOT NULL**: Attribute must always have a value
- **NULL allowed**: Attribute can be empty

### Inheritance

Inheritance allows entities to be organized in a hierarchy, where specialized entities (subtypes) inherit properties from general entities (supertypes).

#### Terminology

| Term | Definition |
|------|------------|
| **Supertype** | General entity with common attributes |
| **Subtype** | Specialized entity inheriting from supertype |
| **Specialization** | Top-down process: defining subtypes from a supertype |
| **Generalization** | Bottom-up process: creating a supertype from existing subtypes |

#### Example

```
Person (supertype)
  |
  +--- Student (subtype)
  |      - Major
  |      - GPA
  |
  +--- Employee (subtype)
         - Salary
         - HireDate
```

#### Inheritance Constraints

**Disjointness:**

| Type | Description | Example |
|------|-------------|---------|
| **Disjoint** | Subtypes are mutually exclusive | Person is Student XOR Employee |
| **Overlapping** | Subtypes can overlap | Person can be both Student AND Employee |

**Completeness:**

| Type | Description | Example |
|------|-------------|---------|
| **Total** | Every supertype instance must be a subtype | Every Vehicle is Car OR Truck OR Motorcycle |
| **Partial** | Supertype instances may not belong to any subtype | Person may or may not be Student/Employee |

## E-R Diagram Notation

E-R diagrams provide a visual representation of the database structure using standardized symbols.

### Basic Symbols

| Component | Symbol | Description |
|-----------|--------|-------------|
| **Entity** | Rectangle | Represents an entity type |
| **Weak Entity** | Double rectangle | Entity dependent on another entity |
| **Attribute** | Ellipse | Property of an entity |
| **Multi-valued Attribute** | Double ellipse | Attribute with multiple values |
| **Derived Attribute** | Dashed ellipse | Attribute calculated from others |
| **Key Attribute** | Underlined text | Primary key attribute |
| **Relationship** | Diamond | Association between entities |
| **Identifying Relationship** | Double diamond | Relationship identifying weak entity |

### Cardinality Notations

Different notations exist for expressing cardinality:

**Chen Notation:**
```
Entity1 ---- (1,N) ---- Relationship ---- (1,1) ---- Entity2
```

**Crow's Foot Notation:**
```
Entity1 ----<---- Relationship ----||---- Entity2
         many                      one
```

**Min-Max Notation:**
```
Entity1 --(1,N)-- Relationship --(0,1)-- Entity2
```

### Inheritance Symbols

| Symbol | Description |
|--------|-------------|
| **Solid line with triangle** | Specialization hierarchy (top-down) |
| **Dashed line with triangle** | Generalization hierarchy (bottom-up) |
| **d** inside triangle | Disjoint constraint |
| **o** inside triangle | Overlapping constraint |

### Additional Notations

**Ternary Relationship Notation:**
Represented by a diamond with lines connecting to three (or more) participating entities, with labels describing the nature of each connection.

**Union Type Notation:**
Represented by a circle or ellipse split into sections, each section corresponding to a possible type of the attribute.

**Attribute Inheritance Notation:**
A dashed line is drawn from the supertype's attribute to the subtype's attribute to show inheritance.

## Relational Model

The **Relational Model** organizes data into tables (relations) with rows (tuples) and columns (attributes). It provides a mathematical foundation for database operations.

### Core Components

| Component | Description | Also Known As |
|-----------|-------------|---------------|
| **Relation** | A table with rows and columns | Table |
| **Tuple** | A single row in a relation | Row, Record |
| **Attribute** | A column in a relation | Column, Field |
| **Domain** | Set of allowed values for an attribute | Data Type |
| **Degree** | Number of attributes in a relation | Arity |
| **Cardinality** | Number of tuples in a relation | Row Count |

### Properties of Relations

1. **No duplicate tuples**: Each tuple is unique
2. **Unordered tuples**: No inherent ordering of rows
3. **Unordered attributes**: Column order doesn't matter (though fixed in practice)
4. **Atomic values**: Each attribute contains a single, indivisible value
5. **Same domain**: All values in a column are from the same domain

### Keys

**Keys** uniquely identify tuples in a relation.

| Key Type | Definition |
|----------|------------|
| **Superkey** | Any set of attributes that uniquely identifies tuples |
| **Candidate Key** | Minimal superkey (no proper subset is a superkey) |
| **Primary Key** | Chosen candidate key for tuple identification |
| **Foreign Key** | Attribute(s) referencing primary key in another relation |
| **Composite Key** | Primary key consisting of multiple attributes |

**Example:**

```sql
Students(StudentID, Email, Name, Major)
- StudentID: Primary key
- Email: Candidate key (also unique)
- (Name, Major): Neither is a key (not unique)

Enrollments(StudentID, CourseID, Grade)
- (StudentID, CourseID): Composite primary key
- StudentID: Foreign key referencing Students
- CourseID: Foreign key referencing Courses
```

### Relationships in Relational Model

Relationships are established through the use of **foreign keys** that reference primary keys.

## Relation Mapping

**Relation Mapping** is the process of transforming an E-R model into a relational schema. This systematic process ensures that all entities, attributes, and relationships are properly represented.

### Entity Types Mapping

#### Basic Entity Mapping

Each entity type in the E-R model corresponds to a relation in the relational model.

**E-R Model:**
```
Student(StudentID, Name, Email, Major)
```

**Relational Model:**
```sql
CREATE TABLE Student (
    StudentID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(255) UNIQUE,
    Major VARCHAR(50)
);
```

**Rules:**
1. Relation has the same name as entity type
2. If entity has an identifying property, it becomes the primary key
3. Other properties become attributes

#### Composite Property Types

If an entity type has a composite property type composed of multiple sub-properties, the sub-properties become separate attributes in the relation.

**E-R Model:**
```
Employee(EmployeeID, Name, Address)
Address: (Street, City, State, ZipCode)
```

**Relational Model:**
```sql
CREATE TABLE Employee (
    EmployeeID INT PRIMARY KEY,
    Name VARCHAR(100),
    Street VARCHAR(200),
    City VARCHAR(100),
    State CHAR(2),
    ZipCode VARCHAR(10)
);
```

**Note:** The composite property itself (Address) is lost; only sub-properties remain.

#### Multi-Valued Property Types

The relational model does not directly support multi-valued attributes. A separate relation must be created.

**E-R Model:**
```
Employee(EmployeeID, Name, Skills)
Skills is multi-valued
```

**Relational Model:**
```sql
CREATE TABLE Employee (
    EmployeeID INT PRIMARY KEY,
    Name VARCHAR(100)
);

CREATE TABLE EmployeeSkills (
    EmployeeID INT,
    Skill VARCHAR(100),
    PRIMARY KEY (EmployeeID, Skill),
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
);
```

### Relationship Mapping

#### One-to-One Relationships (1:1)

For a 1:1 relationship between entity types ET1 and ET2, a foreign key can be added in either ET1 or ET2.

**Strategy:** Place foreign key in the relation representing the entity with total participation (if one exists), or choose arbitrarily.

**Example:**
```
Employee (1,1) --- Manages --- (0,1) Department
```

**Relational Model:**
```sql
CREATE TABLE Employee (
    EmployeeID INT PRIMARY KEY,
    Name VARCHAR(100)
);

CREATE TABLE Department (
    DepartmentID INT PRIMARY KEY,
    Name VARCHAR(100),
    ManagerID INT UNIQUE,  -- Foreign key to Employee
    FOREIGN KEY (ManagerID) REFERENCES Employee(EmployeeID)
);
```

#### One-to-Many Relationships (1:N)

In a 1:N relationship where one instance of ET1 relates to many instances of ET2, the foreign key should be added in ET2 (the "many" side).

**Example:**
```
Department (1,N) --- Has --- (1,1) Employee
```

**Relational Model:**
```sql
CREATE TABLE Department (
    DepartmentID INT PRIMARY KEY,
    Name VARCHAR(100)
);

CREATE TABLE Employee (
    EmployeeID INT PRIMARY KEY,
    Name VARCHAR(100),
    DepartmentID INT NOT NULL,  -- Foreign key
    FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID)
);
```

#### Many-to-Many Relationships (M:N)

In an M:N relationship, a separate relation R is created to represent the relationship. R contains foreign keys referencing the primary keys of both ET1 and ET2.

**Example:**
```
Student (M,N) --- Enrolls --- (M,N) Course
```

**Relational Model:**
```sql
CREATE TABLE Student (
    StudentID INT PRIMARY KEY,
    Name VARCHAR(100)
);

CREATE TABLE Course (
    CourseID INT PRIMARY KEY,
    Title VARCHAR(200)
);

CREATE TABLE Enrollment (
    StudentID INT,
    CourseID INT,
    Grade CHAR(2),
    PRIMARY KEY (StudentID, CourseID),
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID)
);
```

### Inheritance Mapping

Different strategies exist for mapping inheritance hierarchies, depending on the constraints.

#### Strategy 1: Mandatory Disjoint

**Constraints:** Total participation, disjoint subtypes

**Approach:** Create separate relations for each subtype, each inheriting the supertype's primary key and attributes.

**E-R Model:**
```
Person(PersonID, Name)
  |
  +--- Student(GPA, Major)
  +--- Employee(Salary, HireDate)
```

**Relational Model:**
```sql
-- No Person table created

CREATE TABLE Student (
    PersonID INT PRIMARY KEY,  -- Inherited
    Name VARCHAR(100),         -- Inherited
    GPA DECIMAL(3,2),
    Major VARCHAR(50)
);

CREATE TABLE Employee (
    PersonID INT PRIMARY KEY,  -- Inherited
    Name VARCHAR(100),         -- Inherited
    Salary DECIMAL(10,2),
    HireDate DATE
);
```

**Advantages:** No redundant data, simple queries for subtypes
**Disadvantages:** Queries involving all persons require UNION

#### Strategy 2: Mandatory, Overlap Allowed

**Constraints:** Total participation, overlapping subtypes

**Approach:** Create a single relation for the supertype with all subtype attributes. Include a type indicator.

**E-R Model:**
```
Person(PersonID, Name)
  |
  +--- Student(GPA, Major)
  +--- Employee(Salary, HireDate)
```

**Relational Model:**
```sql
CREATE TABLE Person (
    PersonID INT PRIMARY KEY,
    Name VARCHAR(100),
    Type VARCHAR(20),  -- 'Student', 'Employee', 'Both'
    GPA DECIMAL(3,2),
    Major VARCHAR(50),
    Salary DECIMAL(10,2),
    HireDate DATE
);
```

**Advantages:** Single table for all persons, allows overlap
**Disadvantages:** Many NULL values, potential data integrity issues

#### Strategy 3: Non-Mandatory, Overlap Allowed

**Constraints:** Partial participation, overlapping subtypes

**Approach:** Create relation for supertype and separate relations for each subtype.

**Relational Model:**
```sql
CREATE TABLE Person (
    PersonID INT PRIMARY KEY,
    Name VARCHAR(100)
);

CREATE TABLE Student (
    PersonID INT PRIMARY KEY,
    GPA DECIMAL(3,2),
    Major VARCHAR(50),
    FOREIGN KEY (PersonID) REFERENCES Person(PersonID)
);

CREATE TABLE Employee (
    PersonID INT PRIMARY KEY,
    Salary DECIMAL(10,2),
    HireDate DATE,
    FOREIGN KEY (PersonID) REFERENCES Person(PersonID)
);
```

**Advantages:** Flexible, supports partial participation and overlap
**Disadvantages:** Requires joins to get complete information

#### Strategy 4: Non-Mandatory, Disjoint

**Constraints:** Partial participation, disjoint subtypes

**Approach:** Create separate relations for supertype and each subtype. Subtypes reference supertype.

**Relational Model:**
```sql
CREATE TABLE Person (
    PersonID INT PRIMARY KEY,
    Name VARCHAR(100)
);

CREATE TABLE Student (
    PersonID INT PRIMARY KEY,
    GPA DECIMAL(3,2),
    Major VARCHAR(50),
    FOREIGN KEY (PersonID) REFERENCES Person(PersonID) ON DELETE CASCADE
);

CREATE TABLE Employee (
    PersonID INT PRIMARY KEY,
    Salary DECIMAL(10,2),
    HireDate DATE,
    FOREIGN KEY (PersonID) REFERENCES Person(PersonID) ON DELETE CASCADE
);
```

**Advantages:** Clear separation, supports partial participation
**Disadvantages:** Complex queries requiring multiple joins

### Union Type Mapping

For union types, create a relation for the union entity with an artificial identifier.

**E-R Model:**
```
Vehicle (union of Car, Truck)
  VehicleID (artificial identifier)
  LicensePlate
```

**Relational Model:**
```sql
CREATE TABLE Car (
    CarID INT PRIMARY KEY,
    Model VARCHAR(100)
);

CREATE TABLE Truck (
    TruckID INT PRIMARY KEY,
    Capacity INT
);

CREATE TABLE Vehicle (
    VehicleID INT PRIMARY KEY,
    LicensePlate VARCHAR(20),
    SourceType VARCHAR(10),  -- 'Car' or 'Truck'
    SourceID INT  -- References either CarID or TruckID
);
```

**Note:** This approach has limitations in enforcing referential integrity. Modern databases may use table inheritance or other advanced features.

## References

**Course Materials:**
- CS 6400: Database Systems Concepts and Design - Georgia Tech OMSCS
