def parseline(line):
    '''
    Parse one line of a data file.
    
    Parameters
    ----------
    line : string
    '''
    id, neighbors = line.split('->')
    neighbors = neighbors.strip().split(',')
    return id, neighbors
