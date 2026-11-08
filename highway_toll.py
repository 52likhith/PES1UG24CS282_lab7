def _require_string(value, name):
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")


def _parse_non_negative_integer(value, name):
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a non-negative integer")

    if not isinstance(value, str):
        raise TypeError(f"{name} must be a non-negative integer")

    unsigned = value[1:] if value.startswith(('+', '-')) else value
    if not unsigned.isdigit():
        raise ValueError(f"{name} must be a non-negative integer")

    number = int(value)

    if number < 0:
        raise ValueError(f"{name} must be a non-negative integer")

    return number


def parse_plate(plate):
    _require_string(plate, "plate")

    components = [component.strip() for component in plate.split('-')]
    if len(components) != 4:
        raise ValueError("plate must contain exactly four hyphen-separated components")
    if any(component == "" for component in components):
        raise ValueError("plate components must not be empty")

    state, district, series, number = components
    district_number = _parse_non_negative_integer(district, "district")
    plate_number = _parse_non_negative_integer(number, "plate number")

    return state.upper(), district_number, plate_number


def trip_cost(text):
    _require_string(text, "trip text")

    components = [component.strip() for component in text.lower().split('x')]
    if len(components) != 2:
        raise ValueError("trip text must contain exactly one x separator")
    if any(component == "" for component in components):
        raise ValueError("trip count and rate must not be empty")

    count = _parse_non_negative_integer(components[0], "trip count")
    rate = _parse_non_negative_integer(components[1], "rate")
    return count * rate


def axle_class(axles):
    if isinstance(axles, bool) or isinstance(axles, float):
        raise TypeError("axle count must be an integer or integer string")

    if isinstance(axles, str):
        axles = axles.strip()
        if not axles:
            raise ValueError("axle count must be a non-negative integer")
        unsigned = axles[1:] if axles.startswith(('+', '-')) else axles
        if not unsigned.isdigit():
            raise ValueError("axle count must be an integer string")
        n = int(axles)
    elif isinstance(axles, int):
        n = axles
    else:
        raise TypeError("axle count must be an integer or integer string")

    if n < 0:
        raise ValueError("axle count must be non-negative")
    if n == 2:
        return 'car'
    if n <= 4:
        return 'truck'
    return 'heavy'

def main():
    print("==== Running parse_plate ====")
    user_input = input("Enter a plate (e.g. KA-05-AB-1234): ")
    result = parse_plate(user_input)
    print("State, District and Number:", result)

    print("\n==== Running trip_cost ====")
    user_input = input("Enter trips x rate (e.g. 3x150): ")
    result = trip_cost(user_input)
    print("Trip Cost:", result)

    print("\n==== Running axle_class ====")
    user_input = input("Enter an axle count (e.g. 3): ")
    result = axle_class(user_input)
    print("Vehicle Class:", result)

if __name__ == "__main__":
    main()
