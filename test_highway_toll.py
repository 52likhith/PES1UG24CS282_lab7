import pytest
from hypothesis import given, strategies as st
from highway_toll import parse_plate, trip_cost, axle_class


@pytest.mark.parametrize(
    ("plate", "expected"),
    [
        ("KA-05-AB-1234", ("KA", 5, 1234)),
        ("ka-05-ab-1234", ("KA", 5, 1234)),
        (" MH - 05 - AB - 1234 ", ("MH", 5, 1234)),
    ],
)
def test_parse_plate_valid_inputs(plate, expected):
    assert parse_plate(plate) == expected


@given(st.text(max_size=80))
def test_parse_plate_arbitrary_text_is_reasonably_validated(plate):
    try:
        result = parse_plate(plate)
    except (TypeError, ValueError):
        return

    assert isinstance(result, tuple)
    assert len(result) == 3
    assert isinstance(result[0], str)
    assert isinstance(result[1], int)
    assert isinstance(result[2], int)


@given(st.none() | st.integers() | st.lists(st.text(), max_size=5))
def test_parse_plate_rejects_non_string_input(value):
    with pytest.raises((TypeError, ValueError)):
        parse_plate(value)


@pytest.mark.parametrize(
    "plate",
    [
        "",
        "KA05AB1234",
        "KA-05-AB",
        "KA-05-AB-1234-extra",
        "KA--AB-1234",
        "KA-05--1234",
        "KA-no-AB-1234",
        "KA-05-AB-nope",
        "-05-AB-1234",
        "KA-05--",
        "  ",
    ],
)
def test_parse_plate_rejects_malformed_strings(plate):
    with pytest.raises(ValueError):
        parse_plate(plate)


@given(
    st.text(alphabet="0123456789x+- .", max_size=40)
    | st.text(alphabet="ABCxyz0123456789-+.", max_size=40)
)
def test_trip_cost_arbitrary_text_is_rejected_or_computed(text):
    try:
        result = trip_cost(text)
    except (TypeError, ValueError):
        return

    assert isinstance(result, int)
    assert result >= 0


@pytest.mark.parametrize(("text", "expected"), [("3x150", 450), (" 3 X 150 ", 450)])
def test_trip_cost_valid_inputs(text, expected):
    assert trip_cost(text) == expected


@given(st.none() | st.integers() | st.lists(st.text(), max_size=5))
def test_trip_cost_rejects_non_string_input(value):
    with pytest.raises((TypeError, ValueError)):
        trip_cost(value)


@pytest.mark.parametrize(
    "text",
    [
        "",
        "150",
        "3xx150",
        "x150",
        "3x",
        "3x150x2",
        "one x 150",
        "3 x nope",
        "-3x150",
        "3x-150",
        "3.5x150",
        "3x1.5",
        "  ",
    ],
)
def test_trip_cost_rejects_malformed_strings(text):
    with pytest.raises(ValueError):
        trip_cost(text)


@given(st.integers(min_value=0, max_value=1_000_000))
def test_axle_class_valid_non_negative_integers(axles):
    result = axle_class(axles)
    if axles == 2:
        assert result == "car"
    elif axles <= 4:
        assert result == "truck"
    else:
        assert result == "heavy"


@pytest.mark.parametrize(("axles", "expected"), [(2, "car"), (3, "truck"), (4, "truck"), (5, "heavy")])
def test_axle_class_valid_string_and_integer_values(axles, expected):
    assert axle_class(str(axles)) == expected
    assert axle_class(axles) == expected


@given(st.text(alphabet=st.characters(), max_size=40))
def test_axle_class_arbitrary_text_is_validated(text):
    try:
        result = axle_class(text)
    except (TypeError, ValueError):
        return

    assert result in {"car", "truck", "heavy"}


@given(st.one_of(st.integers(max_value=-1), st.floats().filter(lambda value: not value.is_integer())))
def test_axle_class_rejects_negative_and_non_integral_values(axles):
    with pytest.raises((TypeError, ValueError)):
        axle_class(axles)


@given(st.none() | st.lists(st.text(), max_size=5))
def test_axle_class_rejects_non_scalar_inputs(value):
    with pytest.raises((TypeError, ValueError)):
        axle_class(value)
