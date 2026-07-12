---
id: NNN
status: draft
links_to_solution_design: NNN
links_to_problem_statement: NNN
---

# Test specification
[Test cases traced to success criteria and acceptance criteria. Covers unit, integration, edge-case, and regression tests.]

## Acceptance criteria trace
[Every success criterion from the problem statement must map to at least one test case.]

| Success criterion (from problem statement) | Test case(s) |
|---|---|
| [SC1: description] | [UNIT-X / INT-X] |

## Unit tests
[Tests for individual functions in isolation with mocked dependencies. One table per function.]

### [Function name]

| Test case | Test data / setup | Expected result |
|---|---|---|
| [What is being tested] | [Input values and mock setup] | [What the function should return or do] |

## Integration tests
[Tests that exercise multiple components together. Use real or test-container databases where practical, not mocks.]

| Test case | Components exercised | Setup | Expected result |
|---|---|---|---|
| [What is being tested] | [Which components] | [Test environment setup] | [Expected outcome] |

## Edge cases and boundary tests
[Empty input, maximum values, concurrent access, missing dependencies, timeouts, null fields, duplicate submissions.]

| Test case | Edge condition | Expected result |
|---|---|---|
| [What is being tested] | [The unusual input or state] | [What should happen] |

## Regression tests
[Existing behaviour that must not break. Reference the known-callers register for callers of changed shared components.]

| Test case | Existing behaviour preserved | Caller(s) affected |
|---|---|---|
| [What is being tested] | [Behaviour that must still work] | [Which callers depend on this] |
