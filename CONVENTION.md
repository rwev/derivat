# Conventions for derivat

## Naming

### Source Files
Source files should be in Upper Camel Case (a.k.a. Pascal Case), in which several words are joined together, and the first letter of every word is capitalized, e.g. *ExampleSourceFile.py*

### Classes
Classes shall also be named in Upper Camel Case, e.g. 
```python 
class ExampleClass():
```

### Functions 
Functions shall be named in Lower Camel Case, in which several words are joined together, and the first letter of every word is capitalized, **except** the first.

This convention shall be followed for class member functions as well as standalone functions
```python
def doExampleFunction(input_1, input_2):
    # process here
    return result
def isExampleConditionTrue(input_1, input_2):
    # check condition
    return condition_truth
```

### Variables
As demonstrated in the above guidelines for functions, all variables, of **all** types are to follow Snake Case, in which the elements are separated with one underscore character. 
```python
intermediate_value = 5
user_input = raw_input(prompt_str)
class_instance = ExampleClass()
```

### IMPORTS 
Imports shall written in fully-capitalized Snake Case. 
```python
import components.auxiliary.customObjects as CUSTOM_IMPORT 
import SiblingSourceFile as SIBLING 
```

### Spacing 
One empty line shall be present between:
    1. Class definitions;
    2. Functions and other functions;
    3. Functions and their respective bodies.

### Comments
Comments shall be avoided whenever possible, and otherwise deemed as unnecessary in the strive for clean code.  

## Organizational

### Files

#### File Length
All source files should not exceed 250 lines. 
Files shall be broken down and parted out to separate function distinctly and orthagonally. 

## Development
Until there are other contributors, all development will be done by on the master branch and follow the continuously edited TODO.md file in the main project folder.  
