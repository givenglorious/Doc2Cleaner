
from pathlib import Path
import pandas as pd

from .loader import DocumentLoader
from .columns import ColumnCleaner
from .cleaner import TextCleaner


class CleaningPipeline:

    def __init__(self, path: str):
        self.source_path = path
        self.df: pd.DataFrame = DocumentLoader(path).load()

    def preview_columns(self) -> None:
        print("Available columns:", self.df.columns.tolist())
        print("Text candidates  :", ColumnCleaner(self.df).suggest_text_columns())

    def run(
        self,
        text_columns: list[str],
        drop_columns: list[str] | None = None,
        output_path: str = "cleaned.xlsx",
        overwrite_original: bool = False,
        save: bool = True,
    ) -> pd.DataFrame:
        
        column_cleaner = ColumnCleaner(self.df)

        if drop_columns:
            self.df = column_cleaner.drop_columns(drop_columns)

        for col in text_columns:
            if col not in self.df.columns:
                print(f"[Pipeline] Column '{col}' not found, skipping.")
                continue

            target_col = col if overwrite_original else f"{col}_cleaned"
            self.df[target_col] = self.df[col].apply(TextCleaner.clean)

        if save:
            self._save(output_path)

        return self.df

    def _save(self, output_path: str) -> None:
        out = Path(output_path)
        if out.suffix.lower() == ".csv":
            self.df.to_csv(out, index=False)
        else:
            self.df.to_excel(out, index=False)
        print(f"[Pipeline] Done. Saved to {out}")
