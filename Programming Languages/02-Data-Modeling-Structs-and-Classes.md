# 02 Data Modeling: Structs and Classes

## Table of Contents

1. [Overview](#overview)
2. [Core Concepts](#core-concepts)
   - [Fields and Instances](#fields-and-instances)
   - [Mutability and Updates](#mutability-and-updates)
   - [Methods and Associated Behavior](#methods-and-associated-behavior)
   - [Construction and Defaults](#construction-and-defaults)
   - [Invariants and Validation](#invariants-and-validation)
   - [Visibility and Encapsulation](#visibility-and-encapsulation)
   - [Composition](#composition)
   - [Equality, Identity, and Variants](#equality-identity-and-variants)
   - [Classes and Object-Oriented Features](#classes-and-object-oriented-features)
3. [Concept Mapping](#concept-mapping)
4. [References](#references)

## Overview

A **struct** or **class** is a custom type that models a meaningful concept, such as a user account, a point in space, a configuration value, or a database record. It can group related data and, in many languages, the behavior that operates on that data.

Rust and Go use structs as their main data-modeling type. Python uses classes, with dataclasses providing a concise form for data-focused classes. C++ supports both structs and classes. They differ in syntax, default mutability, method placement, construction rules, visibility controls, and support for inheritance.

## Core Concepts

### Fields and Instances

A **field** is a named piece of data in a struct. An **instance** is a value created from that struct type.

Named fields are usually clearer than tuples or positional records because readers do not need to remember what each position means.

#### Rust

~~~rust
struct User {
    username: String,
    email: String,
    active: bool,
}

let user = User {
    username: String::from("ada"),
    email: String::from("ada@example.com"),
    active: true,
};

println!("{}", user.username);
~~~

#### Go

~~~go
type User struct {
    Username string
    Email    string
    Active   bool
}

user := User{
    Username: "ada",
    Email:    "ada@example.com",
    Active:   true,
}

fmt.Println(user.Username)
~~~

#### Python

A dataclass is a concise way to define a class mainly used to store data.

~~~python
from dataclasses import dataclass

@dataclass
class User:
    username: str
    email: str
    active: bool

user = User("ada", "ada@example.com", True)
print(user.username)
~~~

#### C++

~~~cpp
#include <string>

struct User {
    std::string username;
    std::string email;
    bool active;
};

User user{"ada", "ada@example.com", true};
std::cout << user.username << "\n";
~~~

### Mutability and Updates

Updating a field changes the state of an instance. Languages differ in whether instances are mutable by default and how mutation is expressed.

#### Rust

The binding must be declared with **mut** before fields can be changed.

~~~rust
let mut user = User {
    username: String::from("ada"),
    email: String::from("old@example.com"),
    active: true,
};

user.email = String::from("new@example.com");
~~~

Rust also supports struct-update syntax to build a new value using the remaining fields of an existing value.

~~~rust
let updated_user = User {
    email: String::from("new@example.com"),
    ..user
};
~~~

#### Go

Struct values are mutable. A function needs a pointer receiver or pointer parameter to update the caller's struct value.

~~~go
user := User{Username: "ada", Active: true}
user.Active = false

func deactivate(user *User) {
    user.Active = false
}
~~~

#### Python

Class and dataclass instances are normally mutable.

~~~python
user = User("ada", "ada@example.com", True)
user.active = False
~~~

Use **frozen=True** with a dataclass when the instance should not be changed after creation.

#### C++

Struct members are mutable unless the instance or member is declared **const**.

~~~cpp
User user{"ada", "ada@example.com", true};
user.active = false;

const User fixed_user{"grace", "grace@example.com", true};
// fixed_user.active = false; // Error
~~~

### Methods and Associated Behavior

A method is behavior associated with a type. Keeping behavior near the data it operates on makes a type easier to use and understand.

#### Rust

Methods are placed in an **impl** block. The first parameter is a form of **self**.

~~~rust
struct Rectangle {
    width: u32,
    height: u32,
}

impl Rectangle {
    fn area(&self) -> u32 {
        self.width * self.height
    }

    fn double_width(&mut self) {
        self.width *= 2;
    }
}

let mut rectangle = Rectangle {
    width: 10,
    height: 5,
};

println!("{}", rectangle.area());
rectangle.double_width();
~~~

#### Go

Go methods are declared outside the struct definition and use an explicit receiver. A pointer receiver can modify the instance.

~~~go
type Rectangle struct {
    Width  int
    Height int
}

func (r Rectangle) Area() int {
    return r.Width * r.Height
}

func (r *Rectangle) DoubleWidth() {
    r.Width *= 2
}
~~~

#### Python

Methods are declared inside a class. The first parameter, conventionally named **self**, refers to the instance.

~~~python
@dataclass
class Rectangle:
    width: int
    height: int

    def area(self) -> int:
        return self.width * self.height

    def double_width(self) -> None:
        self.width *= 2
~~~

#### C++

Member functions are declared inside the struct or class. A **const** method promises not to change the instance.

~~~cpp
struct Rectangle {
    int width;
    int height;

    int area() const {
        return width * height;
    }

    void double_width() {
        width *= 2;
    }
};
~~~

### Construction and Defaults

A constructor or factory creates an instance in a valid initial state. Defaults provide values when a caller does not supply every field.

#### Rust

Rust does not use constructors as a special language feature. Associated functions conventionally named **new** are common, and **Default** can provide a standard value.

~~~rust
#[derive(Default)]
struct Settings {
    retries: u32,
    verbose: bool,
}

impl Settings {
    fn new(retries: u32) -> Self {
        Self {
            retries,
            verbose: false,
        }
    }
}

let default_settings = Settings::default();
let settings = Settings::new(3);
~~~

#### Go

Go uses struct literals. A conventional constructor is an ordinary function, often returning a pointer.

~~~go
type Settings struct {
    Retries int
    Verbose bool
}

func NewSettings(retries int) *Settings {
    return &Settings{
        Retries: retries,
        Verbose: false,
    }
}

settings := NewSettings(3)
~~~

#### Python

Dataclasses can supply field defaults. A normal class can also initialize state in an **__init__** method.

~~~python
@dataclass
class Settings:
    retries: int = 3
    verbose: bool = False

settings = Settings()
debug_settings = Settings(verbose=True)
~~~

#### C++

Constructors initialize an object. Default member initializers are useful for common defaults.

~~~cpp
struct Settings {
    int retries = 3;
    bool verbose = false;

    Settings() = default;

    Settings(int retry_count, bool is_verbose)
        : retries(retry_count), verbose(is_verbose) {}
};

Settings default_settings;
Settings debug_settings{5, true};
~~~

### Invariants and Validation

An **invariant** is a condition that must remain true for every valid instance. Put validation at the boundary where an instance is created or changed so callers cannot accidentally create an impossible state. Defaults are convenient only when the default is genuinely valid.

For example, an account with a negative balance or an order with zero items should usually be rejected by a constructor/factory or a dedicated method—not left for unrelated callers to handle later.

~~~rust
struct Percentage(u8);

impl Percentage {
    fn new(value: u8) -> Option<Self> {
        (value <= 100).then_some(Self(value))
    }
}
~~~

The syntax varies, but the design principle is shared: expose operations that preserve the invariant, and keep fields private when direct mutation would bypass it.

### Visibility and Encapsulation

Visibility controls whether code outside a type or module can access its fields and behavior directly. Encapsulation keeps a type's internal representation separate from its public interface.

#### Rust

Struct fields are private to their defining module by default. Use **pub** to expose a field.

~~~rust
pub struct Account {
    pub username: String,
    active: bool,
}

impl Account {
    pub fn is_active(&self) -> bool {
        self.active
    }
}
~~~

#### Go

An identifier beginning with an uppercase letter is exported from its package. A lowercase field is package-private.

~~~go
type Account struct {
    Username string // Exported
    active   bool   // Package-private
}
~~~

#### Python

Python does not enforce private fields in the same way. A leading underscore communicates that an attribute is internal by convention.

~~~python
class Account:
    def __init__(self, username: str, active: bool):
        self.username = username
        self._active = active

    def is_active(self) -> bool:
        return self._active
~~~

#### C++

Members of a **struct** are public by default; members of a **class** are private by default. Access specifiers can change this.

~~~cpp
#include <string>
#include <utility>

class Account {
public:
    explicit Account(std::string username)
        : username_(std::move(username)) {}

    bool is_active() const {
        return active_;
    }

private:
    std::string username_;
    bool active_ = true;
};
~~~

### Composition

Composition builds larger types by storing one struct-like type inside another. It is often preferable to modeling a relationship with inheritance.

#### Rust

~~~rust
struct Address {
    city: String,
    country: String,
}

struct Customer {
    name: String,
    address: Address,
}
~~~

#### Go

Go supports named fields and embedding. Embedding promotes the embedded type's fields and methods.

Embedding is still composition: a `Customer` contains an `Address`; it does not make `Customer` a specialized kind of `Address`.

~~~go
type Address struct {
    City    string
    Country string
}

type Customer struct {
    Name string
    Address
}
~~~

#### Python

~~~python
@dataclass
class Address:
    city: str
    country: str

@dataclass
class Customer:
    name: str
    address: Address
~~~

#### C++

~~~cpp
struct Address {
    std::string city;
    std::string country;
};

struct Customer {
    std::string name;
    Address address;
};
~~~

### Equality, Identity, and Variants

**Value equality** asks whether two values contain the same meaningful data. **Identity** asks whether two names refer to the very same object. Decide which matters for a model before using it as a map key, comparing it, or updating it.

Python's `==` commonly compares values while `is` compares identity. Rust can derive `PartialEq`/`Eq`; C++ can define `operator==`; Go structs and arrays are comparable only when all of their fields/elements are comparable. Mutable objects with identity should not usually be used as stable keys.

Structs and classes model a value with several fields. A **variant** (Rust `enum`, a tagged union, or a class hierarchy) models a value that is exactly one of several cases. For example, a payment can be `Cash`, `Card`, or `BankTransfer`; this is clearer and safer than a struct with three optional fields, where invalid combinations are possible.

**Common mistake:** use composition for “has a” relationships and reserve inheritance for a true, substitutable “is a” relationship. Go embedding promotes members but does not create inheritance.

### Classes and Object-Oriented Features

A class commonly combines data, behavior, and encapsulation. Some class systems also support **inheritance**, where a derived type extends a base type, and **polymorphism**, where code works through a shared interface. These features are useful in some designs, but composition is often the simpler default.

#### Rust

Rust has no class inheritance. Structs hold data and `impl` blocks define behavior. Traits describe shared capabilities, which types can implement.

~~~rust
trait Describable {
    fn describe(&self) -> String;
}

struct User {
    name: String,
}

impl Describable for User {
    fn describe(&self) -> String {
        format!("User: {}", self.name)
    }
}
~~~

#### Go

Go has no class inheritance. Structs have methods, and interfaces describe behavior. A type satisfies an interface implicitly by having the required methods.

~~~go
type Describable interface {
    Describe() string
}

type User struct {
    Name string
}

func (u User) Describe() string {
    return "User: " + u.Name
}
~~~

#### Python

Python classes support inheritance. A derived class can add or replace behavior from a base class.

~~~python
class User:
    def describe(self) -> str:
        return "User"

class Admin(User):
    def describe(self) -> str:
        return "Administrator"
~~~

#### C++

C++ classes support inheritance. A virtual method allows derived classes to provide behavior through a base-class interface.

~~~cpp
#include <string>

class User {
public:
    virtual std::string describe() const { return "User"; }
    virtual ~User() = default;
};

class Admin : public User {
public:
    std::string describe() const override { return "Administrator"; }
};
~~~

## Concept Mapping

| Concept | Rust | Go | Python | C++ |
|---|---|---|---|---|
| Basic data type | **struct** | **struct** | Class or **dataclass** | **struct** or **class** |
| Field visibility default | Private to module | Lowercase names unexported | Public by convention | Public for struct; private for class |
| Instance mutation | Binding must be **mut** | Mutable value; pointer for caller mutation | Mutable by default | Mutable unless **const** |
| Method location | **impl** block | Separate declaration with receiver | Inside class definition | Inside or outside class/struct definition |
| Constructor style | Associated function or **Default** | Struct literal or factory function | **__init__** or dataclass defaults | Constructor |
| Composition | Nested fields | Named fields or embedding | Nested objects | Nested members or inheritance |
| Inheritance | No; use composition and traits | No; use composition and interfaces | Supported | Supported |
| Variants / sum types | `enum` | tagged struct or interface | tagged classes / `match` | `std::variant` or class hierarchy |

## References

- [The Rust Programming Language — Using Structs to Structure Related Data](https://doc.rust-lang.org/stable/book/ch05-00-structs.html)
- [The Rust Programming Language — Defining and Instantiating Structs](https://doc.rust-lang.org/stable/book/ch05-01-defining-structs.html)
- [The Rust Programming Language — Methods](https://doc.rust-lang.org/stable/book/ch05-03-method-syntax.html)
- [Go Language Specification — Struct types](https://go.dev/ref/spec#Struct_types)
- [Go Language Specification — Method declarations](https://go.dev/ref/spec#Method_declarations)
- [Python Tutorial — Classes](https://docs.python.org/3/tutorial/classes.html)
- [Python Documentation — dataclasses](https://docs.python.org/3/library/dataclasses.html)
- [C++ classes (working draft)](https://eel.is/c++draft/class)
