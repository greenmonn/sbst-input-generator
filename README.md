# Search Based Test Input Generation

A Python implementation of automated test data generation.

Currently, it works only for the subset of Python functions satisfying these conditions:

- takes only integer arguments

- had only integer type local variables

- contains predicates that only involve relational operators (==, !=, <, >, <=, >=), integer variables, and calls to functions with integer return type


## Run

```

python -m covgen.run.inputgenerator covgen/target/triangle.py triangle

```

