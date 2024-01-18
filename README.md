# Paint Estimation Tool

## Description

This Python tool helps estimate the amount of paint needed for a wall, calculates the cost, and determines the required paint buckets. It includes functions to gather information about the wall, handle obstructions, and choose paint options.

## Functions

### `wallSize()`

Collects information about the length and width of a wall, ensuring valid numerical entries within the range of 0.01 to 500 meters. Calculates the total wall size and subtracts the area occupied by obstructions.

### `obstructions(wall_size)`

Determines if there are obstructions on a wall, calculates and returns the total area occupied by the obstructions. If no obstructions are present, returns 0.

### `bucketsCalc(final_area)`

Calculates the number of paint buckets needed to cover a given area, considering available bucket sizes (10L, 5L, 2L, and 1L).

### `finish(total_size)`

Calculates the cost and required paint buckets for finishing a wall, considering the number of coats, total wall size, and user-selected paint brand.

## Usage

1. Run the Python file `BnQ_paint.py` in the terminal.
2. Follow the on screen instructions to finalise the paint amount, cost, and buckets needed.

## Example

```powershell
# Example usage
python ../path_to_file/BnQ_paint.py
```

## Dependencies

This project has a dependency on the `math` library, which is a standard library in Python.

## License

This project is licensed under the MIT License.
