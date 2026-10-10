def uniform2normal(x_uniform):
    """
    This function converts random samples form uniform distribution to normal distribution
    using inverse transform sampling (https://en.wikipedia.org/wiki/Inverse_transform_sampling).

    Actually, in order to create normally distributed random samples, one can use Numpy command:
    'np.random.rand'

    However, I am using this type of conversion for the sake of example, in order reproduce identical random
    samples in the Python code of the book and the Matlab code of the book
    (in the real-life applications there is no need for such a function).

    Matlab and Numpy random generators produce different samples for normal distribution although the same seed is used.
    i.e. for the same seed, Matlab command 'randn' and  Numpy command 'np.random.randn' yield different samples

    On the other hand, Matlab and Numpy random generators produce identical samples for uniform distribution if the same seed is used.
    i.e. for the same seed, Matlab command 'rand' and  Numpy command 'np.random.rand' yield identical samples
    
    Inputs
    --------------------------------------------------------------------------
    Variable      Variable Type       Units       Description
    --------------------------------------------------------------------------
    x_uniform     matrix                          Uniformly distributed noise
    --------------------------------------------------------------------------
    
    Outputs
    --------------------------------------------------------------------------
    Variable      Variable Type       Units       Description
    --------------------------------------------------------------------------
    x_normal      matrix                          Normally distributed noise
    --------------------------------------------------------------------------
    """
    from numpy import sqrt
    from scipy.special import erfinv

    x_normal = sqrt(2) * erfinv(2 * x_uniform - 1)

    return x_normal

def addNoise(X, sigma, params):
    """
    This is a generic function.
    This function creates measurements by adding a random noise to the simulated true system state.
    It is possible to provide 'seed' to the function in order to produce the same random sequence, each time when we create measurements.
    It allows to compare different Kalman Filter outputs during parameters calibration.

    Inputs:
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Variable      Variable Type                   Description
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    X              matrix                          true system state (in the measurement domain)
                                                   (rows represent different states)
                                                   (columns represent states at different time samples)
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    sigma          scalar/vector/matrix            Uncertainty (standard deviation)
                                                   - if sigma is a scalar, the same measurement uncertainty is applied for each state and for each time sample
                                                   - if sigma is a column vector, each element represents the measurement uncertainties for different states,
                                                     while the same measurement uncertainty is applied for each time sample.
                                                   - if sigma is a row vector, each element represents the measurement uncertainties for different time samples,
                                                     while the same measurement uncertainty is applied for state.
                                                   - if sigma is a matrix, each element represents a unique measurement uncertainty for each element in X
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------

    Paramerters (params):
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Variable      Variable Type                     Description
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    seed           scalar integer                   used to produce the same random sequence, each time when we create measurements
                                                    optional parameter (pass empty if not required)
                                                    (columns represent states at different time samples)
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    numOfDecimals  scalar integer                   the number of fractional digits or decimal places (the number of digits following the decimal point)
                                                    for rounding noise if required (usually used for presentation convenience)
                                                    optional parameter
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------

    Outputs:
    -------------------------------------------------------------------------------------------------------------------------------------------------------
    Variable      Variable Type       Units       Description
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Z               matrix                        measurements
                                                  (rows represent different states)
                                                  (columns represent states at different time samples)
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------

    """

    import numpy as np

    # create Measurement Uncertainty for each state and each time sample

    if sigma.size == 1:
        S = np.tile(sigma, X.shape)
    elif sigma.shape[0] > 1 and sigma.shape[1] == 1:  # r is a column vector
        assert sigma.size == X.shape[0], 'Dimension mismatch'  # sanity checks
        S = np.tile(sigma, (1, X.shape[1]))
    elif sigma.shape[0] == 1 and sigma.shape[1] > 1:  # r is a row vector
        assert sigma.size == X.shape[1], 'Dimension mismatch'  # sanity checks
        S = np.tile(sigma, (X.shape[0], 1))
    elif sigma.ndim == 2:  # r is a matrix
        assert X.shape == sigma.shape, 'Dimension mismatch'  # sanity checks
        S = sigma
    elif sigma.ndim > 2:
        raise Exception('Too many dimensions in r')

    # apply seed to random number generator
    if "seed" in params:
        seed = params["seed"]
        np.random.seed(seed[0])

    # add noise
    randUniform = np.random.rand(*X.shape)    # generate uniform noise
    randNormal = uniform2normal(randUniform)  # convert uniform distribution to normal distribution

    noise = randNormal*S

    Z = X + noise

    # round if required(usually used for presentation convenience)
    if "numOfDecimals" in params:
        Z = np.around(Z, params["numOfDecimals"])

    # return random number generator to default
    if "seed" in params:
        np.random.seed()

    return Z