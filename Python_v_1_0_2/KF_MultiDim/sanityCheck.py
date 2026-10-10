def sanityCheck(Z, R, H, F, Q, P0, x0, G=None, U=None, u0=None):
    """
    This is a generic function.
    This function check the size of all building blocks of the Kalman Filter.
    In case of inconsistency, the function throws an error

    Inputs
    -------------------------------------------------------------------------------------------------------------------------------------------------------
    Variable      Variable Type       Size            Description
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Z             matrix              n_z * n_m       measurements
                                                      rows represent different states)
                                                      (columns represent states at different time samples)
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    R             matrix              n_z * n_z       Measurement Noise Matrix
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    H             matrix              n_z * n_x       Observation Matrix
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    F             matrix              n_x * n_x       Dynamic Model Matrix
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Q             matrix              n_x * n_x       Process Noise Matrix
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    P0            matrix              n_x * n_x       Initial Estimate Covariance Matrix
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    x0            vector              n_x * 1         Initial State Vector
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    G             vector              n_x * n_u       Control Matrix
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    U             matrix              n_u * n_m       Control Input
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    u0            vector              n_u * 1         Initial Control Input
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    n_x is the number of states
    n_z is the number of measured parameters
    N   is the number of measurements

    """
    import numpy as np

    # extract n_x, n_z, n_u, and n_m
    if Z.ndim == 1:
        Z = np.reshape(Z, (1, -1))
    n_z = Z.shape[0]

    if x0.ndim == 1:
        x0 = np.reshape(x0, (-1, 1))
    n_x = x0.shape[0]

    if G is not None:
        # if the control input presents
        n_m = Z.shape[1]

        if U.ndim == 1:
            U = np.reshape(U, (1, -1))
        n_u = U.shape[0]

        if u0.ndim == 1:
            u0 = np.reshape(u0, (-1, 1))

    # perform the sanity check
    assert R.shape == (n_z, n_z),  'The dimensions of the R matrix are wrong'
    if H is not None:
        assert H.shape == (n_z, n_x),  'The dimensions of the H matrix are wrong'
    if F is not None:
        assert F.shape == (n_x, n_x),  'The dimensions of the F matrix are wrong'
    assert Q.shape == (n_x, n_x),  'The dimensions of the Q matrix are wrong'
    assert P0.shape == (n_x, n_x), 'The dimensions of the P0 matrix are wrong'
    assert x0.shape == (n_x, 1),   'The dimensions of the xO vector are wrong'

    if G is not None:
        # if the control input presents
        assert G.shape == (n_x, n_u), 'The dimensions of the G matrix are wrong'
        assert U.shape == (n_u, n_m), 'The dimensions of the U matrix are wrong'
        assert u0.shape == (n_u, 1),  'The dimensions of the u0 matrix are wrong'

    return Z, x0, U, u0