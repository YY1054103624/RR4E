"""
split and interactively page a string or file of text
"""


def more(text, numlines=15):
    """
    page multiline string to stdout
    """
    lines = text.splitlines()               # like split('\n') but no '' at end
    while lines:
        chunk = lines[:numlines]
        lines = lines[numlines:]
        for line in chunk: print(line)
        if lines and input('More?') not in ['y', 'Y']: break


if __name__ == '__main__':                  # when run, not when imported
    import sys
    if len(sys.argv) == 1:                  # page stdin if no cmd args
        more(sys.stdin.read())
    else:
        more(open(sys.argv[1]).read())
