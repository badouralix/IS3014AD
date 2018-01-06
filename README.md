# IS3014AD
Course assignments

## Thoughts

Two phases :

1. Build the AST according to the grammar / syntax
1. Run an execution according to the semantic. This requires a state / an environment of all the variables. Also, **executing** a command is fairly different from **evaluating** an expression

Running an analysis and building up tests will probably be much easier in within an SSA form.

## Design

:warning:
When exec-ing a command, the new state is return from the exec call.
But also, the previous state (a dict) is overriden with the new state.
This can be avoided by deep-copying the state before making an assignement.
What should we do?

## TODO

- implement "take a step" for `Com`
- implement a data struct for the state with a copy method used in (cfgraph/utils.py)
