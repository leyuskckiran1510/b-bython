from util import load_sample
from util import print_code  # type:ignore

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

INDENT_WITH = "    "

# Normal Symbol stack
SYMBOLS = ["{", "}", "(", ")", "[", "]"]
# Symbol Stack for f-strings
SYMBOLS_F = ["{", "}", "(", ")", "[", "]", '"', "'"]


def do_fstring(code: str, index: int):
    stack_symbol = [code[index]]
    index += 1
    while index < len(code) and stack_symbol:
        char = code[index]
        if char in SYMBOLS_F:
            symbol_stack_op(stack_symbol, char, SYMBOLS_F)
        index += 1
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


def symbol_stack_op(
    sym_stack: list[str],
    cur_sym: str,
    symbols: list[str] = SYMBOLS,
):
    match cur_sym:
        # remove the epsilon from the stack
        case x if x == "{" and sym_stack[-1] == "e":
            sym_stack.pop()
        case x if x == "}" and sym_stack[-1] == "{":
            sym_stack.pop()
        case x if x == "]" and sym_stack[-1] == "[":
            sym_stack.pop()
        case x if x == ")" and sym_stack[-1] == "(":
            sym_stack.pop()
        case x if x == '"' and sym_stack[-1] == '"':
            sym_stack.pop()
        case x if x == "'" and sym_stack[-1] == "'":
            sym_stack.pop()
        case x if x in symbols:
            sym_stack.append(cur_sym)
        case _:
            ...


def do_open_braces(code: str, pointer: int):
    # Accept by empty Stack
    line = ""
    # insert epsilon  as star symbol
    symbol_stack: list[str] = ["e"]
    while symbol_stack and len(code) > pointer:
        char = code[pointer]
        match char:
            case x if x in SYMBOLS:
                symbol_stack_op(symbol_stack, char)
            case _:
                ...
        if char != "\n" and symbol_stack:
            line += char
        pointer += 1
    return line + ":\n", pointer - 1


def remove_tailing_close_braces(inner_chunk: str):
    code_len = len(inner_chunk)
    while code_len > 0:
        code_len -= 1
        if inner_chunk[code_len] != "}":
            continue
        else:
            break
    return inner_chunk[:code_len]


def indent_it(code_block: str, level: int):
    new_code = INDENT_WITH * level
    pointer = 0
    while pointer < len(code_block):
        char = code_block[pointer]
        if char == "\n":
            char = "\n" + INDENT_WITH * level
        new_code += char
        pointer += 1
    return new_code


def do_inner_chunk(code: str, pointer: int, level: int = 0):
    symbol_stack = [code[pointer]]
    pointer += 1
    inner_chunk: str = ""
    while symbol_stack and len(code) > pointer:
        char = code[pointer]
        match char:
            case x if x in SYMBOLS:
                symbol_stack_op(symbol_stack, char)
            case _:
                ...
        if char == ";" and symbol_stack == ["{"]:
            while char == ";":
                char = code[pointer]
                pointer += 1
            pointer -= 2
            char = "\n"
        inner_chunk += char
        pointer += 1
    inner_chunk = remove_tailing_close_braces(inner_chunk)
    inner_chunk = tokenizer(inner_chunk, level=level)
    inner_chunk = indent_it(inner_chunk, level)
    # print_code(inner_chunk, level)
    return inner_chunk, pointer


def handel_word(code: str, cur_word: str, pointer: int, level: int = 0):
    if cur_word in INDENT_ABLES:
        until_open_braces, pointer = do_open_braces(code, pointer)
        code_line = cur_word + until_open_braces
        inner_chunk, pointer = do_inner_chunk(code, pointer, level)
        return code_line + inner_chunk, pointer
    else:
        return cur_word + code[pointer], pointer + 1


def tokenizer(raw_code: str, level: int = 0):
    new_code: str = ""
    cur_word = ""
    pointer = 0
    code_len = len(raw_code)
    while pointer < code_len:
        char = raw_code[pointer]
        match char:
            case x if x in ['"', "'"]:
                n_pointer = handel_quote(raw_code, pointer)
                cur_word += raw_code[pointer:n_pointer]
                pointer = n_pointer
            case x if x in [" ", "\n"]:
                new_chunk, pointer = handel_word(
                    raw_code, cur_word, pointer, level + 1
                )
                new_code += new_chunk
                cur_word = ""
            case _:
                cur_word += char
                pointer += 1
        # print_code(new_code, level)
    return new_code + cur_word


if __name__ == "__main__":
    for file, sample in load_sample(3):
        print(f"Original FIle {file}..")
        print("Tokonized into... ")
        python_code = tokenizer(sample, 0)
        # with open("output.py", "w") as fp:
        #     fp.write(python_code)
        # exec(python_code)
        print(python_code)
