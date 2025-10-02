# Javascript

## Variables

### Data Type

1. **Number**: Represents both integer and floating-point numbers. For example, `let age = 25;` or `let price = 99.99;`.

2. **String**: Represents textual data. It's denoted by single or double quotes. For example, `let name = "Alice";`.

3. **Boolean**: Represents a logical entity and can have two values: `true` or `false`. For example, `let isActive = true;`.

4. **Undefined**: A variable that has not been assigned a value has the value `undefined`. For example, `let result;`.

5. **Null**: Represents the intentional absence of any object value. For example, `let empty = null;`.

6. **Array**: Designed to store lists of data and are typically used for ordered data. They are accessed using numeric indices

   - **Dynamic Size:** Arrays in JavaScript are dynamic, meaning they can grow or shrink in size as needed.
   - **Heterogeneous Elements:** UJavaScript arrays can store different types of elements in the same array. You can have numbers, strings, objects, etc., all in one array.
   - **Array Properties and Methods:** JavaScript arrays have many built-in methods for manipulation and traversal.
     - `length` property gives the number of elements in the array
     - `push()` and `pop()` for adding/removing elements from the end
     - `shift()` and `unshift()` for adding/removing elements from the beginning
     - `slice()` for extracting a portion of an array
     - `splice()` for adding/removing elements from a specific index
     - `map()`, `filter()`and `reduce()` for more complex operations
     - `forEach()` allow for iterating over each element.
     - spread operator (`...`) for easy copying and combining of arrays, and `for...of` loops for iterating over array elements.

   - **Creating Arrays:**
     - **Use `const`** if you want to ensure that the reference to the array does not change. This is a common practice to signal to other developers that the variable should not be reassigned. It helps in maintaining the integrity of your references.
     - **Use `let`** if you anticipate that you will need to reassign the array to a different array or a different value at some point in your code.
   - **Pass by Reference:**In JavaScript, arrays are reference types. When you assign an array to a new variable, it refers to the same array. Modifications to the array through one variable are reflected in the other.

7. **Object**: Objects in JavaScript are collections of properties. They are used to store keyed collections of various data and more complex entities

   - **Properties**: An object property is a key-value pair. The key (or property name) is always a string or symbol, and the value can be any type, including another object, which allows for building complex data structures.

   - **Creating Objects**: The simplest way to create an object is using object literal notation:

     ```
     let person = {
         name: "Alice",
         age: 25,
         isStudent: true
     };
     ```

   - **Accessing Properties**: You can access object properties using dot notation or bracket notation:

     ```
     console.log(person.name); // Alice
     console.log(person['age']); // 25
     ```

   - **Methods**: Objects can also contain functions, known as methods. For example:

     ```
     let person = {
         name: "Alice",
         greet: function() {
             console.log("Hello, my name is " + this.name);
         }
     };
     person.greet(); // Hello, my name is Alice
     ```

   - **Mutable Nature**: Objects in JavaScript are mutable. You can add, modify, and delete properties after an object is created.

   - **Reference Type**: Objects are reference types. If you assign an object to another variable, you are copying the reference, not the actual object. Therefore, changes made through one reference are visible through all references.

   - **Functions as Objects**: In JavaScript, functions are objects too. They can have properties and methods.

### Declaration

1. **var**: Introduced in earlier versions of JavaScript. Variables declared with `var` are function-scoped, which means they are recognized within the function in which they are defined, or globally if declared outside any function.
2. **let**: Introduced in ES6 (ECMAScript 2015), `let` allows you to declare block-scoped local variables, optionally initializing them to a value. `let` provides better scoping, reducing the risk of errors.
3. **const**: Also introduced in ES6, `const` is used to declare variables whose values are never intended to change. They are block-scoped like `let` and must be initialized at the time of declaration.

### Scope

- **Global Scope**: A variable declared outside any function has a global scope and is accessible from any part of the code.
- **Local Scope**: Variables declared within a function are local to that function and cannot be accessed from outside the function.
- **Block Scope**: Variables declared with `let` and `const` are block-scoped, meaning they are only accessible within the block (`{}`) where they are defined.
- Variables declared with `var` are hoisted to the top of their scope and initialized with `undefined`.
- `let` and `const` are also hoisted, but accessing them before declaration results in a `ReferenceError`. This is known as the "temporal dead zone."

## Functions

### Definition

1. **Basic Function Syntax**:
   - Functions are declared using the `function` keyword, followed by a name, parameters, and a body.
   - Example: `function f(a, b) { return a + b; }`
   - These functions can return a value or `undefined` implicitly.
   - The `...args` syntax allows functions to accept an indefinite number of arguments.
   - Functions can be created within other functions and returned.
2. **Anonymous Functions**:
   - Functions can be declared without a name and assigned to variables.
   - Example: `var f = function(a, b) { return a + b; }`
3. **Immediately Invoked Function Expression (IIFE)**:
   - Functions can be defined and executed instantly, useful for encapsulating variables within a scope.
   - Example: `const result = (function(a, b) { return a + b; })(3, 4);`
7. **Arrow Functions**:
   - An alternative syntax using `=>` is often preferred for its minimalism.
   - Arrow functions do not hoist and differ in handling `this`, `super`, and `arguments`.
   - Single-line arrow functions can omit the `return` keyword.

### Return

In JavaScript, the `return` statement is used in a function to specify the value that should be returned to the caller of the function.

