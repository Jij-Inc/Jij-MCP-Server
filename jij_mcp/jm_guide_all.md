JijModeling Guides
# Placeholder
```
import jijmodeling as jm

# array parameter
d = jm.Placeholder("d", ndim=2, description="Description of d")

# scalar parameter
c = jm.Placeholder("c", description="Description of c")

# shape of array parameter
n = d.len_at(0, latex="n")  # n is the length of the first dimension of d
m = d.len_at(1, latex="m")  # m is the length of the second dimension of d
```
# Decision Variables
```
# shape of array parameter
n = d.len_at(0, latex="n")  # n is the length of the first dimension of d
m = d.len_at(1, latex="m")  # m is the length of the second dimension of d

# You have to define shape for BinaryVar, IntegerVar, and ContinuousVar
x = jm.BinaryVar("x", shape=(n, m), description="Description of x")

# You can use the scalar placeholders as the lower_bound and upper_bound arguments for IntegerVar and ContinuousVar
# You need to set lower_bound and upper_bound for IntegerVar and ContinuousVar
z = jm.IntegerVar("z", lower_bound=0, upper_bound=X, shape=(n,), description="Description of z")
y = jm.ContinuousVar("y", lower_bound=0, upper_bound=Y shape=(m,), description="Description of y")
```

## Complex case lower bound and upper bound
If you want to set the lower bound and upper bound for each element of the decision variable, first you set overparameterized lower bound and upper bound.
Then you can set the lower bound and upper bound for each element of the decision variable with Constraint object.

```
# 10000 is overparameterized value
z = jm.IntegerVar("z", lower_bound=0, upper_bound=10000, shape=(n,), description="Description of z")

i = jm.Element("i", belong_to=(0, n))

problem = jm.Problem("Problem_Name", sense=jm.ProblemSense.MINIMIZE)
# Define lower bound and upper bound
K = jm.Placeholder("K", ndim=1, description="Description of K")
problem += jm.Constraint("z_upper_bound", z[i] <= K[i], forall=[i])
```

# summation and element guide

"# Element
Element objects are used to represent indices for multi-dimensional variables in JijModeling. They are created using the `jm.Element` class with the following syntax:
```
# Element in a range
element_name = jm.Element("element_name", belong_to=(lower_bound, upper_bound))

# Element in a set
element_name = jm.Element("element_name", belongs_to=set_of_indices)
# set_of_indices can is a 1D Placeholder object

# Element in a set but Element is also set
# i in a in A
A = jm.Placeholder("A", ndim=2, description="Description of A")
a = jm.Element("i", belongs_to=A)  # a is 1D Element object
i = jm.Element("i", belongs_to=a)  # i is 0D Element object
```

```
# Create a Problem object
problem = jm.Problem("Problem_Name", sense=jm.ProblemSense.MINIMIZE)

# Define the objective function using jm.sum() and Element objects
i = jm.Element("i", belong_to=(0, n))
j = jm.Element("j", belong_to=(0, m))

# Objective function example
# You can just use `+=` to add the objective function to the problem
problem += jm.sum([i, j], d[i, j]*x[i, j])

# conditional summation
jm.sum([(i, i > 0)], d[i]*x[i])
```
# Objective Function
# Problem Object and objective function
```
# Create a Problem object
problem = jm.Problem("Problem_Name", sense=jm.ProblemSense.MINIMIZE)

# Define the objective function using jm.sum() and Element objects
i = jm.Element("i", belong_to=(0, n))
j = jm.Element("j", belong_to=(0, m))

# Objective function example
# You can just use `+=` to add the objective function to the problem
problem += jm.sum([i, j], d[i, j]*x[i, j])

# conditional summation
jm.sum([(i, i > 0)], d[i]*x[i])

# multi conditional summation
# you can connect multiple conditions with `&`, `|` operators
jm.sum([(i, (0 < i) & (i <= 10)), (j, j < 5)], d[i, j]*x[i, j])
```
# How to implement constraints in JijModeling

Constraint objects are created using the `jm.Constraint` class with the following syntax:
```
constraint_name = jm.Constraint("constraint_name", constraint_expression, forall=[i, j, k])
```

API
```
def Constraint(name: str, condition: Condition, forall: list) -> Constraint:
```

Example:
add constraint object via `+=`
```
problem += jm.Constraint("constraint_name", jm.sum([i], x[i, j]), forall=[j])
```

condition forall is represented as a tuple
```
problem += jm.Constraint("constraint_name", jm.sum([i], x[i, j]), forall=[(j, j > 0)])

# no forall constraint you don't need to use forall.
problem += jm.Constraint("sample", jm.sum([i], d[i]*x[i]) <= c)

# multiple conditions
# you can connect multiple conditions with `&`, `|` operators
problem += jm.Constraint("constraint_name", jm.sum([i], x[i, j]), forall=[(j, (j > 0) & (j <= 10)), (i, i < 10)])
```

# If you want to use set operations, you need to convert the another representation
```
# Example1 (representing i in A condition):
# i is sweeped from 0 to n-1 (=C) and A is a set of indices
# x_i == 1 forall i in C | i in A
# You cannot represent this directly in JijModeling
# So you have to handle this condition by your preprocess data preparation.
# That means you have to prepare set C \cap A as follows:
CcapA = jm.Placeholder("CcapA", ndim=1, description="CcapA")
i = jm.Element("i", belongs_to=CcapA) # i in C \cap A
problem += jm.Constraint("constraint_name", x[i] == 1, forall=[i])
```
