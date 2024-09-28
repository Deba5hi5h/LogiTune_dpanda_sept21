

# **CODING GUIDELINES:**

Recommended google guideline: https://google.github.io/styleguide/pyguide.html


### 1. Logitech has a copyright banner that should be added to all the files that has been created by any developer:
```python
# Copyright (c) 2022 Logitech Inc.
# All rights reserved
```
### 2. Docstrings
- classes
```python
class SampleClass:
    """Summary of class here.

    Longer class information....
    Longer class information....

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """

    def __init__(self, likes_spam: bool = False):
        """Inits SampleClass with blah."""
        self.likes_spam = likes_spam
        self.eggs = 0
```
- functions and methods
```python
def verify_framing_speed_default_unselected(self, timeout: int) -> None:
    """
    Method to verify default option for Framing Speed is not selected

    :param timeout: sync timeout
    :return none
    """
    e = self.look_element(SyncAppLocators.FRAMING_SPEED_DEFAULT)
    while timeout > 0:
        if not e.is_selected():
            break
        timeout = timeout - 1
        time.sleep(1)
    if not e.is_selected():
        Report.logPass("Sync App: Framing Speed Default is not selected")
    else:
        Report.logFail("Sync App: Framing Speed Default is selected")
```
- tests
````python
class TestSomething(LCITestCase):
 ...
 def test_001_verifying_something(self) -> None:
 """Verification of something <--- This is first doc line
 This test sends a message to REST server to verify something, it will
fail if REST response is not acceptable...
````

### 3. Naming conventions:

| TYPE                       | PUBLIC | INTERNAL |
|----------------------------|--------|----------|
| Packages                   |lower_with_under|| 
| Modules (Filenames)        |lower_with_under|_lower_with_under|
| Classes                    |CapWords| _CapWords|
| Exceptions                 |CapWords||
| Functions                  |lower_with_under()|   _lower_with_under()|
| Global/Class Constants     |CAPS_WITH_UNDER| _CAPS_WITH_UNDER|
| Global/Class Variables     |lower_with_under|_lower_with_under|
| Instance Variables         |lower_with_under|_lower_with_under (protected)|
| Methods Names              |lower_with_under()|_lower_with_under() (protected)|
| Function/Method Parameters |lower_with_under||
| Local Variables            |lower_with_under||

#### A. Names to Avoid
- single character names, except for specifically allowed cases:
  - counters or iterators (e.g. i, j, k, v, et al.)
  - e as an exception identifier in try/except statements.
  - f as a file handle in with statements

Please be mindful not to abuse single-character naming. Generally speaking, descriptiveness should be proportional to the name’s scope of visibility. For example, i might be a fine name for 5-line code block but within multiple nested scopes, it is likely too vague.

- dashes (-) in any package/module name
- __double_leading_and_trailing_underscore__ names (reserved by Python)
- offensive terms
- names that needlessly include the type of the variable (for example: id_to_name_dict)

#### B. Naming Conventions
- “Internal” means internal to a module, or protected or private within a class.
- Prepending a single underscore (_) has some support for protecting module variables and functions (linters will flag protected member access).
- Prepending a double underscore (__ aka “dunder”) to an instance variable or method effectively makes the variable or method private to its class (using name mangling); we discourage its use as it impacts readability and testability, and isn’t really private. Prefer a single underscore.
- Place related classes and top-level functions together in a module. Unlike Java, there is no need to limit yourself to one class per module.
- Use CapWords for class names, but lower_with_under.py for module names. Although there are some old modules named CapWords.py, this is now discouraged because it’s confusing when the module happens to be named after a class. (“wait – did I write import StringIO or from StringIO import StringIO?”)
- Underscores may appear in unittest method names starting with test to separate logical components of the name, even if those components use CapWords. One possible pattern is test<MethodUnderTest>_<state>; for example testPop_EmptyStack is okay. There is no One Correct Way to name test methods.

### 4. Type Annotated Code

Type annotations improve the readability and maintainability of your code. The type checker will convert many runtime errors to build-time errors

Type annotations (or “type hints”) are for function or method arguments and return values:

```python
def func(a: int) -> List[int]:
```

You can also declare the type of a variable using similar PEP-526 syntax:

```python
a: SomeType = some_func()
```

### 5. Exception handling

One of the least tested python code is inside the Exception handling blocks, please be
mindful to test your code’s exception handling.

A. Use of `try/except` is strongly recommended where appropriate.

B. Any function / code block that has a possibility to raise an exception should catch the
exception and raise it all the way up to the test case so that the test case can act on
the exception.

C. Minimize the amount of code in a `try/except` block. The larger the body of the try, the more likely that an exception will be raised by a line of code that you didn’t expect to raise an exception. In those cases, the try/except block hides a real error.

D. Use the `finally` clause to execute code whether or not an exception is raised in the try block. This is often useful for cleanup, i.e., closing a file.

### 6. Line length

TBD