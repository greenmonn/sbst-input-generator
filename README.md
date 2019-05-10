# Search Based Test Input Generation

A Python implementation of automated test data generation.

Currently, it works only for the subset of Python functions satisfying these conditions:

- takes only integer arguments

- had only integer type local variables

- contains predicates that only involve relational operators (==, !=, <, >, <=, >=), integer variables, and calls to functions with integer return type


## Run

```
python -m covgen <file>
```

Additional options can be given:

```
python -m covgen <file> --function (-f) <target_function_name> --method (-m) <avm or hillclimbing> --retry-count (-r) <number>
```

For example:
```
python -m covgen target/calender.py -m avm --retry-count 10
```

prints out list of generated inputs that cover detected branches,
from each function defined in the target file.