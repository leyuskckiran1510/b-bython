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

SYMBOLS = ["{", "}", "(", ")", "[", "]"]


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


def do_open_braces(code: str, pointer: int):
    line = ""
    while code[pointer] != "{":
        line += code[pointer]
        pointer += 1
    return line + ":", pointer


def remove_tailing_close_braces(inner_chunk: str):
    code_len = len(inner_chunk)
    while code_len > 0:
        code_len -= 1
        if inner_chunk[code_len] != "}":
            continue
        else:
            break
    return inner_chunk[:code_len]


def do_inner_chunk(code: str, pointer: int):
    # back_up_pointer = pointer

    symbol_stack = [code[pointer]]
    pointer += 1
    inner_chunk = ""
    while symbol_stack:
        char = code[pointer]
        match char:
            case x if x == "}" and symbol_stack[-1] == "{":
                symbol_stack.pop()
            case x if x == "]" and symbol_stack[-1] == "[":
                symbol_stack.pop()
            case x if x == ")" and symbol_stack[-1] == "(":
                symbol_stack.pop()
            case x if x in SYMBOLS:
                symbol_stack.append(char)
            case _:
                ...
        inner_chunk += char
        pointer += 1
    inner_chunk = remove_tailing_close_braces(inner_chunk)

    inner_chunk = str(tokenizer(inner_chunk))
    return inner_chunk, pointer + 1
    # return "", back_up_pointer + 1


def handel_word(code: str, cur_word: str, pointer: int):
    if cur_word in INDENT_ABLES:
        until_open_braces, pointer = do_open_braces(code, pointer)
        code_line = cur_word + until_open_braces
        inner_chunk, pointer = do_inner_chunk(code, pointer)
        return code_line + inner_chunk, pointer
    else:
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
