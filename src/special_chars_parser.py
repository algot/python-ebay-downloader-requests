def replace_substring(string_to_process, chars_to_replace):
    for c in chars_to_replace:
        string_to_process = string_to_process.replace(c[0], c[1])
    return string_to_process


def remove_chars(string_to_process, list_of_chars_to_delete):
    for c in list_of_chars_to_delete:
        string_to_process = string_to_process.replace(c, '')
    return string_to_process


chars_quoted = (('_amp;', '&'), ('_#034;', "'"), ('_wbr__', ''), ('_#039;', "'"))

chars_alpha = (
    ('Ã', 'A'), ('Á', 'A'), ('Ä', 'A'),
    ('à', 'a'), ('à', 'a'), ('ä', 'a'), ('ӓ', 'a'), ('â', 'a'), ('á', 'a'), ('å', 'aa'), ('ą', 'a'),
    ('ć', 'c'), ('ç', 'c'), ('ç', 'c'), ('č', 'c'),
    ('é', 'e'), ('é', 'e'), ('è', 'e'), ('è', 'e'), ('ê', 'e'), ('ë', 'e'),
    ('í', 'i'), ('ï', 'i'), ('î', 'i'),
    ('ł', 'l'),
    ('Ñ', 'N'),
    ('Ö', 'O'), ('ô', 'o'), ('ö', 'o'), ('ó', 'o'), ('œ', 'oe'),
    ('ř', 'r'),
    ('Š', 'S'), ('ß', 'ss'), ('Ś', 'S'),
    ('ť', 't'),
    ('Ü', 'U'), ('ü', 'u'), ('û', 'u'), ('ù', 'u'),
    ('ý', 'y'),
    ('ż', 'z'), ('ź', 'z'))

chars_special = (
    ('´', '\''), ('̂', '\''), ('’', '\''), ('̈', '\''), ('″', '\''),
    ('-️', '-'), ('_', '-'), ('-', '-'), ('-️', '-'), ('-️', '-'), ('-️', '-'),
    ('¤', '-'), ('¶', '-'), ('º', '_'),
    ('×', 'x'), ('÷', '-'), ('³', '3'),
    ('£', 'pound'))

chars_emojii = (
    ('♥', '1'), ('☆', '1'), ('❚', '1'), ('★', '1'),
    ('🌈', '-'), ('📷', '-'), ('📸', '-'), ('💖', '-'),
    ('❤', '-'), ('♫', '-'), ('✅', '-'), ('◈', '-'), ('☺', '-'), ('♦', '-'))

chars_to_delete = 'ђўР“™ќ®Їљ§њћџ•”¬¦Ґ†Ґ«›—©\'Ё★'


def parse_string(input_string):
    result = replace_substring(input_string, chars_quoted)
    result = replace_substring(result, chars_alpha)
    result = replace_substring(result, chars_special)
    result = replace_substring(result, chars_emojii)
    result = remove_chars(result, chars_to_delete)

    return result
