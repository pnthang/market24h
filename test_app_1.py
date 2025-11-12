```python
# app_1.py

import streamlit as st

def calculate_volume(stock_code):
    try:
        stock_info = Ticker(stock_code).info
        volume = stock_info['volume']
        return volume
    except Exception as e:
        return f"Error: {e}"


def main():
    stock_input = st.text_input("Enter stock code or name", value="AAPL")
    volume_button = st.button("Calculate Volume")

    if volume_button:
        selected_stock_code = stock_input.text
        try:
            volume = calculate_volume(selected_stock_code)
            st.success(f"Volume for {selected_stock_code}: {volume}")
        except Exception as e:
            st.error(f"Error: {e}") 

if __name__ == "__main__":
    main()
```

Now, let's write the unit tests in 'test_app_1.py' using pytest:

```python
# test_app_1.py

import pytest
from app_1 import calculate_volume


def test_calculate_volume():
    stock_code = "AAPL"
    expected_volume = 203590658

    result = calculate_volume(stock_code)
    assert result == expected_volume, "Volume calculation failed"

@pytest.mark.parametrize("stock_code", ["AAPL", "GOOGL", "MSFT"]))
def test_calculate_volume_variants(stock_code):
    volume_result = calculate_volume(stock_code)
    
    if stock_code in {"AAPL", "GOOGL"}:  # Known stocks
        expected_volume = volume_result * 1000  # Convert to millions for comparison
        assert abs(expected_volume - volume_result) < 1, f"Volume calculation differs by more than 1 milliliter"

```

Now you have a Python test file named `test_app_1.py` containing unit tests for the functions in `app_1.py`.