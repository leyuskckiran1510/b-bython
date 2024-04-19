from util import load_sample

INDENT_ABLES = [
    "def",
    "for",
    "with",
    "if",
    "else",
    "elif",
    "while",
    "try",
    "except",
    "finally",
    "class",
    "match",
    "case",
]


def do_fstring(code: str, index: int):
    return index


def handel_quote(code: str, index: int):
    code_len = len(code)
    next_three = code[index : index + 3]
    quote = code[index]
    if next_three in ['"""', "'''"]:
        count = 0
        while count < 3 and index < code_len:
            char = code[index]
            if char == quote:
                count += 1
            index += 1
    else:
        is_fstring = index > 0 and code[index - 1] == "f"
        if is_fstring:
            index = do_fstring(code, index)
        else:
            index += 1
            while code[index] != quote:
                index += 1

            index += 1
    return index


def handel_word(code: str, cur_word: str, pointer: int):
    return cur_word + code[pointer], pointer + 1


def tokenizer(raw_code: str):
    new_code: str = ""
    cur_word = ""
    pointer = 0
    code_len = len(raw_code)
    while pointer < code_len:
        char = raw_code[pointer]
        match char:
            case x if x in ['"', "'"]:
                n_pointer = handel_quote(raw_code, pointer)
                new_code += raw_code[pointer:n_pointer]
                pointer = n_pointer
            case x if x in [" ", "\n"]:
                new_chunk, pointer = handel_word(raw_code, cur_word, pointer)
                new_code += new_chunk
                cur_word = ""
            case _:
                cur_word += char
                pointer += 1
    return new_code + cur_word


if __name__ == "__main__":
    for file, sample in load_sample(1):
        print(f"Original FIle {file}..")
        print("Tokonized into... ")
        print(tokenizer(sample))
