def alphaBetaGammaFilter(dt, x0, v0, a0, z, alpha, beta, gamma=0):

    """
    This is a generic function.
    This function runs the alpha-beta-gamma filter in the loop for all measurements.


    Inputs
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Variable      Variable Type       Units       Description
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    dt            scalar              seconds     time between samples
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    x0            scalar              meters      Initial position
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    v0            scalar              m/s         Initial velocity
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    a0            scalar              m/s^2       Initial acceleration
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    z             vector              meters      Range measurements
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    alpha         scalar                          The alpha factor
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    beta          scalar                          The beta factor
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    gamma         scalar                          The gamma factor (optional parameter)
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------


    Outputs
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Variable      Variable Type       Units       Description
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    x_pred        vector              meters      Record of position predictions for each filter iteration
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    v_pred        vector              m/s         Record of velocity predictions for each filter iteration
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    a_pred        vector              m/s^2       Record of acceleration predictions for each filter iteration
    %------------------------------------------------------------------------------------------------------------------------------------------------------------------
    x_est         vector              meters      Record of position estimations for each filter iteration
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    v_est         vector              m/s         Record of velocity estimations for each filter iteration
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    a_est         vector              m/s^2       Record of acceleration estimations for each filter iteration
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------

    """
    import numpy as np
    from KF_OneDim.motionDynamicModel import motionDynamicModel
    from KF_OneDim.alphaBetaGammaStateUpdate import alphaBetaGammaStateUpdate

    # initiate
    x = x0
    v = v0
    a = a0

    n = z.size

    x_est = np.zeros(n)
    v_est = np.zeros(n)
    a_est = np.zeros(n)
    x_pred = np.zeros(n + 1)
    v_pred = np.zeros(n + 1)
    a_pred = np.zeros(n + 1)

    # run the filter

    for i in range(n):
        # predict
        [x_p, v_p, a_p] = motionDynamicModel(dt, x, v, a)

        # update
        [x, v, a] = alphaBetaGammaStateUpdate(dt, x_p, v_p, a_p, z[i], alpha, beta, gamma)

        # keep the record of estimations
        x_est[i] = x
        v_est[i] = v
        a_est[i] = a
        x_pred[i] = x_p
        v_pred[i] = v_p
        a_pred[i] = a_p

    # predict the next state
    [x_p, v_p, a_p] = motionDynamicModel(dt, x, v, a)
    x_pred[i + 1] = x_p
    v_pred[i + 1] = v_p
    a_pred[i + 1] = a_p

    return x_est, v_est, a_est, x_pred, v_pred, a_pred
