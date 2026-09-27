import pandas as pd
import pytest
from src.transform import clean_country_name, is_valid_transaction, aggregate_data

# Test 1: Test the clean_country_name function
def test_clean_country_name():
    assert clean_country_name(" egypt ") == "EGYPT"
    assert clean_country_name(" uAe ") == "UAE"
    assert clean_country_name("  ") == ""
    assert clean_country_name(None) == ""
    assert clean_country_name(123) == ""

# Test 2: Null user_id
def test_null_user_id():
    row = {
        'transaction_id': '123',
        'user_id': None,
        'transaction_date': '2025-01-01',
        'amount': 100,
        'transaction_type': 'purchase'
    }
    assert not is_valid_transaction(row)

# Test 3: Negative amount for purchase
def test_negative_amount_purchase():
    row = {
        'transaction_id': '123',
        'user_id': '456',
        'transaction_date': '2025-01-01',
        'amount': -100,
        'transaction_type': 'purchase'
    }
    assert not is_valid_transaction(row)

# Test 4: Positive amount for refund
def test_positive_amount_refund():
    row = {
        'transaction_id': '123',
        'user_id': '456',
        'transaction_date': '2025-01-01',
        'amount': 100,
        'transaction_type': 'refund'
    }
    assert not is_valid_transaction(row)

# Test 5: aggregate_data produces correct total amounts for valid transactions
def test_aggregate_data():
    sample_df = pd.DataFrame(
        [
            {
                "transaction_id": "1",
                "user_id": "001",
                "country": "EGYPT",
                "transaction_date": "2026-09-01",
                "transaction_type": "purchase",
                "amount": 200.5,
            },
            {
                "transaction_id": "2",
                "user_id": "002",
                "country": "EGYPT",
                "transaction_date": "2026-09-01",
                "transaction_type": "purchase",
                "amount": 300.0,
            },
            {
                "transaction_id": "3",
                "user_id": "001",
                "country": "EGYPT",
                "transaction_date": "2026-09-01",
                "transaction_type": "refund",
                "amount": -50.0,
            },
        ]
    )

    summary = aggregate_data(sample_df)

    assert len(summary) == 1
    assert summary.loc[0, "country"] == "EGYPT"
    assert summary.loc[0, "number_of_transactions"] == 3
    assert summary.loc[0, "number_of_users"] == 2
    assert summary.loc[0, "total_amount"] == 450.5
