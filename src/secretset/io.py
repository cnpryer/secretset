import pandas as pd  # type: ignore


def read_file(filename: str) -> pd.DataFrame:
    """Read file from current directory using filename.
    Args:
        filename (str): Filename. Only reads xlsx, xls, and csv.
    Returns:
        pd.DataFrame: Pandas DataFrame
    """
    if filename.lower().endswith(".xls") or filename.lower().endswith(".xlsx"):
        return pd.read_excel(filename)

    if filename.lower().endswith(".csv"):
        return pd.read_csv(filename)

    raise Exception("File must be .xls, .xlsx, .csv.")
