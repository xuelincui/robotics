def avgFilter(z, x0):
    """
    This is a generic function.
    This function runs the Averaging Filter in the loop for all measurements.

    Inputs
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Variable      Variable Type       Description
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    z             vector              Measurements
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    x0            scalar              Initial value
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------


    Outputs
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Variable      Variable Type       Description
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    x_est         vector              Record of estimations for each filter iteration
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------

    """
    import numpy as np
    from KF_OneDim.staicDynamicModel import staicDynamicModel
    from KF_OneDim.avgStateUpdate import avgStateUpdate

    # initiate

    x = x0
    n = z.size
    x_est = np.zeros(n)

    # run the filter

    for i in range(n):
        # predict
        x_p, _ = staicDynamicModel(x)

        # update
        x = avgStateUpdate(x_p, z[i], i+1)

        # keep the record of estimations
        x_est[i] = x


    return x_est


