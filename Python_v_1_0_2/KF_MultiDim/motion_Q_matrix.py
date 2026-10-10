def motion_Q_matrix(dt, sig_a, strModel, dim, strNoiseModel):
    """
    This is a generic function.
    This function creates Q matrix (Process Noise Matrix) for the motion dynamic models.

    
    Inputs
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Variable          Variable Type       Units       Description
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    dt                scalar              seconds     time between samples
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    sig_a             scalar              m/(s^2)     acceleration standard deviation
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    strModel          string                          the order of the model:
                                                      'constant':     static model, no movemet 
                                                      'linear':       constant velocity model
                                                      'quadratic':    constant acceleration model
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    dim           	integer                           dimension of the model:
                                                      dim = 1: single dimension (X axis)
                                                      dim = 2: two dimensions (X,Y axes)
                                                      dim = 3: three dimensions (X,Y,Z axes)
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    strNoiseModel     string                          the order of the model:
                                                      'discrete':     discrete noise model
                                                      'continuous':   continuous noise model (integral of  the discrete noise model)
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    
    Outputs
    -------------------------------------------------------------------------------------------------------------------------------------------------------
    Variable      Variable Type       Units       Description
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Q             matrix                          Process Noise Matrix
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    For example, for model = 'quadratic', noise model = 'discrete' and dim = 3, the Q matrix looks like this:
    
    Q = [dt^4/4     dt^3/2   dt^2/2      0           0   	    0;      
         dt^3/2     dt^2     dt          0           0   	    0;      
         dt^2/2     dt       1           0           0          0;
         0          0        0           dt^4/4      dt^3/2     dt^3/2;
         0          0        0           dt^3/2      dt^2       dt;
         0          0        0           dt^2/2      dt         1] *sig_a^2;

    """

    import numpy as np
    from KF_MultiDim.motion_F_matrix import motion_F_matrix

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

    # Compute one-dimensional Q
    F = motion_F_matrix(dt, 'quadratic', 1)     # create single dimension F matrix for quadratic model

    Qa = np.zeros((F.shape))    # crete Qa matrix
    Qa[-1,-1] = sig_a**2

    Q1D = F @ Qa @ F.T                          # Compute Q
    Q1D = Q1D[0:(order + 1), 0: (order + 1)]    # Cut Q according to the model

    # Compute Q for continuous noise model
    if strNoiseModel == 'continuous':   # integrate Q
        # create element-wise divider for Q
        Qm = np.zeros((order + 1, order + 1))
        for i in range(0,order+1):
            for j in range(0,order+1):
                Qm[i, j] = 5 - i - j

        Qm = 1/ Qm    # element-wise division

        Q1D = Q1D*Qm*dt

    # Create multi-dimensional Q
    Q = np.zeros(((order + 1) * dim, (order + 1) * dim))

    # insert Q1D in the right places
    for i in range(dim):
        ix1 = i * (order + 1)
        ix2 = ix1 + order + 1
        Q[ix1: ix2, ix1: ix2] = Q1D

    return Q
