# PrograLang

## Description
**PrograLang** (short for "Programming Language") is a personal experimental project built in pure Python that demonstrates the process of creating a custom programming language from scratch. This project implements a full pipeline: from lexical analysis to parsing, intermediate representation (POLIZ), and finally generating executable code for the .NET CLR.

The language is minimalistic and currently supports basic constructs like variable declarations, arithmetic operations, conditional statements (`if`, `else`, `end`), and simple data types. The resulting program is compiled into an `.il` file which can be executed using the CLR.

## Features
- Custom file-based language input (`test.ruby`).
- Lexical analysis and token generation.
- Parsing logic to generate intermediate representation (POLIZ).
- POLIZ (Polish notation-style intermediate code) used for order of execution and context management.
- Code generation to `.il` file for CLR compilation.
- Support for:
  - Data types: `int`, `float`
  - Conditional blocks: `if`, `else`, `end`
  - Comparison operators: `>`, `<`
- No external Python libraries used — pure Python implementation.

### Limitations
- Negative numbers are not supported.
- Limited set of data types and control structures.
- Only supports a simple subset of programming logic.

## Technologies Used
- **Language:** Python (no external libraries)
- **Target:** .NET CLR (IL code generation)

## How to Run
1. Write your custom code in the `test.ruby` file.
2. Run the main Python script:
   ```bash
   python main.py
   ```
3. The program will:
   - Tokenize the input code
   - Parse the token table
   - Generate POLIZ (intermediate representation)
   - Output an `.il` file
   - Optionally compile it using a CLR-compatible compiler

## Example Syntax
```ruby
int x = 5
float y = 3.14
if x > 3
  float z = y
else
  int z = x
end
```


