|   Issue    |       Type        |       Line(s)     |      Description     | Fix Approach |
--------------------------------------------------------------------------------------------
| Mutable default arg | Bug (Potential) | 8 | `logs=[]` is a mutable default argument, so the same list is shared across all calls to `addItem`. | Change the default to `logs=None` and initialize inside the function: `if logs is None: logs = []`. |
--------------------------------------------------------------------------------------------

| Insecure `eval()` use | Security (Medium) | 59 | `eval()` can execute arbitrary code, posing a significant security risk. (Flagged by Bandit and Pylint). | Remove the `eval()` call entirely. If dynamic evaluation is truly needed, use `ast.literal_eval`. |
--------------------------------------------------------------------------------------------

| Bare 'except' block | Bug (Potential) | 19 | `except:` catches all exceptions, including `SystemExit`, hiding bugs and making the code hard to debug. (Flagged by Pylint, Bandit, and Flake8). | Replace `except:` with specific exceptions, such as `except KeyError:` (if the item doesn't exist) or `except TypeError:`. |
--------------------------------------------------------------------------------------------

| No type/value validation | Bug | 8, 14 | The `addItem` function accepts non-string items and negative quantities (see line 50, 51). | Add type and value validation at the start of `addItem` and `removeItem` (e.g., check `isinstance(item, str)` and `qty > 0`). |
--------------------------------------------------------------------------------------------

| Improper file handling | Resource Mgmt | 26, 32 | `open()` is used without a `with` statement, which can lead to resource leaks if an error occurs before `f.close()`. | Use a `with` block for opening files: `with open(file, "w", encoding="utf-8") as f:`. |
--------------------------------------------------------------------------------------------

| Missing encoding | Bug (Potential) | 26, 32 | `open()` is called without specifying an `encoding`, which can fail on different operating systems. (Flagged by Pylint). | Specify `encoding="utf-8"` in all `open()` calls. |
--------------------------------------------------------------------------------------------

| Use of `global` | Code Smell / Design | 5, 27 | Using `global stock_data` makes the code hard to test and reason about by modifying a global state. (Flagged by Pylint). | Refactor the code into an `Inventory` class to manage `stock_data` as an instance attribute. |
--------------------------------------------------------------------------------------------

| Unused import | Style / Cleanup | 2 | The `logging` module is imported but never used. (Flagged by Flake8 and Pylint). | Remove the `import logging` line. |
--------------------------------------------------------------------------------------------

| Naming convention | Style | 8, 14, 22+ | Function names use `camelCase` (e.g., `addItem`) instead of the standard Python `snake_case`. (Flagged by Pylint). | Rename all functions to `snake_case` (e.g., `add_item`, `remove_item`, `get_qty`) and update their calls. |
--------------------------------------------------------------------------------------------

| Missing docstrings | Style / Maintainability | 1, 8, 14+ | The module and all functions lack docstrings, making the code hard to understand. (Flagged by Pylint). | Add a module-level docstring and docstrings to all functions describing their purpose, parameters, and return values. |
--------------------------------------------------------------------------------------------

| Old string formatting | Style | 12 | Uses old `%` formatting instead of a modern f-string. (Flagged by Pylint). | Convert the string to an f-string: `f"{datetime.now()}: Added {qty} of {item}"`. |
--------------------------------------------------------------------------------------------

| Whitespace/Formatting | Style | Multiple | Inconsistent blank lines between functions. (Flagged by Flake8). | Run an auto-formatter like `black` or `autopep8`, or manually add/remove lines to conform to PEP 8. |
--------------------------------------------------------------------------------------------


Reflection
The easiest fixes were simple cleanup, like deleting unused imports or fixing spacing. The hardest fixes were the hidden bugs, like the logs=[] issue, and design problems, like the use of a global variable. Those required deeper knowledge and bigger code changes.

False Alarms: The tools were accurate. There were no real false positives. The only thing close was the tool complaining about function names (e.g., addItem), which was technically correct but might be ignored by a team if they have a different style guide.

How to Use These Tools: You'd use them in two main places:

Locally: In your code editor (like VS Code) to get live feedback, and with "pre-commit hooks" to stop bad code from being saved.

Automatically: In a "CI pipeline" (like GitHub Actions) to check all code before it's merged into the main project, blocking any bad pull requests.

What Got Better: The code improved a lot. It is now:

More Secure: Removing eval() closed a major security hole.

More Robust: Fixed a key bug (with the logs) and ensured the program reports errors properly instead of just failing silently.

Easier to Read: The code is cleaner, more organized, and easier for another person to understand.