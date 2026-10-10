def KF_1D(z, r, x0, p0, q, strModel):
    """
    This is a generic function.
    This function runs the 1D Kalman Filter in the loop for all measurements.

    Inputs
    -------------------------------------------------------------------------------------------------------------------------------------------------------
    Variable      Variable Type       Description
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    z             vector              Range measurements
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    r             scalar              Measurement error
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    x0            vector              Initial State Vector
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    p0            vector              Initial Estimate variance
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    q             scalar              The Process Noise Variance
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    strModel      string              The dynamic model (currently only 'constant' model supported)
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------



    %Outputs
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    x_est         vector              Record of estimations for each filter iteration
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    x_pred        vector              Record of predictions for each filter iteration
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    p_est         vector              Record of estimates uncertainties for each filter iteration
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    p_pred        vector              Record of predictions uncertainties for each filter iteration
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    k             vector              Records of the Kalman Gain for each filter iteration
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------

    """

    import numpy as np
    from KF_OneDim.staicDynamicModel import staicDynamicModel

    # filter initiation
    x = x0
    p = p0

    # dimensions
    n = z.size

    x_est = np.zeros(n)
    p_est = np.zeros(n)
    k = np.zeros(n)
    x_pred = np.zeros(n + 1)
    p_pred = np.zeros(n + 1)

    # Run the filter
    # step 0
    r_sq = r**2

    for i in range(n):
        # predict
        if strModel == 'constant':
            x_p, p_p = staicDynamicModel(x, p, q)

        # update
        KG = p_p / (p_p + r_sq)  # Kalman Gain

        x = x_p + KG * (z[i] - x_p)
        p = (1 - KG) * p_p

        # update the record
        x_est[i] = x
        p_est[i] = p
        k[i] = KG
        x_pred[i] = x_p
        p_pred[i] = p_p

    # predict the next state
    if strModel == 'constant':
        x_pred[i + 1], p_pred[i + 1] = staicDynamicModel(x, p, q)

    return x_est, x_pred, p_est, p_pred, k