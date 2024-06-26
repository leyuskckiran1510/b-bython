import re
import sys
import traceback
from uuid import uuid4

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

MAGIC_WORDS = {
    r"else[\s]+if": "elif",
}

INDENT_WITH = "    "

# Normal Symbol stack
SYMBOLS = ["{", "}", "(", ")", "[", "]"]
# Symbol Stack for f-strings
SYMBOLS_F = ["{", "}", "(", ")", "[", "]", '"', "'"]


WHITESPACES = [" ", "\n", "\t", "\v", "\f"]


def do_fstring(code: str, index: int) -> int:
    """
    Resolve f-strings
    This function is useless,
    for the current usecase, but it is usefull
    if we want to convert bbpy to something other than python
    """
    stack_symbol = [code[index]]
    index += 1
    while index < len(code) and stack_symbol:
        char = code[index]
        if char in SYMBOLS_F:
            symbol_stack_op(stack_symbol, char, SYMBOLS_F)
        index += 1
    return index


def handel_quote(code: str, index: int) -> int:
    """
    It handels the thirple and single quotes,
    and f-strings
    """
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
            while index < code_len and code[index] != quote:
                index += 1
            index += 1
    return index


def symbol_stack_op(
    sym_stack: list[str],
    cur_sym: str,
    symbols: list[str] = SYMBOLS,
):
    """
    Does stack push and pop operation
    """
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


def do_open_braces(code: str, pointer: int) -> tuple[str, int]:
    """
    search for  open brace '{', and replace it with ':\n';
    only if their are no other symbol in the stack as
    we can have a dic in a function defination it self
    """
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


def remove_tailing_closing_brace(inner_chunk: str) -> str:
    code_len = len(inner_chunk)
    while code_len > 0:
        code_len -= 1
        if inner_chunk[code_len] != "}":
            continue
        else:
            break
    return inner_chunk[:code_len] + "\n"


def count_space(line: str):
    count = 0
    while count < len(line) and line[count] in WHITESPACES:
        count += 1
    return count


def indent_it(code_block: str, level: int) -> str:
    pointer = 0
    # remove leading newline
    # when the bbpy code is already formatted and is not minimized
    # it will cause multiple new-line in code block begening
    # so remove the pre-formmated new-line if exsists
    # then format ourself
    if code_block[pointer] == "\n":
        pointer += 1

    line_droped = False
    new_code = "\n" + INDENT_WITH * level
    while pointer < len(code_block):
        char = code_block[pointer]
        if char == "\n":
            line_droped = True
        elif line_droped:
            char = INDENT_WITH * level + char
            line_droped = False
        new_code += char
        pointer += 1
    return new_code


def handle_solo_code_block(
    raw_code: str, pointer: int, level: int = 0
) -> tuple[str, int]:

    code, pointer = do_inner_chunk(raw_code, pointer, level + 2)
    uid = str(uuid4()).replace("-", "_")
    template = f"def anonm_{uid}():"
    call_it = f"anonm_{uid}()\n"
    final_code = template + code + call_it
    return final_code, pointer


def do_inner_chunk(code: str, pointer: int, level: int = 0) -> tuple[str, int]:
    """
    it extracts out the code block ie:- code inside outermost '{' and '}',
    then treats the code block as a new code and runs complier on it
    then indents the tokenized output
    """
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
        if char == ";" and code[pointer + 1] != "\n" and symbol_stack == ["{"]:
            while char in WHITESPACES + [";"]:
                char = code[pointer]
                pointer += 1
            pointer -= 2
            char = "\n"
        inner_chunk += char
        pointer += 1

    if not symbol_stack and pointer < len(code):
        # consume tailing white spaces also
        while pointer < len(code) and code[pointer] in WHITESPACES:
            pointer += 1

    inner_chunk = remove_tailing_closing_brace(inner_chunk)
    inner_chunk = complier(inner_chunk, level=level)
    inner_chunk = indent_it(inner_chunk, level)
    return inner_chunk, pointer


def handel_word(
    code: str, cur_word: str, pointer: int, level: int = 0
) -> tuple[str, int]:
    """
    It handels the tokens, ie:- space sperated words
    """
    if cur_word in INDENT_ABLES:
        until_open_braces, pointer = do_open_braces(code, pointer)
        code_line = cur_word + until_open_braces
        inner_chunk, pointer = do_inner_chunk(code, pointer, level)
        return code_line + inner_chunk, pointer
    else:
        return cur_word + code[pointer], pointer + 1


def complier(raw_code: str, level: int = 0) -> str:
    new_code: str = ""
    cur_word = ""
    pointer = 0
    code_len = len(raw_code)
    assigment = False
    spaces = False
    while pointer < code_len:
        char = raw_code[pointer]
        match char:
            case x if x in ['"', "'"]:
                n_pointer = handel_quote(raw_code, pointer)
                cur_word += raw_code[pointer:n_pointer]
                pointer = n_pointer
            case x if x in [" ", "\n"]:
                # we have handled the word
                # but still their is bunch of spaces
                # then ignore those spaces
                if spaces and cur_word == "":
                    pointer += 1
                    continue

                if x == "\n":
                    assigment = False
                if x == " ":
                    spaces = True

                new_chunk, pointer = handel_word(
                    raw_code, cur_word, pointer, level + 1
                )
                new_code += new_chunk
                cur_word = ""
            case x if x in ["{"] and not assigment:
                if cur_word in INDENT_ABLES:
                    new_chunk, pointer = handel_word(
                        raw_code, cur_word, pointer, level + 1
                    )
                    new_code += new_chunk
                    cur_word = ""
                else:
                    new_chunk, pointer = handle_solo_code_block(
                        raw_code, pointer, level + 1
                    )
                    cur_word += new_chunk
            case _:
                cur_word += char
                spaces = False
                if char == "=":
                    assigment = True
                pointer += 1
    return new_code + cur_word


def replace_magic_words(code: str):
    for _from, to in MAGIC_WORDS.items():
        code = re.sub(_from, to, code)
    return code


def work_on_sampe(sample_index: int):
    for file, sample in load_sample(sample_index):
        print(f"Original FIle {file}..")
        print("Tokonized into... ")
        sample = "\n".join([i.strip() for i in sample.split("\n")])
        python_code = complier(sample)
        python_code = replace_magic_words(python_code)
        with open("output.py", "w") as fp:
            fp.write(python_code)
        try:
            exec(python_code)
        except BaseException as _:
            traceback.print_exc()
            print(f"[ERROR] in {file=}", "\n")


def test_all(upto: int = 5):
    for sample_index in range(1, upto + 1):
        work_on_sampe(sample_index)


if __name__ == "__main__":
    sample_index = 7
    if len(sys.argv) > 1 and sys.argv[1].isnumeric():
        sample_index = int(sys.argv[1])
        work_on_sampe(sample_index)
    elif len(sys.argv) > 1 and sys.argv[1] == "test":
        test_all(sample_index)
    else:
        work_on_sampe(sample_index)
