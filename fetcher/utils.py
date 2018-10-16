def normalize_filename(filename):
    f_name = filename.split('/')[-1]
    f_name = f_name.split('?')[0]
    return f_name

def normalize_name(s):
    if s is None:
        return ''
        
    new_s = ''
    for c in s:
        if c in '- \t\n':
            new_s += '_'
        else:
            new_s += c
    return new_s
