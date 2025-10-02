[toc]

## Extended Entity-Relationship Model

### Entity

- Entities represent real-world objects, concepts, or things that are important to the database. They are typically nouns and have attributes that describe their properties.
- Attributes are characteristics or properties of an entity. They provide additional information about the entity. 
  - Single-valued property: only has single value, represented by an ellipsis
  - Multi-valued property: can have more than one value. We represent these property types with a double ellipsis
  - Composite property: combine two or more property types to create composite property types
- Union Entity: Union types represent attributes that can have multiple types.

### Relationship

- Relationships represent associations or connections between entities. They describe how entities interact or are related to each other

- Cardinality: Cardinality defines the number of instances of one entity that can be related to instances of another entity in a relationship
  - One-to-One: each instance of one entity is associated with exactly one instance of another entity
  - One-to-Many:  each instance of one entity can be associated with multiple instances of another entity, but each instance of the second entity is associated with only one instance of the first entity
  - Many-to-Many: multiple instances of one entity can be associated with multiple instances of another entity
  - N-ary (ternary): the relationship is defined between multiple entities simultaneously; For example, a student enrolls in a course taught by a specific professor
  - Identifying relationship:  the existence of a relationship depends on the existence of certain entities; the primary key of the child entity includes the primary key of the parent entity as part of its own primary key; the child entity is a weak entity type
  - Recursive relationship: an entity is related to itself through a relationship

### Constraint

- Entity Integrity Constraint: the primary key attribute of an entity must have a unique value and cannot be null
- Referential Integrity Constraint: foreign key values in a relationship must match the primary key values of the related entity or be null
- Domain Constraint: the values stored in an attribute adhere to specific data types, formats, or value restrictions
- Caridinality Constraint: specify the minimum and maximum number of occurrences allowed in a relationship
- Nullability Constraint: whether an attribute can have null values or must have non-null values

### Inheritance

- subtypes: represent specialized entities that inherit attributes and relationships from a more general entity called a supertype
- supertypes: general entity 
- Specification: defining subtypes from a supertype
- Generalizaiton: creating a supertype from existing subtypes

### E-R Diagram

- Entity: Entities are represented by rectangles (or squares) with the entity name written inside
- Attribute: typically shown as ovals or ellipses connected to the respective entity box
- Primary Key: underlined within the attribute oval or written separately below the attribute name
- Relationship: represented by diamonds (or rhombuses) connected by lines to the participating entities
- Cardinality Notations: indicate the number of instances of one entity that can be associated with instances of another entity in a relationship
- Inheritance Symbols: 
  - Solid line with a triangle arrowhead: Indicates a specialization hierarchy where the subtype entities inherit attributes and relationships from the supertype
  - Dashed line with a triangle arrowhead: Represents a generalization hierarchy where a supertype is created from existing subtypes

- Disjointness and Completeness Constraints
  - Disjoint: subtypes are exclusive, 
  - Overlapping: subtype can overlap
- Ternary (N-ary) Relationship Notation: These relationships are typically represented by diamonds (or rhombuses) with lines connecting them to the participating entities. The lines may include labels to describe the nature of the relationship.
- Union Type Notation: They are represented by a circle or ellipse split into sections, each section corresponding to a possible type of the attribute.
- Attribute Inheritance Notation: a dashed line is drawn from the supertype's attribute to the subtype's attribute.

## Relational Model

- Tables/Relations: Tables are used to represent entities, and each table has a unique name.
- Rows/Tuples: Each row in a table represents a specific occurrence of an entity.
- Columns/Attributes: Columns define the properties or characteristics of an entity.
- Keys: Keys are used to uniquely identify rows in a table
- Relationships: Relationships represent associations between entities in the database. They are established through the use of keys

### Relation Mapping

- Entity Types: Each entity type in the ER model corresponds to a relation in the relational model. 
  - The relation has the same name as the entity type
  - If the entity type has an identifying property, it becomes the primary key of the relation
  - Other properties of the entity type become attributes in the relation
  - Composite Property Types: If an entity type has a composite property type, composed of multiple sub-properties, the sub-properties become separate attributes in the relation and we lose the composite property itself
  - Multi-Valued Property Types: The relational model does not directly support multi-valued attributes. If an entity type has a multi-valued property type, a separate relation is created to represent the property

- Relationships: 
  - One-to-One: For a 1:1 relationship between entity types ET1 and ET2, a foreign key can be added either in ET1 or ET2 to establish the connection
  - One-to-Many Relationships: In a 1:N relationship, where one instance of ET1 relates to many instances of ET2, the foreign key should be added in ET2.
  - Many-to-Many Relationships: In an N:M relationship, a separate relation R is created to represent the relationship. R contains foreign keys referencing the primary keys of ET1 and ET2

- Inheritance
  - Mandatory Disjoint: Create separate relations for ET1 and ET2, both inheriting the primary key A and attribute B from ET. ET1 has an additional attribute C, while ET2 has an additional attribute D.
  - Mandatory, Overlap Allowed: Create a single relation for ET with attributes A, B, C, and D. Include an attribute named "Type" to indicate whether the tuple is an instance of ET1, ET2, or both
  - Non-Mandatory, Overlap Allowed: Create relation ET and separate relations for ET1 and ET2, both inheriting the primary key A from ET. ET1 has an additional attribute C, and ET2 has an additional attribute D. Instances of ET are added as tuples in ET and can be referenced by ET1, ET2, both, or neither
  - Non-Mandatory, Disjoint: Create separate relations for ET, ET1, and ET2. ET1 and ET2 inherit the primary key A from ET. Tuples in ET can exist without being referenced by ET1 or ET2, and when referenced, they exclusively belong to either ET1 or ET2

- Union Type
  - Create a relation for ET that includes the property type B.
  - Introduce an artificial identifier in the ET relation called ET-ID. ET-ID will consist of either a value of C or D, representing the primary key of either ET1 or ET2. 
  - Create separate relations for ET1 and ET2 with primary keys C and D respectively. The artificial identifier allows us to uniquely identify each tuple in ET, as every tuple must be an instance of either ET1 or ET2.
