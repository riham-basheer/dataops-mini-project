import os
import pandas as pd

def clean_country_name(country:str) -> str:
    """
    Convert country values into a standard format.
    Args:
        country (str): The country name to clean.
    Example:
        " egypt " → "EGYPT"
        " uAe " → "UAE"
    """
    if pd.isna(country) or not isinstance(country, str): #it exists and is string
        return ""
    return country.strip().upper()


def is_valid_transaction(row: dict) -> bool:
    """
    Check if a transaction is valid based on the following criteria:
        - The 'transaction_id' field must not be null.
        - The 'user_id' field must not be null.
        - The 'transaction_date' field must not be null.
        - For a purchase: The 'amount' field must be a positive number or zero.
        - For a refund: The 'amount' field must be a negative number.
    If so, the record is considered valid; otherwise, it is flagged and written to a separate file for further review.
    Args:
        row (dict): A dictionary representing a transaction.
    """
    if pd.isna(row.get('transaction_id')) or pd.isna(row.get('user_id')) or pd.isna(row.get('transaction_date')):
        return False

    try:
        amount = float(row.get('amount'))
    except (TypeError, ValueError):
        return False
    
    transaction_type = str(row.get('transaction_type')).strip().lower()

    if transaction_type == 'purchase' and (pd.isna(amount) or amount <= 0):
        return False
    elif transaction_type == 'refund' and (pd.isna(amount) or amount >= 0):
        return False
    
    return True

def transform_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Transform the input DataFrame by cleaning country names and filtering valid transactions.
    Args:
        df (pd.DataFrame): The input DataFrame containing transaction data.
    """
    if df.empty:
        return df, pd.DataFrame()

    df_copy = df.copy() 

    # Clean country names
    df_copy['country'] = df_copy['country'].apply(clean_country_name)

    # Filter valid transactions
    valid_transactions = df_copy[df_copy.apply(is_valid_transaction, axis=1)]

    # Filter invalid transactions
    invalid_transactions = df_copy[~df_copy.apply(is_valid_transaction, axis=1)]

    return valid_transactions, invalid_transactions

def aggregate_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate the transaction data by country. 
    Args:
        df (pd.DataFrame): The input DataFrame containing valid transaction data.
    Example:
        country, transaction_date, number_of_transactions, number_of_users, total_amount
        EGYPT | 2026-09-01 | 20 | 15 | 4500
        UAE   | 2026-09-01 | 10 | 8  | 2700 
"""  

    if df.empty:
        return pd.DataFrame(columns=['country', 'transaction_date', 'number_of_transactions', 'number_of_users', 'total_amount'])

    # Ensure transaction_date is in datetime format
    df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')

    # Group by country and transaction_date, then aggregate
    aggregated_df = df.groupby(['country', 'transaction_date']).agg(
        number_of_transactions=('transaction_id', 'count'),
        number_of_users=('user_id', pd.Series.nunique),
        total_amount=('amount', 'sum')
    ).reset_index()

    return aggregated_df

def run_pipeline(input_file: str = "data/transactions.csv", output_dir: str = "output") -> None:
    """
    Run the data transformation and aggregation pipeline.
    Args:
        input_file (str): The path to the input CSV file containing transaction data.
        output_dir (str): The directory where the output files will be saved.
    """
    # Read the input CSV file
    df = pd.read_csv(input_file)
    print(f"Read {len(df)} records from {input_file}")

    # Transform the data
    valid_transactions, invalid_transactions = transform_data(df)
    print(f"Found {len(valid_transactions)} valid transactions and {len(invalid_transactions)} invalid transactions.")
    
    # Aggregate the valid transactions
    aggregated_data = aggregate_data(valid_transactions)

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save the results to CSV files
    valid_transactions.to_csv(os.path.join(output_dir, 'valid_transactions.csv'), index=False)
    invalid_transactions.to_csv(os.path.join(output_dir, 'invalid_transactions.csv'), index=False)
    aggregated_data.to_csv(os.path.join(output_dir, 'aggregated_transactions.csv'), index=False)
    print(f"Results saved to {output_dir}")

    if not invalid_transactions.empty:
        print(f"Invalid transactions have been saved to {os.path.join(output_dir, 'invalid_transactions.csv')}")
        print ("Sample of invalid transactions:")
        print(invalid_transactions.head())


if __name__ == "__main__":
    run_pipeline()