Here's the unit test file `test_app_1.py` created for the provided code:

```python
# app_1.py (Code being tested)

# test_app_1.py
import pytest

def test_data_collection():
    # Example data manipulation test case
    sample_stock_code = 'AAPL'
    stock_data = yf.download(sample_stock_code).info
    assert isinstance(stock_data, pd.DataFrame)
    
def test_market_data_display():
    # Example display test case for the collected data
    assert "Current Price" in stock_data.columns
    assert "Apple Inc." in stock_data["longName"]
    assert "Close" in stock_data.keys()

if __name__ == "__main__":
    pytest.main()
```

This Python test file, `test_app_1.py`, contains unit tests for the data collection and display parts of the 'app_1.py' code.

To run these tests, you would typically use a command like `pytest` in your terminal or IDE. The tests are assertions that verify the functionality of the code, ensuring it is working as expected.