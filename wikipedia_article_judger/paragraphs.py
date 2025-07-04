stop_words = [
    'a', 'an', 'and', 'are', 'as', 'at', 'being', 'but', 'by', 'can', 'for', 
    'has', 'in', 'is', 'it', 'its', 'just', 'like', 'not', 'of', 'on', 
    'our', 'the', 'this', 'thus', 'to', 'while', 'with'
]

def para_empty(input_para:str)-> bool :
    if len(input_para) == 0:
        return True
    return False

def validate_para(input_para:str, low:int = 10, high:int = 600) -> str:
  para = input_para.split()
  if len(para) > high or len(para) < low:
    return True
  return False

def clean(input_para: str, stop_words: list[str] = stop_words) -> str:
  words = input_para.split()  
  filtered_words = [word for word in words if word.lower() not in stop_words]
  return ' '.join(filtered_words)
