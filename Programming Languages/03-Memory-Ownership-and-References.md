# 03 Memory, Ownership, and References

## Table of Contents

1. [Overview](#overview)
2. [Core Concepts](#core-concepts)
   - [Memory and Lifetime](#memory-and-lifetime)
   - [Names, Values, and References](#names-values-and-references)
   - [Ownership and Resource Cleanup](#ownership-and-resource-cleanup)
   - [Copies, Moves, and Aliases](#copies-moves-and-aliases)
   - [References and Mutation](#references-and-mutation)
   - [Slices and Views](#slices-and-views)
3. [Concept Mapping](#concept-mapping)
4. [References](#references)

## Overview

Programming languages need rules for managing memory, resources, and access to shared data. The key concepts in this note are lifetime, ownership, cleanup, copies, moves, aliases, references, mutation, slices, and views.

These concepts appear in Rust, Go, Python, and C++, but each language maps them to different language features and safety guarantees. Each concept below is explained generally, followed by relevant code examples in the four languages.

## Core Concepts

### Memory and Lifetime

A value's **lifetime** is the period during which it is valid and can be used.

The **stack** commonly stores fixed-size local values and function-call data. The **heap** commonly stores dynamically sized or shared data. These are useful implementation models, not the language rules themselves: a compiler can choose different storage locations without changing ownership or lifetime semantics. The practical question is: **who keeps a value alive, and when is it released?**

#### Rust

Rust values are valid within their scope. A heap-owning value is dropped when its owner leaves that scope.

~~~rust
{
    let message = String::from("hello");
    println!("{message}");
} // message is dropped here
~~~

#### Go

Go's garbage collector keeps reachable heap data alive. A local variable can safely escape a function when it is still needed.

~~~go
func makeNumber() *int {
    number := 42
    return &number
}
~~~

#### Python

Python objects remain alive while they are reachable through names or other objects.

~~~python
def make_list():
    values = [1, 2, 3]
    return values

numbers = make_list()
~~~

#### C++

C++ objects normally have a deterministic lifetime. A local object is destroyed when its enclosing scope ends.

~~~cpp
{
    std::string message = "hello";
    std::cout << message << "\n";
} // message is destroyed here
~~~

### Names, Values, and References

A variable name can hold a value directly or refer to an object/value stored elsewhere. Assignment can therefore copy data, transfer responsibility, or create another path to the same data.

```text
copy:   first [1, 2]       second [1, 2]
alias:  first ─┐
               ├──> [1, 2]
        second ─┘
move:   first (unusable)   second [1, 2]
```

This model explains why mutation through one alias can be observed through another. It also explains why a pointer, slice, reference, or view must not outlive the data it refers to. Rust checks many such cases at compile time; garbage-collected languages preserve reachable objects; C++ requires the programmer to preserve the relevant lifetime.

### Ownership and Resource Cleanup

**Ownership** means responsibility for a value or resource. A resource may be heap memory, an open file, a network connection, or a locked mutex.

A resource must be released exactly once. Languages use different cleanup strategies: deterministic scope-based cleanup, garbage collection, or explicit cleanup helpers.

#### Rust

The owner of a value is responsible for it. Rust runs **Drop** automatically when the owner leaves scope.

~~~rust
let message = String::from("hello");
println!("{message}");
// message is dropped at the end of the enclosing scope
~~~

#### Go

Go collects ordinary memory automatically. Use **defer** for external resources such as files.

~~~go
func readNote() error {
    file, err := os.Open("notes.txt")
    if err != nil {
        return err
    }
    defer file.Close()

    return nil
}
~~~

#### Python

Python automatically manages ordinary object memory. Use **with** to reliably close external resources.

~~~python
with open("notes.txt") as file:
    text = file.read()
# file is closed here
~~~

#### C++

C++ commonly uses RAII: an object's destructor releases its resource when the object leaves scope.

~~~cpp
#include <fstream>

{
    std::ifstream file{"notes.txt"};
    // Use file.
} // file's destructor closes it here
~~~

### Copies, Moves, and Aliases

When assigning one variable to another, one of three broad outcomes is possible:

| Outcome | Meaning |
|---|---|
| **Copy** | The new variable receives an independent value. |
| **Move** | Responsibility transfers to the new variable. |
| **Alias** | Both variables can access the same underlying object or data. |

#### Rust

Assigning a heap-owning **String** moves ownership. Use **clone** for an independent copy.

~~~rust
let first = String::from("hello");
let second = first;

// println!("{first}"); // Error: first was moved.

let original = String::from("copy me");
let copied = original.clone();
~~~

#### Go

Arrays are copied, but assigning a slice can create an alias to shared underlying storage.

~~~go
first := []string{"hello"}
second := first

second[0] = "hi"
fmt.Println(first) // [hi]
~~~

#### Python

Assignment binds another name to the same object. A list copy can be made with **list()**.

~~~python
first = ["hello"]
second = first
second[0] = "hi"

copied = list(first)
copied[0] = "hello again"
~~~

The `list(first)` copy is **shallow**: nested mutable objects are still shared. Use a deliberate deep-copy operation only when independent nested state is required.

#### C++

Ordinary assignment commonly copies an object. **std::move** asks the type to transfer resources when possible.

~~~cpp
#include <string>
#include <utility>

std::string first = "hello";
std::string copied = first; // Copy

std::string source = "move me";
std::string destination = std::move(source);
~~~

After a C++ move, the source object remains valid but its exact value should not be relied on until it is assigned a new value.

### References and Mutation

A **reference** or **pointer** provides access to data owned somewhere else. Read-only access inspects a value; mutable access changes it.

Languages choose different rules for combining read-only and mutable access. Some allow aliases freely, while others enforce exclusive mutation.

#### Rust

**&T** is a shared, read-only borrow. **&mut T** is an exclusive mutable borrow.

~~~rust
fn length(text: &String) -> usize {
    text.len()
}

fn append_world(text: &mut String) {
    text.push_str(", world");
}
~~~

#### Go

A pointer lets a function modify a caller's value. Other aliases may still exist.

~~~go
func addOne(number *int) {
    *number += 1
}

score := 10
addOne(&score)
~~~

#### Python

Function parameters are names bound to objects. Mutating a passed mutable object affects the caller's object.

~~~python
def add_language(items):
    items.append("Rust")

languages = ["Go"]
add_language(languages)
~~~

#### C++

A **const** reference communicates read-only access. A non-const reference allows mutation.

~~~cpp
std::size_t length(const std::string& text) {
    return text.size();
}

void append_world(std::string& text) {
    text += ", world";
}
~~~

### Slices and Views

A **slice** or **view** represents part of an existing sequence without necessarily owning a new copy of the data.

Views avoid copying, but the original data must remain valid as long as the view is used. Some language views share storage; others make a copy.

#### Rust

A slice borrows part of a collection without owning it.

~~~rust
let numbers = [10, 20, 30, 40];
let middle: &[i32] = &numbers[1..3];

println!("{middle:?}"); // [20, 30]
~~~

#### Go

A slice is a view into an underlying array. Modifying the view can modify the original slice.

~~~go
numbers := []int{10, 20, 30, 40}
middle := numbers[1:3]

middle[0] = 99
fmt.Println(numbers) // [10 99 30 40]
~~~

#### Python

A list slice produces a new list. Use **memoryview** for a view over binary data.

~~~python
numbers = [10, 20, 30, 40]
middle = numbers[1:3]

middle[0] = 99
print(numbers)  # [10, 20, 30, 40]
~~~

#### C++

**std::span** is a non-owning view over contiguous data. The original collection must outlive the span.

~~~cpp
#include <span>
#include <vector>

std::vector<int> numbers{10, 20, 30, 40};
std::span<int> middle = std::span{numbers}.subspan(1, 2);

middle[0] = 99;
~~~

**Common mistakes:** retaining a small Go slice that keeps a large backing array reachable, using a C++ `std::span` after its source is destroyed or reallocated, and expecting a Python list slice to be a view. A Rust slice cannot outlive its borrowed data, but it can still become logically stale if the underlying value changes through a permitted path.

## Concept Mapping

| Question | Rust | Go | Python | C++ |
|---|---|---|---|---|
| Who releases heap memory? | Owner's **Drop** implementation | Garbage collector | Garbage collector | Object destructor / RAII object |
| Does assignment invalidate the source? | Often, for non-**Copy** values | No | No | Only explicit move operations transfer resources |
| Can two names share mutable data? | Not through conflicting borrows | Yes | Yes | Yes |
| How is read-only access expressed? | **&T** | Convention or value/pointer choice | Convention and immutable types | **const T&** |
| How is mutation through another function expressed? | **&mut T** | Pointer, slice, or map | Mutable object passed to function | **T&** or **T*** |
| Are dangling ordinary references prevented? | Yes, by compile-time checking | Managed heap values remain alive while reachable | Objects remain alive while reachable | Not universally; raw references and pointers can dangle |
| Closest construct to a Rust slice | **&[T]**, **&str** | Slice | **memoryview** for shared views | **std::span** |

## References

- [The Rust Programming Language — Chapter 4: Understanding Ownership](https://doc.rust-lang.org/stable/book/ch04-00-understanding-ownership.html)
- [The Rust Programming Language — References and Borrowing](https://doc.rust-lang.org/stable/book/ch04-02-references-and-borrowing.html)
- [Go Language Specification](https://go.dev/ref/spec)
- [Go Garbage Collector Guide](https://go.dev/doc/gc-guide)
- [Python Data Model](https://docs.python.org/3.14/reference/datamodel.html)
- [C++ object lifetime (working draft)](https://eel.is/c++draft/basic.life)
