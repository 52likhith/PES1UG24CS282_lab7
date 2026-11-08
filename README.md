# Highway Toll Calculator — Lab 7 Fuzz Testing

A Python application for validating vehicle registration plates, calculating toll trip costs, and classifying vehicles by axle count. The project includes both fixed example tests and property-based fuzz tests written with Hypothesis.

## Requirements

- Python 3.12 or later
- pytest
- Hypothesis

Install the test dependencies:

```powershell
python -m pip install pytest hypothesis
```

## Run the application

From the project directory, run:

```powershell
python highway_toll.py
```

The interactive program prompts for a vehicle plate, a trip count and rate, and an axle count.

## Functions

### `parse_plate(plate)`

Parses a four-part, hyphen-separated registration plate and returns the normalized state, district number, and plate number.

Example:

```python
parse_plate("KA-05-AB-1234")
# ("KA", 5, 1234)
```

### `trip_cost(text)`

Calculates the cost of one trip description in `count x rate` format.

Example:

```python
trip_cost("3x150")
# 450
```

### `axle_class(axles)`

Classifies a vehicle by axle count:

| Axles | Class |
|------|-------|
| 2 | `car` |
| 3–4 | `truck` |
| 5 or more | `heavy` |

The function accepts non-negative integers and integer strings.

## Run the tests

Run all tests with:

```powershell
python -m pytest
```

The test suite covers valid inputs, malformed input, type errors, boundary values, and automatically generated inputs from Hypothesis.

To run a single test file:

```powershell
python -m pytest test_highway_toll.py
```

## Project files

| File | Description |
|------|-------------|
| `highway_toll.py` | Toll calculator implementation and interactive entry point |
| `test_highway_toll.py` | Unit and Hypothesis fuzz tests |
| `screenshots/` | Captures of the application and fuzz-test results |
| `screenshots.pdf` | Combined screenshot report |
