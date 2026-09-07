import re
import pandas as pd
class TextCleaner:
    URL_PATTERN = re.compile(r"http[s]?://\S+")
    PIC_TWITTER_PATTERN = re.compile(r"pic\.twitter\.com\S+")
    MENTION_PATTERN = re.compile(r"@\w+")
    HASHTAG_PATTERN = re.compile(r"#\w+")
    NON_ASCII_PATTERN = re.compile(r"[^\x00-\x7F]+")
    SYMBOL_PATTERN = re.compile(r"[!$%^&*@#()_+|~=`{}\[\]%\-:\";'<>?,./]")
    NUMBER_PATTERN = re.compile(r"[0-9]+")
    REPEATED_CHAR_PATTERN = re.compile(r"(.)\1{2,}")
    NEWLINE_PATTERN = re.compile(r"\n")
    MULTISPACE_PATTERN = re.compile(r" +")

    @classmethod
    def clean(cls, text) -> str:
        if pd.isna(text):
            return ""

        cleaned = str(text)
        cleaned = cls.URL_PATTERN.sub(" ", cleaned)
        cleaned = cls.PIC_TWITTER_PATTERN.sub(" ", cleaned)
        cleaned = cls.MENTION_PATTERN.sub(" ", cleaned)
        cleaned = cls.HASHTAG_PATTERN.sub(" ", cleaned)
        cleaned = cls.NON_ASCII_PATTERN.sub(" ", cleaned)  # non-ASCII & emoji
        cleaned = cls.SYMBOL_PATTERN.sub(" ", cleaned)
        cleaned = cls.NUMBER_PATTERN.sub("", cleaned)
        cleaned = cls.REPEATED_CHAR_PATTERN.sub(r"\1", cleaned)  # ayoooo -> ayo
        cleaned = cls.NEWLINE_PATTERN.sub(" ", cleaned)
        cleaned = cls.MULTISPACE_PATTERN.sub(" ", cleaned)

        return cleaned.strip().lower()