- **Terminating Function Execution**: When a `return` statement is executed in a function, the function stops executing and returns the specified value to the function caller.
- **Returning a Value**: The `return` statement can be followed by the value that needs to be returned. This value can be a number, a string, an object, an array, or even another function.
- **No Return Value**: If a function doesn’t have a `return` statement, or if the `return` statement doesn’t have an accompanying value, the function returns `undefined`.

### Closure

- **Access to Outer Function Scope**: Closures can remember and access variables and arguments of its outer function even after the outer function has returned.
- **Data Encapsulation**: They can be used to create private variables or functions. This is a powerful feature because it allows you to hide the implementation details of a function, exposing only what is necessary.
- **Preserving State**: Closures are often used to preserve the state of things. For instance, they are used in event handlers to keep track of state between events.

```javascript
function outerFunction(outerVariable) {
    return function innerFunction(innerVariable) {
        console.log(outerVariable + ' ' + innerVariable);
    };
}

const newFunction = outerFunction('Hello');
newFunction('World'); // Output: "Hello World"

```

### Hoisting

Function hoisting in JavaScript is a behavior where function declarations are moved to the top of their containing scope during the compilation phase. This allows functions to be used before they are declared in the code.

- **Initialization Not Hoisted**: For function expressions, while the variable declaration is hoisted, the initialization or assignment of the function to the variable is not hoisted.
- **Let and Const**: Variables declared with `let` and `const` are hoisted but not initialized. Accessing them before the declaration results in a `ReferenceError`.
- **Best Practices**: Relying on hoisting can make code less readable and lead to errors. It is generally recommended to declare functions and variables at the top of their scope to avoid confusion.

## Error Handling

- **try Block**: You write the code that might throw an error inside the `try` block.

- **catch Block**: If an error occurs in the `try` block, control is passed to the `catch` block. The `catch` block receives an error object containing information about the error.

  ```javascript
  try {
      // Code that may throw an error
      let result = potentiallyRiskyOperation();
  } catch (error) {
      // Code to handle the error
      console.error(error.message);
  }
  ```
  
- **finally Block**: Optionally, a `finally` block can be used after the `catch` block. Code inside `finally` always executes, regardless of whether an error was thrown or caught.

## Async Programming

Asynchronous programming is a critical aspect of JavaScript, allowing you to perform long-running operations without blocking the main execution thread. Understanding how to work with asynchronous operations is essential for building responsive applications, especially in web development.

1. JavaScript runs a piece of code (this code is running on the main thread).
2. When an async operation is encountered (like setTimeout, fetch, etc.), JavaScript sets it up and then continues running the rest of the code. It doesn't wait for the async operation to complete. This async operation might be running in the background but not on the main JavaScript thread.
3. When the async operation completes, its callback function is placed into the task queue.
4. Once the call stack is empty (i.e., all the code in the current turn of the Event Loop has been executed), the Event Loop takes the first task from the task queue and pushes it onto the call stack, which immediately executes it.
5. This process continues, with the Event Loop pushing tasks from the task queue onto the call stack whenever the call stack is empty, allowing JavaScript to handle multiple operations concurrently despite being single-threaded.

### Callbacks

- **Passing Functions as Arguments**: In JavaScript, functions are first-class objects, meaning they can be passed as arguments to other functions, returned by them, and assigned to variables.
- **Executing the Callback**: The function that receives the callback will execute it at the appropriate time. This could be immediately, like in array methods (`forEach`, `map`, `filter`, etc.), or later, such as in asynchronous operations.

```javascript
console.log("Starting the timer...");

// setTimeout returns a Timeout object which can be used to reference the timer
let timeoutId = setTimeout(() => {
  console.log("Timeout completed!");
}, 2000);

// Some condition or logic
if (/* some condition */) {
// Cancels the timeout
  clearTimeout(timeoutId);
}
```

```javascript
console.log("Starting the interval...");

const timer = setInterval(() => {
  console.log("Interval...");
}, 2000);

if (/* some condition */) {
// Cancels the timeout
  clearInterval(timer);
}
```

### Promises

- **Pending:** Initial state.
- **Fulfilled:** Operation completed successfully.
- **Rejected:** Operation failed.

```javascript
const myPromise = new Promise((resolve, reject) => {
  const condition = true;
  if (condition) {
    resolve("Promise resolved");
  } else {
    reject("Promise rejected");
  }
});
```

- `async/await`
  - `async` is used to define an asynchronous function. It ensures that the function always returns a promise. When the `async` keyword is used before a function declaration or function expression, it becomes an asynchronous function.
  - `await` is used to pause the execution of an asynchronous function until a promise is resolved. It can only be used inside an `async` function. When `await` is used before a promise, it waits for the promise to be resolved or rejected. If resolved it proceeds to the next line of code and if the awaited promise is rejected, an exception is thrown.
- `then()/catch()/finally()`
  - `.then()` is a Promise method used to specify what to do when the Promise is fulfilled, i.e., when an asynchronous operation completes successfully. It takes up to two arguments: callback functions for the success and failure cases of the Promise.
  - `.catch()` is a method used to define a callback function that will be executed when the Promise is rejected, i.e., if an error occurs during the asynchronous operation.
  - `.finally` method is a built-in method of a Promise that is always executed, regardless of whether the promise is fulfilled or rejected. This makes it an excellent place to put cleanup code that must be run regardless of the outcome of the promise.
- `Promise.all()`: The `Promise.all()` method is used to handle multiple promises concurrently. It takes an array (or an iterable) of promises as input and returns a new promise that resolves when all the promises in the input array have resolved.