import pandas as pd


class ColumnCleaner:

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def suggest_text_columns(self) -> list[str]:
        return self.df.select_dtypes(include="object").columns.tolist()

    def drop_columns(self, columns: list[str]) -> pd.DataFrame:
        existing = [c for c in columns if c in self.df.columns]
        missing = [c for c in columns if c not in self.df.columns]
        if missing:
            print(f"[ColumnCleaner] column not found, skipping: {missing}")
        return self.df.drop(columns=existing)
