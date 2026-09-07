from pathlib import Path
import pandas as pd


class DocumentLoader:

    SUPPORTED_EXTENSIONS = {".xlsx", ".xls", ".csv"}

    def __init__(self, path: str):
        self.path = Path(path)

    def load(self) -> pd.DataFrame:  
        ext = self.path.suffix.lower()

        if ext not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Format '{ext}' its not supported. "
                f"Gunakan salah satu dari: {', '.join(self.SUPPORTED_EXTENSIONS)}"
            )

        if not self.path.exists():
            raise FileNotFoundError(f"File not found: {self.path}")

        if ext == ".csv":
            return pd.read_csv(self.path)
        return pd.read_excel(self.path)
