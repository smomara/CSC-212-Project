# American English as a Context-Free Grammar

This repository contains the project "American English as a Context-Free Grammar" developed for the CSC 212 Theory of Computing course in Spring 2023. The project focuses on creating a context-free language model for American English and implementing a parser that constructs a parse tree representing the structure of a sentence generated using the grammar.

## Project Description

The goal of this project is to develop a context-free grammar for American English and implement a parser to parse sentences based on the grammar rules. The project involves the following steps:

1. Identifying the syntax and grammar rules of American English by analyzing the structure of sentences and understanding the interactions between different parts of speech.
2. Developing a set of context-free grammar rules, including nonterminal and terminal symbols, and production rules.
3. Implementing a parser using Java/Python/C++ to parse sentences based on the context-free grammar and construct a parse tree.
4. Testing the context-free grammar by generating random sentences and verifying their validity in American English.

Extra credit extensions to the project may include developing a language model based on the context-free grammar and incorporating semantic information into the grammar for generating more meaningful sentences.

## Project Structure

The repository is structured as follows:
```markdown
|- src/         # Source code directory
|  |- parser.py # Implementation of the parser in Python
|
|- tests/       # Test cases directory
|  |- test1.txt # Example test case file
|
|- README.md    # Project documentation (you are here)
```

## Usage

To use the parser, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/american-english-cfg.git
   ```

2. Navigate to the `src` directory:

   ```bash
   cd american-english-cfg/src
   ```

3. Run the parser script:

   ```bash
   python parser.py
   ```

   Note: Make sure you have Python installed on your system.

4. Follow the on-screen instructions to input sentences and see the resulting parse trees.

## Testing

To test the context-free grammar and parser, you can use the test cases provided in the `tests` directory. Feel free to create your own test cases as well.
