# IS3014AD
Course assignments

## Thoughts

### CFG

Two phases :

1. Build the AST according to the grammar / syntax
1. Run an execution according to the semantic. This requires a state / an
   environment of all the variables. Also, **executing** a command is fairly
   different from **evaluating** an expression

Running an analysis and building up tests will probably be much easier in
within an SSA form.

### Tests

A test should be generated given a cfg AND a path to go through.

A path is a list of nodes, that can be turned into a list of edges. Each edge
is a *bexp* or a *stmt*. Each *bexp* adds a constraint and some symbols (new
unique registers). Each *stmt* may add some symbols (new unique variables, new
unique registers) and some constraints (between these new symbols).

One must notice that a path must be in SSA form (and this is easy to do!)

## Design

:warning:
When exec-ing a command, the new state is return from the exec call.
But also, the previous state (a dict) is overriden with the new state.
This can be avoided by deep-copying the state before making an assignement.
What should we do?

## TODO

- implement "take a step" for `Com`
- implement a data struct for the state with a copy method used in
  (cfgraph/utils.py)
