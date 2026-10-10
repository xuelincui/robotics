def motion_F_matrix(dt, strModel, dim):
    """
    This is a generic function.
    This function creates F matrix (State Transition Matrix) for the motion dynamic models.
    
    Inputs
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Variable      Variable Type       Units       Description
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    dt            scalar              seconds     time between samples
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    strModel      string                          the order of the model:
                                                  'constant':     static model, no movemet 
                                                  'linear':       constant velocity model
                                                  'quadratic':    constant acceleration model
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    dim           scalar integer                  dimension of the model:
                                                  dim = 1: single dimension (X axis)
                                                  dim = 2: two dimensions (X,Y axes)
                                                  dim = 3: three dimensions (X,Y,Z axes)
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    
    Outputs
    -------------------------------------------------------------------------------------------------------------------------------------------------------
    Variable      Variable Type       Units       Description
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    F             matrix                          Dynamic Model Matrix
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    For example, for model = 'linear' and dim = 2, the F matrix looks like this:
    
    F = [1     dt    0     0;
         0     1     0     0;
         0     0     1     dt;     
         0     0     0     1];


    """
    import numpy as np

    # sanity checks
    assert (0 < dim <= 3) and (dim == round(dim)), 'The ''dim'' variable must be a positive integer between 1 and 3'

    if strModel == 'constant':
        order = 0
    elif strModel == 'linear':
        order = 1
    elif strModel == 'quadratic':
        order = 2
    else:
        raise Exception('Unknown motion model type')

    # Create one - dimensional F
    F1D = np.zeros((order + 1, order + 1))

    F1D[0,0] = 1

    # create first row
    for i in range(1, order+1):
        F1D[0,i] = F1D[0,i-1] * dt / i

    # create other rows
    for i in range(1, order+1):
        F1D[i, i:] = F1D[i - 1, (i - 1) : -1]

    # Create multi - dimensional F
    F = np.zeros(((order + 1) * dim, (order + 1) * dim))

    # insert F1D in the right places
    for i in range(dim):
        ix1 = i * (order + 1)
        ix2 = ix1 + order + 1
        F[ix1: ix2, ix1: ix2] = F1D

    return F