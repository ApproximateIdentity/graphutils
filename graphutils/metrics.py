def l1(dist1, dist2):
    '''
    Compute L1 distance between two distributions.
    
    Parameters
    ----------
    dist1, dist2 : dict of floats

    Returns
    -------
    d : float

    Notes
    -----
    This assumes that both distributions have all the same keys.
    '''
    d = 0.0
    for key in dist1.iterkeys():
        d += abs(dist1[key] - dist2[key])
    return d
