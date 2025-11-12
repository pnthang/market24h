Here is the unit test for the 'app_1.py' code:

```python
# test_ app_1.py

import pytest
from app_1 import get_yahoo_finance_data


@pytest.mark.parametrize(
    "ticker, data",
    [
        ("AAPL", "expected JSON"),  # Example input values
        (None, None),  # Invalid input to check error handling
    ],
)
def test_get_yahoo_finance_data(ticker, data):
    if ticker and isinstance(data, str):  # Check valid inputs
        result = get_yahoo_finance_data(ticker)
        assert result == data, "Test failed. Expected: {}, Got: {}".format(data, result)
    else:
        pytest.raises(AssertionError), lambda: get_yahoo_finance_data(ticker))


if __name__ == "__main__":
    pytest.main(["test_app_1.py"]))
```

This test file (`test_app_1.py`) includes unit tests using pytest for the `get_yahoo_finance_data()` function in the 'app_1.py' module.

The tests check valid and invalid inputs, and assert that the function returns the expected JSON data based on those inputs.