def sigmaWeights(n, sigmaPntAlgo, alpha):
    """

    Description
    this function computes the Sigma Points weights for 'original' or 'modified' algorithms

    Inputs
    -------------------------------------------------------------------------------------------------------------------------------------------------------
    Variable      Variable Type       Description
    -------------------------------------------------------------------------------------------------------------------------------------------------------
    n             integer              Number of dimensions
    -------------------------------------------------------------------------------------------------------------------------------------------------------
    sigmaPntAlgo  string              The algorithm type for Sigma Poins Calculation. It can be 'original' or 'modified'
    -------------------------------------------------------------------------------------------------------------------------------------------------------
    alpha         scalar              Tunning parameter for the 'modified' sigma-points algorithm
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------


    Outputs
    -------------------------------------------------------------------------------------------------------------------------------------------------------
    Variable      Variable Type       Description
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    weights       dict                Unscented Transform Weights
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Lambda     	  scalar              'modified' algorithm parameter
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------

    """

    import numpy as np



    if sigmaPntAlgo == 'original':
        kappa = 3 - n  # hardcoded for the Gaussian distribution
        w0_m = kappa / (n + kappa)  # weights for the mean
        w_i = 1 / (n + kappa) / 2   # weights for the other sigma points
        w0_c = w0_m
        Lambda = kappa

    elif sigmaPntAlgo == 'modified':
        betta = 2  # hardcoded for the Gaussian distribution
        kappa = 0  # hardcoded
        Lambda = (alpha ** 2) * (n + kappa) - n
        w0_m = Lambda / (Lambda +n)            # weights for the mean
        w0_c = w0_m + 1 - alpha ** 2 + betta    # weights for the covariance
        w_i  = 1 / (Lambda + n) / 2             # weights for the other sigma points


    w_m = np.concatenate([np.array([w0_m]), np.tile(w_i, 2 * n)]).reshape((2*n+1, 1))
    w_c = np.diag(np.concatenate([np.array([w0_c]), np.tile(w_i, 2 * n)]))

    weights = {
        "w_m": w_m,
        "w_c": w_c
    }

    # weights.w_m = [w0_m, repmat(w_i, 1, 2 * n)]'
    # weights.w_c = diag([w0_c, repmat(w_i, 1, 2 * n)])
    return weights, Lambda