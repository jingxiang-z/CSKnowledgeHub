## Java Basic

### Concepts

- Java Virtual Machine(JVM):an abstract machine, provides a runtime environment in which java bytecode can be executed
- Java Runtime Enviroment (JRE): contains the parts of java libraries required to run java programs
- Java Development Kit(JDK): includes everything including compiler, JRE, debuggers, etc.

### Features

- Platform Independent: conpiler converts source code to bytecode, then JVM executes the bytecode
- Object Oriented: abstraction, encapsulationl, inheritance, polymorphism
- Robust: garbage collection, exception handling, memory allocation

## Variable

### Data Type

Java is statically typed language where each variable and expression type is already known at compile time

Primitive Data Type:

- Boolean: true, false
- Character: char
- Integer: byte, short, int, long
- Floating-Point: float, double

Non-primitive Data Types:

- String: a sequence of characters, immutable and can not be changed
- Array: declared like other variables with [] after the data type, stored in contiguous memory and dynamically allocated

### Variable

- local variables: created in the block, exists only within the block, must initialized
- instance variables: declared in a class, created with an object and destroyed when object is destroyed, default initalized to 0
- static variables: created at the start of program execution and destroyed when execution ends, default value 0 

## Objected Oriented

### Concepts

- class: user-defined prototype, represents the set of properties and methods
- object: basic unit of OOP that represents real life entity

- access modifier: defines the access type of the method
  - public: accessible in all classes
  - Protected: accessible within the package and in subclass
  - Private: accessible only in the class

- 4pillars of OOP
  - Abstraction: identify only the required characteristics of an object, ignoring the irrelevant details
  - Encapsulation: a wrapping up of data under a single unit; bind together the code and data it manipulates
  - inheritance: one class is allowed to inherit the features of another class
  - Polymorphism: the ability to differentiate between entities with the same name efficiently

### Constructor

Constructor: A constructor is a special method that is used to initialize objects.

- constructors must have the same name as the class
- constructors do not return any type
- contructors are called only once at the time of object creation

Copy Constructor: copy constructer is called when copy one object to another

- no default copy constructor, if not defined then compile error
- Non-primitive data type only create reference, if need copy, explicitly call copy constructor

### Inheritance

- single inheritance: subclasses inherit the features from one superclass
- multilevel inheritance: the inherited class is base class for other classes
- hierarchical inheritance: one class serves as superclass for more than one subclass
- multiple inheritance: one class can inherit from multiple interfaces but not classes

### Polymorphism

- Compile-time Polymorphism: achieved by function overloading
  - change the number of parameters
  - change data types of the arguments
  - change the order of the parameters of methods
- Runtime Polymorphism: acheived by method overriding
  - At run-time, Java determines the superclass version or subclass version of a method to be executed
  - A superclass reference variable can refer to a subclass object

### Abstraction

In Java, abstraction is achieved by interfaces and abstract classes.

abstraction provide a superclass without providing a complete implementation of every method

- abstract class: a class declared with an abstract keyword
- abstract method: a method that is declared without implementation

interfaces is defined as an abstract type used to specify the behavior of a class, only have abstract methods

- Interfaces use implements keyword for inheritance
- interface supports multiple inheritance

### Encapsulation

Encapsulation is defined as the wrapping up of data under a single unit. It binds together code and the data it manipulates

- the variable or data is hidden from any other class and can be accessed only the the member function
- encapsulation can be achieved by declaring all variables in the class as private and writing public methods in the class

## Exception

- Built-in Exceptions
  - Checked Exception: compile time exceptions including IOException, SQLException, etc.
  - Unchecked Exception: compiler won't check the exceptions at compile time, including ClassCastException, etc.
- User-Defined Exceptions

```java
try {
  	// block of code to monitor for errors
} catch (ExceptionType1 ex1) {
  	// exception handler for ExceptionType1
} catch (ExceptionType2 ex2) {
  	// exception handler for ExceptionType2
} finally {
  	// optional, block of code to be executed after try block ends
}
```

### Exception Handling

- If an exception has occurred, the method creates and exception object and hands it off to JVM
- JVM searches the call stack to find the method that can handle the occurred exception (Exception handler)
- JVM stats searching the method where exception occurred, and proceed through the call stack in reversed order
- if finds an appropriate handler, then passes the exception to it
- If can not find an appropriate handler, call the default exception handler

## Collections

### List

- ArrayList: a dynamic array, size increase or decrease automatically when collection grows or shrinks
- LinkedList: every element is a separate object with data part and address part, linked using pointers and addresses
- Vector: dynamic arrays, identical to ArrayList of implementation; Vector is synchronized but ArrayList is not
- Stack: last in first out data structures

### Queue

- PriorityQueue: based on the priority heap, ordered according to the natural ordering or by a comparator
- ArrayDeque: double-ended queue

### Set

- HashSet: inherent implementation of hash table data structure
- LinkedHashSet: uses doubly linked list to store the data and retains the ordering of the elements
- TreeSet: use a tree for storage, the order of the element is maintained using their natural ordering

### Map

- HashMap: stores the data in key value pairs
