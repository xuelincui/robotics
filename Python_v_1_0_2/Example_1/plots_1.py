def plots_1(x_true, x_est, z):
    """
    This function creates measured vs. estimated vs. true weight plot for example 1.

    Inputs
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Variable      Variable Type       Description
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    x_true        vector              The true value
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    x_est         vector              Record of estimations for each filter iteration
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    z             vector              Measurements
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------

    """
    import numpy as np
    import matplotlib.pyplot as plt

    n = np.arange(1, x_true.size + 1)

    fig = plt.figure(figsize=(17, 9))

    plt.plot(n, z, '-bs', markerfacecolor='c', linewidth=3, markeredgewidth=2, markersize=6,
             label='Measurements')
    plt.plot(n, x_est, '-ro', markerfacecolor='m', linewidth=3, markeredgewidth=2, markersize=8,
             label='Estimates')

    plt.plot(n, x_true, '-gd', markerfacecolor='lime', linewidth=3, markeredgewidth=2, markersize=8,
             label='True values')

    plt.grid(which='both', color='0.95', linestyle='-')

    plt.xlabel('Iterations', fontsize=18, color='darkred')
    plt.ylabel('Weight (g)', fontsize=18, color='darkred')

    plt.legend(fontsize='x-large')

    plt.show()