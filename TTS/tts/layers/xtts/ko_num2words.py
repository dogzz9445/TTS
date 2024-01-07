# reference from https://github.com/esoyeon/KoreanTTS
# reference from https://github.com/savoirfairelinux/num2words


import re

_ordinal_il_re = re.compile(r"([0-9]+)(차)")
_ordinal_chut_re = re.compile(r"([0-9]+)(번째|째)")
_ordinal_han_re = re.compile(r"([0-9]+)(번|시|명|가지|살|마리|포기|송이|수|톨|통|점|개|벌|척|채|다발|그루|자루|줄|켤레|그릇|잔|마디|상자|사람|곡|병|판)")
_number_re = re.compile(r"[0-9]+")

def _remove_commas(m):
    text = m.group(0)
    if "," in text:
        text = text.replace(",", "")
    return text


def _remove_dots(m):
    text = m.group(0)
    if "." in text:
        text = text.replace(".", "")
    return text


class TextNorm:
    def __init__(self):
        self.setup()
        
    def setup(self):
        self.negword = "마이너스 "
        self.pointword = "점"

        self.high_numwords = [
            '무량대수',
            '불가사의',
            '나유타',
            '아승기',
            '항하사',
            '극',
            '재',
            '정',
            '간',
            '구',
            '양',
            '자',
            '해',
            '경',
            '조',
            '억',
            '만']
        self.mid_numwords = [(1000, "천"), (100, "백")]
        self.low_numwords = ["십", "구", "팔", "칠", "육", "오", "사", "삼", "이",
                             "일", "영"]
        self.ords = {"일": "한",
                     "이": "두",
                     "삼": "세",
                     "사": "네",
                     "오": "다섯",
                     "육": "여섯",
                     "칠": "일곱",
                     "팔": "여덟",
                     "구": "아홉",
                     "십": "열",
                     "이십": "스물",
                     "삼십": "서른",
                     "사십": "마흔",
                     "오십": "쉰",
                     "육십": "예순",
                     "칠십": "일흔",
                     "팔십": "여든",
                     "구십": "아흔"}
    
    def to_ordinal(self, value):
        self.verify_ordinal(value)
        outwords = self.to_cardinal(value).split(" ")
        lastwords = outwords[-1].split("백")
        if "십" in lastwords[-1]:
            ten_one = lastwords[-1].split("십")
            ten_one[0] = self.ords[ten_one[0] + "십"]
            ten_one[1] = self.ords.get(ten_one[1], ten_one[1])
            ten_one[0] = ten_one[0].replace("스무", "스물")
            lastwords[-1] = ''.join(ten_one)
        else:
            lastwords[-1] = self.ords.get(lastwords[-1], lastwords[-1])
        if (lastwords[-1] == '' and len(lastwords) > 1):
            outwords[-1] = '백'.join(lastwords)
        else:
            outwords[-1] = "백 ".join(lastwords)
        return " ".join(outwords) + " 번째"

    def _expand_decimal_point(m, lang="en"):
        amount = m.group(1).replace(",", ".")
        return num2words(float(amount), lang=lang if lang != "cs" else "cz")

    def __call__(self, text: str) -> str:
        text = re.sub(_dot_number_re, _remove_dots, text)
        text = re.sub(_currency_re["GBP"], lambda m: _expand_currency(m, lang, "GBP"), text)
        text = re.sub(_currency_re["USD"], lambda m: _expand_currency(m, lang, "USD"), text)
        text = re.sub(_currency_re["EUR"], lambda m: _expand_currency(m, lang, "EUR"), text)
        text = re.sub(_ordinal_re, lambda m: _expand_ordinal(m, lang), text)
        text = re.sub(_number_re, lambda m: _expand_number(m, lang), text)
        
    
    
if __name__ == "__main__":
    text_norm = TextNorm()
    print(text_norm("1시 2명 3가지 4살 5마리 6포기 7송이 8수 9톨 10통 11점 12개 13벌 14척 15채 16다발 17그루 18자루 19줄 20켤레 21그릇 22잔 23마디 24상자 25사람 26곡 27병 28판"))