BLOCK_SIZE = 1024


def tail_log(f, lines=20):
    """
        Author: S.Lott
        Source: http://stackoverflow.com/questions/136168/get-last-n-lines-of-a-file-with-python-similar-to-tail
    """

    total_lines_wanted = lines

    f.seek(0, 2)
    block_end_byte = f.tell()
    lines_to_go = total_lines_wanted
    block_number = -1
    blocks = []  # blocks of size BLOCK_SIZE, in reverse order starting
    # from the end of the file
    while lines_to_go > 0 and block_end_byte > 0:
        if block_end_byte - BLOCK_SIZE > 0:
            # read the last block we haven't yet read
            f.seek(block_number * BLOCK_SIZE, 2)
            blocks.append(f.read(BLOCK_SIZE))
        else:
            # file too small, start from begining
            f.seek(0, 0)
            # only read what was not read
            blocks.append(f.read(block_end_byte))
        lines_found = blocks[-1].count(b'\n')
        lines_to_go -= lines_found
        block_end_byte -= BLOCK_SIZE
        block_number -= 1
    all_read_text = b''.join(reversed(blocks))
    return all_read_text.splitlines()[-total_lines_wanted:]