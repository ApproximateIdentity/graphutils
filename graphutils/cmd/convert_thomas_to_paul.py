from sys import stdin, stdout

from graphutils.parsing import parseline

if __name__ == '__main__':
    for line in stdin:
        id, neighbors = parseline(line)
        try:
            # Note the space before final newline!
            stdout.write(id + '\n' + ' '.join(neighbors) + ' \n')
        except OSError:
            break
        
    # To match final newline in file.
    try:
        stdout.write('\n')
    except OSError:
        pass
