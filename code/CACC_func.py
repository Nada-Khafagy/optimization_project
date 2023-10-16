def CACC(k0, k1, k2, al, vl, vf, s, sd):

    af = k0*al + k1 * (vl-vf) + k2 * (s-sd)
    
    return af