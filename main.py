import regex as re
from load import DocumentLoader

class TextProcessor:
    def __init__(self, data = DocumentLoader("data.xlsx")):
        self.data = data
        
    def removing_anomalies(self) -> str:

        cleaned_text = self.data
        #1: Ascii
        cleaned_text = re.sub(r'[^\x00-\x7F]+', ' ', cleaned_text)
        #2: Link
        cleaned_text = re.sub(r'http[s]?\:\/\/.[a-zA-Z0-9\.\//\_?=%&#\-+!]+', ' ', cleaned_text)
        cleaned_text = re.sub(r'pic.twitter.com?.[a-zA-Z0-9\.\//\_?=%&#\-+!]+', ' ', cleaned_text)
        #3: Mention
        cleaned_text = re.sub(r'\@([\w]+)', ' ', cleaned_text)
        #4: Tagar
        cleaned_text = re.sub(r'\#([\w]+)', ' ', cleaned_text)
        #5: Simbol
        cleaned_text = re.sub(r'[!$%^&*@#()_+|~=``{}\[\]%\-:";\'<>?,./]', ' ', cleaned_text)
        #6: angka
        cleaned_text = re.sub(r'[0-9]+', '', cleaned_text)
        #7: karakter berulang (example: ayoooo)
        cleaned_text = re.sub(r'([a-zA-Z])\1\1', r'\1', cleaned_text)
        #8: Dobble Space >>
        cleaned_text = re.sub(r' +', ' ', cleaned_text)
        #9: Space Awal Dan Akhir Kalimat
        cleaned_text = re.sub(r'^[ ]|[ ]$', '', cleaned_text)
        #10: Hapus /n jadi space
        cleaned_text = re.sub(r'\n', ' ', cleaned_text)
        #11: Hapus emoji
        cleaned_text = re.sub(r'[^\x00-\x7F]+', ' ', cleaned_text)

        cleaned_text = cleaned_text.lower()

        return cleaned_text
# #TDL 
# PYDANTIC'
# CONVERT TO LLM 
