def plots_2(x_true, v_true, x_est, v_est, x_pred, v_pred, z, dt):
    """
    This function creates position and velocity plots for examples 2 and 3.
    
    Inputs
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Variable      Variable Type       Units       Description
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    x_true        vector              meters      The true position
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    v_true        vector              m/s         The true velocity
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    x_est         vector              meters      Record of position estimations for each filter iteration
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    v_est         vector              m/s         Record of velocity estimations for each filter iteration
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    x_pred        vector              meters      Record of position predictions for each filter iteration
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    v_pred        vector              m/s         Record of velocity predictions for each filter iteration
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    z             vector              meters      Range measurements
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    dt            scalar              seconds     time between samples
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------

    """
    import numpy as np
    import matplotlib.pyplot as plt

    t = np.arange(dt, (x_true.size+1)*dt, dt)

    # position plots
    fig = plt.figure(figsize=(17, 9))

    plt.plot(t, x_true, '-gd', markerfacecolor='lime', linewidth=3, markeredgewidth=2, markersize=8,
             label='True values')
    plt.plot(t, z, '-bs', markerfacecolor='c', linewidth=3, markeredgewidth=2, markersize=6,
             label='Measurements')
    plt.plot(t, x_est, '-ro', markerfacecolor='m', linewidth=3, markeredgewidth=2, markersize=8,
             label='Estimates')
    plt.plot(t, x_pred[:-1], '-^', c=(0.4, 0.4, 0.4), markerfacecolor=(0.8, 0.8, 0.8), linewidth=3, markeredgewidth=2, markersize=8,
             label='Prediction')

    plt.grid(which='both', color='0.95', linestyle='-')


    plt.xlabel('Time (s)', fontsize=14, color='darkred')
    plt.ylabel('Range (m)', fontsize=14, color='darkred')
    plt.title('Range vs. time', fontsize=22, color='darkred', fontweight='bold')
    plt.legend(fontsize='x-large')

    # plt.show()

    # velocity plot
    fig = plt.figure(figsize=(17, 9))

    plt.plot(t, v_true, '-gd', markerfacecolor='lime', linewidth=3, markeredgewidth=2, markersize=8,
             label='True values')
    plt.plot(t, v_est, '-ro', markerfacecolor='m', linewidth=3, markeredgewidth=2, markersize=8,
             label='Estimates')
    plt.plot(t, v_pred[:-1], '-^', c=(0.4, 0.4, 0.4), markerfacecolor=(0.8, 0.8, 0.8), linewidth=3, markeredgewidth=2,
             markersize=8,
             label='Prediction')

    plt.grid(which='both', color='0.95', linestyle='-')

    plt.xlabel('Time (s)', fontsize=14, color='darkred')
    plt.ylabel('Velocity (m/s)', fontsize=14, color='darkred')
    plt.title('Velocity vs. time', fontsize=22, color='darkred', fontweight='bold')
    plt.legend(fontsize='x-large')

    plt.show()