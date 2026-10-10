def motion_G_matrix(dt, strModel):
    """
    This is a generic function.
    This function creates G matrix (Control Matrix) for the motion dynamic models.

    
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
    
    
    Outputs
    -------------------------------------------------------------------------------------------------------------------------------------------------------
    Variable      Variable Type       Units       Description
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    G             matrix                          Control Matrix
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    For example, for model = 'linear', the G matrix looks like this:
    
    G = [0.5*dt^2; ...
         dt]  

    """
    import numpy as np

    if strModel == 'constant':
        order = 1
    elif strModel == 'linear':
        order = 2
    elif strModel == 'quadratic':
        raise Exception('For quadratic model, the acceleration shall be a part of the F matrix')
    else:
        raise Exception('Unknown motion model type')

    G = np.zeros((2, 1))

    G[0] = dt**order / order
    G[1] = dt**(order - 1)

    return G