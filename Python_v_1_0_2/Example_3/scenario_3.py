def scenario_3(dt, isPlotScenario = None):
    """
    This function creates scenario for examples 3 and 4.

    The scenario is divided into two parts:

    1. The aircraft moves with a constant speed for 3 time samples.
    2. The aircraft moves with a constant acceleration for 12 time samples.

    Inputs
    ---------------------------------------------------------------------------------------
    Variable            Variable Type       Units       Description
    ---------------------------------------------------------------------------------------
    dt                  scalar              seconds     time between samples
    ---------------------------------------------------------------------------------------
    isPlotScenario      boolean                         Optional input. Indicates whether to make
                                                        scenario plots
    -------------------------------------------------------------------------------------------

    Outputs
    ------------------------------------------------------------------------------------------
    Variable      Variable Type       Units       Description
    ------------------------------------------------------------------------------------------
    x             vector              meters      aircraft range
    ------------------------------------------------------------------------------------------
    v             vector              m/s         aircraft velocity
    ------------------------------------------------------------------------------------------
    a             vector              m/(s^2)     aircraft acceleration
    ------------------------------------------------------------------------------------------

    """

    import numpy as np
    import matplotlib.pyplot as plt
    from Example_3.initParams_3 import initParams_3

    # init parameters
    params = initParams_3('scenario')

    v0 = params["v0"]  # initial aircraft velocity
    x0 = params["x0"]  # initial aircraft range
    a = params["a"]


    n = a.size

    x = np.zeros(n)      # preset range
    v = np.zeros(n)      # preset velocity

    x[0] = x0 + v0 * dt + 0.5 * a[0] * dt**2
    v[0] = v0 + a[0] * dt

    for i in range(1, n):
        x[i] = x[i-1] + v[i-1] * dt + 0.5 * a[i] * dt**2
        v[i] = v[i-1] + a[i] * dt

    if (isPlotScenario is None):
        isPlotScenario = params["isPlotScenario"]

    if isPlotScenario:
        # plots of the aircraft position and velocity
        t = np.arange(0, x.size+1)*dt    # time vector

        fig, axs = plt.subplots(3, figsize=(17, 9))
        axs[0].plot(t, np.concatenate((np.array([x0]), x)) / 1e3, '-m', linewidth=3)
        axs[0].set_xlabel('Time (s)', fontsize=14, color='darkred')
        axs[0].set_ylabel('Range (km)', fontsize=14, color='darkred')
        axs[0].set_title('Range vs. Time', fontsize=22, color='darkred', fontweight='bold')

        axs[1].plot(t, np.concatenate((np.array([v0]), v)), '-c', linewidth=3)
        axs[1].set_xlabel('Time (s)', fontsize=14, color='darkred')
        axs[1].set_ylabel('Velocity (m/s)', fontsize=14, color='darkred')
        axs[1].set_title('Velocity vs. Time', fontsize=22, color='darkred', fontweight='bold')

        axs[2].plot(t[0:5], np.concatenate((np.array([0]), a[0:4])), '-b', linewidth=3)
        axs[2].plot(t[4:], np.concatenate((np.array([a[4]]), a[4:])), '-b', linewidth=3)
        axs[2].set_xlabel('Time (s)', fontsize=14, color='darkred')
        axs[2].set_ylabel('Acceleration ($m/s^2$)', fontsize=14, color='darkred')
        axs[2].set_title('Acceleration vs. Time', fontsize=22, color='darkred', fontweight='bold')

        fig.tight_layout()
        # plt.show()

    return x, v, a