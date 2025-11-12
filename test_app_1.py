Here's a Python test file 'test_app_1.py' using pytest, testing the functionality of the `app_1.py` file:

```python
# Import the app under test and pytest
import app_1
from pytest import fixture

# Define a fixture to store application state
@fixture
def app_state():
    return {'market_data': []}

# Test functions for each feature in 'app_1.py'
@pytest.mark.parametrize(
    "function, data, expected_output",
    [
        ("get_market_data", {}, app_state[0]['market_data']], []),
        ("store_ data", {"market_data": []}, app_state),],
)
def test_app_functions(function, data, expected_output):
    # Call the function under test with provided data
    result = function(data) if function else None

    # Assert that the output matches the expected value
    assert result == expected_output, \
        f"Function {function} did not produce the correct output. Expected: {expected_output}, Actual: {result}"

# Run all tests
if __name__ == "__main__":
    pytest.main()
```

This test file includes unit tests for each function in `app_1.py`. The tests use fixture data to simulate different scenarios and check that the functions produce the expected outputs.