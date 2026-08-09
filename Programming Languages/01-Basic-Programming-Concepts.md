# 01 Basic Programming Concepts

## Table of Contents
1. [Overview](#overview)
2. [Foundations](#foundations)
   - [Variables](#variables)
   - [Scope and Constants](#scope-and-constants)
   - [Basic Data Types](#basic-data-types)
   - [Collections](#collections)
   - [Type Conversion](#type-conversion)
3. [Functions and Program Structure](#functions-and-program-structure)
   - [Functions](#functions)
   - [Function Parameters and Results](#function-parameters-and-results)
   - [Passing Values to Functions](#passing-values-to-functions)
4. [Control Flow](#control-flow)
   - [Conditional Control Flow](#conditional-control-flow)
   - [Multiple Conditions and Logical Operators](#multiple-conditions-and-logical-operators)
   - [Multi-Way Branching](#multi-way-branching)
   - [Loops](#loops)
5. [Documentation](#documentation)
   - [Comments](#comments)
6. [Comparison](#comparison)
   - [Key Differences](#key-differences)

## Overview

Most programming languages provide the same core building blocks:

- **Variables** store values under names.
- **Types** describe what kind of values can be stored.
- **Functions** package reusable behavior.
- **Conditionals** choose which code to execute.
- **Loops** repeat code.
- **Comments** explain code for human readers.

The syntax differs between languages, but the underlying ideas are similar. The examples below implement the same ideas in Rust, Go, Python, and C++.

## Foundations

### Variables

#### Rust

Rust variables are immutable by default. Use `mut` when a value must change.

~~~rust
fn main() {
    let name = "Ada";
    let mut score = 10;

    score += 5;

    println!("{name} has {score} points");
}
~~~

Rust also supports **shadowing**, where a new variable reuses an existing name:

~~~rust
let spaces = "   ";
let spaces = spaces.len(); // The new value has type usize
~~~

#### Go

Go variables can be declared with `var` or with the short declaration operator `:=`.

~~~go
package main

import "fmt"

func main() {
    name := "Ada"
    score := 10

    score += 5

    fmt.Printf("%s has %d points\n", name, score)
}
~~~

Go variables are mutable by default. A variable declared with `const` cannot change.

#### Python

Python variables are names bound to objects, and their types are determined at runtime.

~~~python
name = "Ada"
score = 10

score += 5

print(f"{name} has {score} points")
~~~

Python variables can be reassigned to values of different types:

~~~python
value = 10
value = "ten"
~~~

#### C++

C++ variables normally require a declared type. Use `const` for a value that should not be reassigned.

~~~cpp
#include <iostream>
#include <string>

int main() {
    std::string name = "Ada";
    int score = 10;

    score += 5;

    std::cout << name << " has " << score << " points\n";
}
~~~

### Scope and Constants

**Scope** is the part of the program where a variable name is available. In all four languages, a variable declared inside a function or block is normally unavailable outside it.

Constants represent values that should not change. Rust, Go, and C++ enforce constants in the language; Python uses an uppercase naming convention but does not enforce it.

#### Rust

~~~rust
const MAX_RETRIES: u32 = 3;

{
    let message = "only available in this block";
    println!("{message}");
}
~~~

#### Go

~~~go
const MaxRetries = 3

if true {
	message := "only available in this block"
	fmt.Println(message)
}
~~~

#### Python

~~~python
MAX_RETRIES = 3  # Convention: treat uppercase names as constants

if True:
    message = "available after this block too"

print(message)
~~~

#### C++

~~~cpp
const int max_retries = 3;

{
    std::string message = "only available in this block";
    std::cout << message << "\n";
}
~~~

Python blocks do not create a new local scope, unlike the block scopes shown in Rust, Go, and C++. Functions do create local scopes in Python.

### Basic Data Types

The names vary slightly, but all four languages provide numbers, Boolean values, text, and collections.

| Concept | Rust | Go | Python | C++ |
|---|---|---|---|---|
| Integer | `i32`, `u32` | `int`, `int32` | `int` | `int`, `long` |
| Decimal number | `f64` | `float64` | `float` | `double` |
| Boolean | `bool` | `bool` | `bool` | `bool` |
| Character | `char` | `rune` | one-character `str` | `char` |
| Text | `String`, `&str` | `string` | `str` | `std::string` |
| Fixed-size collection | array | array | tuple | array or `std::array` |
| Growable sequence | `Vec<T>` | slice | list | `std::vector<T>` |
| Key-value collection | `HashMap<K, V>` | `map[K]V` | `dict` | `std::map<K, V>` |

#### Rust

~~~rust
let count: i32 = 42;
let price: f64 = 9.99;
let available: bool = true;
let letter: char = 'R';
let numbers: [i32; 3] = [1, 2, 3];
~~~

Rust is statically typed. The compiler often infers types, but every value still has a known type at compile time.

#### Go

~~~go
var count int = 42
price := 9.99
available := true
letter := 'R'
numbers := [3]int{1, 2, 3}
~~~

Go is statically typed and can infer types when using `:=`.

#### Python

~~~python
count = 42
price = 9.99
available = True
letter = "R"
numbers = [1, 2, 3]
~~~

Python is dynamically typed: type checking happens while the program runs rather than requiring declarations for every variable.

#### C++

~~~cpp
int count = 42;
double price = 9.99;
bool available = true;
char letter = 'R';
int numbers[] = {1, 2, 3};
~~~

C++ is statically typed. The `auto` keyword can ask the compiler to infer a variable's type:

~~~cpp
auto count = 42; // inferred as int
~~~

### Collections

Strings and collections are used constantly in real programs. The examples below show a growable sequence and a key-value collection in each language.

#### Rust

~~~rust
use std::collections::HashMap;

let mut languages = vec!["Rust", "Go"];
languages.push("Python");

let mut scores = HashMap::new();
scores.insert("Ada", 100);
~~~

#### Go

~~~go
languages := []string{"Rust", "Go"}
languages = append(languages, "Python")

scores := map[string]int{"Ada": 100}
~~~

#### Python

~~~python
languages = ["Rust", "Go"]
languages.append("Python")

scores = {"Ada": 100}
~~~

#### C++

~~~cpp
#include <map>
#include <string>
#include <vector>

std::vector<std::string> languages = {"Rust", "Go"};
languages.push_back("Python");

std::map<std::string, int> scores = {{"Ada", 100}};
~~~

### Type Conversion

Conversion changes a value from one type to another. Rust, Go, and C++ make many conversions explicit, which helps avoid accidental data loss. Python also has explicit conversion functions.

#### Rust

~~~rust
let text = "42";
let number: i32 = text.parse().expect("valid integer");
let decimal = number as f64;
~~~

#### Go

~~~go
import "strconv"

number, err := strconv.Atoi("42")
decimal := float64(number)
~~~

#### Python

~~~python
number = int("42")
decimal = float(number)
~~~

#### C++

~~~cpp
#include <string>

int number = std::stoi("42");
double decimal = static_cast<double>(number);
~~~

In the Go example, production code should check `err` before using `number`. In Rust, `parse` can also fail; `expect` ends the program with a message if the input is invalid.

## Functions and Program Structure

### Functions

Functions group instructions into reusable units. In all four languages, functions can receive parameters and return values.

#### Rust

~~~rust
fn add(a: i32, b: i32) -> i32 {
    a + b // Last expression is returned
}

fn main() {
    let result = add(2, 3);
    println!("{result}");
}
~~~

Rust requires parameter and return types in function signatures. A semicolon would turn `a + b` into a statement instead of the return expression.

#### Go

~~~go
package main

import "fmt"

func add(a int, b int) int {
    return a + b
}

func main() {
    result := add(2, 3)
    fmt.Println(result)
}
~~~

Go also supports multiple return values, commonly used for a result and an error.

#### Python

~~~python
def add(a, b):
    return a + b

result = add(2, 3)
print(result)
~~~

Python also allows optional type hints:

~~~python
def add(a: int, b: int) -> int:
    return a + b
~~~

#### C++

~~~cpp
#include <iostream>

int add(int a, int b) {
    return a + b;
}

int main() {
    int result = add(2, 3);
    std::cout << result << "\n";
}
~~~

### Function Parameters and Results

All four languages can accept multiple parameters. Their support for default parameters and multiple return values differs:

| Language | Default parameters | Multiple return values |
|---|---|---|
| Rust | No; use separate functions, options, or a struct | Tuple |
| Go | No | Built in |
| Python | Yes | Tuple packing/unpacking |
| C++ | Yes | Usually a struct, tuple, or output parameter |

#### Rust

~~~rust
// Rust has no default parameters, so both arguments are required.
fn greet(name: &str, greeting: &str) -> String {
    format!("{greeting}, {name}!")
}

fn min_max(a: i32, b: i32) -> (i32, i32) {
    if a < b { (a, b) } else { (b, a) }
}

let (smallest, largest) = min_max(8, 3);
~~~

#### Go

~~~go
// Go has no default parameters, so both arguments are required.
func greet(name string, greeting string) string {
	return greeting + ", " + name + "!"
}

func minMax(a int, b int) (int, int) {
	if a < b {
		return a, b
	}
	return b, a
}

smallest, largest := minMax(8, 3)
~~~

#### Python

~~~python
def greet(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"

def min_max(a: int, b: int) -> tuple[int, int]:
    return (a, b) if a < b else (b, a)

smallest, largest = min_max(8, 3)
~~~

#### C++

~~~cpp
#include <string>
#include <utility>

std::string greet(const std::string& name,
                  const std::string& greeting = "Hello") {
    return greeting + ", " + name + "!";
}

std::pair<int, int> min_max(int a, int b) {
    return a < b ? std::pair{a, b} : std::pair{b, a};
}

auto [smallest, largest] = min_max(8, 3);
~~~

### Passing Values to Functions

This is a preview of a larger topic: how functions receive values.

| Language | Common approach |
|---|---|
| Rust | Values move by default; use references such as `&T` to borrow without transferring ownership. |
| Go | Arguments are passed by value; slices, maps, and pointers can let a function affect shared data. |
| Python | Names are passed to objects; mutating a passed mutable object is visible to the caller, but rebinding the parameter is not. |
| C++ | Arguments are copied by default; references (`T&`) and pointers can allow mutation of the caller's value. |

You do not need to master these rules yet, but they explain why a function may or may not be able to change a variable supplied by its caller.

#### Rust

~~~rust
fn add_one(number: &mut i32) {
    *number += 1;
}

let mut score = 10;
add_one(&mut score);
~~~

#### Go

~~~go
func addOne(number *int) {
	*number += 1
}

score := 10
addOne(&score)
~~~

#### Python

~~~python
def add_item(items):
    items.append("Rust")

languages = []
add_item(languages)
~~~

#### C++

~~~cpp
void add_one(int& number) {
    ++number;
}

int score = 10;
add_one(score);
~~~

## Control Flow

### Conditional Control Flow

#### Rust

~~~rust
let score = 85;

if score >= 60 {
    println!("pass");
} else {
    println!("fail");
}
~~~

Rust requires the condition to be a Boolean. Since `if` is an expression, it can also produce a value:

~~~rust
let result = if score >= 60 { "pass" } else { "fail" };
~~~

#### Go

~~~go
score := 85

if score >= 60 {
    fmt.Println("pass")
} else {
    fmt.Println("fail")
}
~~~

Go does not use parentheses around the condition.

#### Python

~~~python
score = 85

if score >= 60:
    print("pass")
else:
    print("fail")
~~~

Python uses indentation to define the body of each branch.

#### C++

~~~cpp
int score = 85;

if (score >= 60) {
    std::cout << "pass\n";
} else {
    std::cout << "fail\n";
}
~~~

### Multiple Conditions and Logical Operators

Use `else if` (or Python's `elif`) to choose among more than two paths. Logical operators combine Boolean conditions.

| Meaning | Rust | Go | Python | C++ |
|---|---|---|---|---|
| AND | `&&` | `&&` | `and` | `&&` |
| OR | `||` | `||` | `or` | `||` |
| NOT | `!` | `!` | `not` | `!` |

#### Rust

~~~rust
let age = 20;
let has_ticket = true;

if age >= 18 && has_ticket {
    println!("admit");
} else if age >= 18 {
    println!("ticket required");
} else {
    println!("too young");
}
~~~

#### Go

~~~go
age := 20
hasTicket := true

if age >= 18 && hasTicket {
	fmt.Println("admit")
} else if age >= 18 {
	fmt.Println("ticket required")
} else {
	fmt.Println("too young")
}
~~~

#### Python

~~~python
age = 20
has_ticket = True

if age >= 18 and has_ticket:
    print("admit")
elif age >= 18:
    print("ticket required")
else:
    print("too young")
~~~

#### C++

~~~cpp
int age = 20;
bool has_ticket = true;

if (age >= 18 && has_ticket) {
    std::cout << "admit\n";
} else if (age >= 18) {
    std::cout << "ticket required\n";
} else {
    std::cout << "too young\n";
}
~~~

### Multi-Way Branching

When comparing one value against several cases, a multi-way branch is often clearer than a long `else if` chain.

#### Rust

~~~rust
let day = 2;

match day {
    1 => println!("Monday"),
    2 => println!("Tuesday"),
    _ => println!("another day"),
}
~~~

#### Go

~~~go
day := 2

switch day {
case 1:
	fmt.Println("Monday")
case 2:
	fmt.Println("Tuesday")
default:
	fmt.Println("another day")
}
~~~

Python 3.10 and later supports `match`:

#### Python

~~~python
day = 2

match day:
    case 1:
        print("Monday")
    case 2:
        print("Tuesday")
    case _:
        print("another day")
~~~

#### C++

~~~cpp
int day = 2;

switch (day) {
    case 1:
        std::cout << "Monday\n";
        break;
    case 2:
        std::cout << "Tuesday\n";
        break;
    default:
        std::cout << "another day\n";
        break;
}
~~~

Rust's `match` must handle every possible case, which is why it commonly includes `_`. In C++, `break` prevents execution from falling through into the next case.

### Loops

Loops repeat a block of code. The right loop depends on whether you are iterating through a collection, repeating while a condition is true, or deliberately running until a `break` statement stops the loop.

#### Rust

Use `for` to iterate through a collection:

~~~rust
let numbers = [10, 20, 30];

for number in numbers {
    println!("{number}");
}
~~~

Use `while` when repetition depends on a condition:

~~~rust
let mut count = 3;

while count > 0 {
    println!("{count}");
    count -= 1;
}
~~~

`loop` repeats indefinitely until `break`. A loop can return a value through `break`:

~~~rust
let mut attempts = 0;

let result = loop {
    attempts += 1;

    if attempts == 3 {
        break "success";
    }
};

println!("{result}");
~~~

Use `continue` to skip the remainder of the current iteration:

~~~rust
for number in 1..=5 {
    if number % 2 == 0 {
        continue;
    }

    println!("odd: {number}");
}
~~~

#### Go

Go uses `for` for every loop style. Use `range` to iterate through a collection:

~~~go
numbers := []int{10, 20, 30}

for _, number := range numbers {
	fmt.Println(number)
}
~~~

This condition-based `for` loop is similar to a `while` loop in other languages:

~~~go
count := 3

for count > 0 {
	fmt.Println(count)
	count--
}
~~~

A three-part `for` loop has initialization, a condition, and an update:

~~~go
for index := 0; index < 5; index++ {
	if index == 2 {
		continue
	}

	if index == 4 {
		break
	}

	fmt.Println(index)
}
~~~

An omitted condition creates an infinite loop; use `break` to exit it:

~~~go
for {
	// Repeat until a break statement exits the loop.
	break
}
~~~

#### Python

Use `for` to iterate through a collection:

~~~python
numbers = [10, 20, 30]

for number in numbers:
    print(number)
~~~

`range` is useful when you need a sequence of numbers. The end value is excluded:

~~~python
for number in range(1, 6):
    print(number)  # 1 through 5
~~~

Use `while` when repetition depends on a condition:

~~~python
count = 3

while count > 0:
    print(count)
    count -= 1
~~~

`break` exits a loop, while `continue` skips to the next iteration:

~~~python
for number in range(1, 6):
    if number == 2:
        continue
    if number == 5:
        break

    print(number)
~~~

#### C++

Use a range-based `for` loop to iterate through an array or collection:

~~~cpp
#include <iostream>

int numbers[] = {10, 20, 30};

for (int number : numbers) {
    std::cout << number << "\n";
}
~~~

A classic `for` loop is useful when an index is needed:

~~~cpp
for (int index = 0; index < 5; ++index) {
    std::cout << index << "\n";
}
~~~

Use `while` to repeat while a condition is true:

~~~cpp
int count = 3;

while (count > 0) {
    std::cout << count << "\n";
    --count;
}
~~~

`do-while` runs its body at least once because it checks the condition after each iteration:

~~~cpp
int attempts = 0;

do {
    ++attempts;
} while (attempts < 3);
~~~

Use `break` to exit and `continue` to skip one iteration:

~~~cpp
for (int number = 1; number <= 5; ++number) {
    if (number == 2) {
        continue;
    }
    if (number == 5) {
        break;
    }

    std::cout << number << "\n";
}
~~~

## Documentation

### Comments

Comments are ignored by the compiler or interpreter and are intended for human readers.

#### Rust

~~~rust
// Rust comment
~~~

#### Go

~~~go
// Go comment
~~~

#### Python

~~~python
# Python comment
~~~

#### C++

~~~cpp
// C++ comment
~~~

All four languages also support multi-line comment syntax, although Python commonly uses triple-quoted strings for documentation rather than ordinary comments.

## Comparison

### Key Differences

| Topic | Rust | Go | Python | C++ |
|---|---|---|---|---|
| Type system | Static, strict | Static, relatively simple | Dynamic | Static, highly feature-rich |
| Mutability | Immutable by default | Mutable by default | Mutable by default | Mutable by default |
| Block syntax | Curly braces | Curly braces | Indentation | Curly braces |
| Main loop forms | `loop`, `while`, `for` | `for` | `for`, `while` | `for`, `while`, `do-while` |
| Memory management | Ownership and borrowing | Garbage collection | Garbage collection | Manual, RAII, or smart pointers |

The most important conceptual difference is memory management. Rust checks ownership and borrowing at compile time, Go and Python use garbage collection, and C++ offers several approaches including manual management and RAII.

