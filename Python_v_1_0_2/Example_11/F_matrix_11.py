def F_matrix_11(x, Fargs):
    """
    Description
    This function creates F matrix (State Transition Matrix) for example 11.

    Inputs
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Variable                Variable Type       Units           Description
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    x                       matrix                              The vehicle position, velocity and acceleration
                                                                (first row is the X axis position, second row is the X axis velocity, third row is is the X axis acceleration)
                                                                (fourth row is the Y axis position, fifth row is the Y axis velocity, sixth row is is the Y axis acceleration)
                                                                (columns represent states at different time samples)
    -------------------------------------------------------------------------------------------------------------------------------------------------------
    Fargs[0] - dt           scalar              seconds         time between samples
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Fargs[1] - strModel 	string                              the order of the model:
                                                                'constant':     static model, no movemet
                                                                'linear':       constant velocity model
                                                                'quadratic':    constant acceleration model
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Fargs[2] - dim     	    scalar integer                      dimension of the model:
                                                                dim = 1: single dimension (X axis)
                                                                dim = 2: two dimensions (X,Y axes)
                                                                dim = 3: three dimensions (X,Y,Z axes)
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------


    Outputs
    -------------------------------------------------------------------------------------------------------------------------------------------------------
    Variable                Variable Type        Units          Description
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    F                       matrix                              State Transition Matrix
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    dF                      matrix                              Derivative of F
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------

    """
    from KF_MultiDim.motion_F_matrix import motion_F_matrix

    dt = Fargs[0]
    strModel = Fargs[1]
    dim = Fargs[2]

    F = motion_F_matrix(dt, strModel, dim)  # create F matrix (State Transition Matrix)

    Fx = F @ x  # the State Space Model is linear
    dFx = F  # derivative of(Fx)

    return Fx, dFx
