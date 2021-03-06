# Search Based Test Input Generation

A Python implementation of automated test data generation.

Currently, it works only for the subset of Python functions satisfying these conditions:

- takes only integer arguments

- had only integer type local variables

- contains predicates that only involve relational operators (==, !=, <, >, <=, >=), integer variables, and calls to functions with integer return type


## Run from Source

If directly clone the source and run package, run below command on project root directory.

```
python -m covgen <file>
```

Additional options can be given (you can remain it as default value):

```
--function (-f) <target_function_name> 

--method (-m) <avm or hillclimbing> 

--retry-count (-r) <retry count> 

--int-min <minimum value of initial arguments for heuristic methods> 

--int-max <maximum value of initial arguments for heuristic methods>
```

For example:
```
python -m covgen target/triangle.py -m avm --retry-count 10 --int-min 0 --int-max 1000
```

prints out list of generated inputs that cover detected branches,
from each function defined in the target file.


## Using pip

This input generator package is available on PyPI of name `covgen`. 

After installing the dependencies:

```
pip install anytree
pip install astor
```

You can install this package with below command:

```
pip install covgen
```

Then run it anywhere with your python.

```
python -m covgen <target file location>
```

Or, you can build your own program using generated inputs.

```python
from covgen.run.inputgenerator import InputGenerator

generator = InputGenerator('target/triangle.py', function_name='triangle')

inputs = generator.generate_all_inputs()

print(inputs['triangle'])
```