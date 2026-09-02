import pandas as pd 

class DocumentLoader:
    def __init__(self,data : str):
        self.data = data.lower()

    def csv(self) -> str:
        if self.data.endswith('xlsx'):
            data = pd.read_excel(self.data)
            print(f'Load a {data}')
        else:
            return "You're data type have to be xlsx"

if __name__ == "__main__":
    #Testing the DocumentLoader class
    loader = DocumentLoader("data.xlsx")
    loader.csv()

