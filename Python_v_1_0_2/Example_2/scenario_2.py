def scenario_2(dt):
    """
    This function creates scenario for example 2 - a constant-velocity aircraft

    Inputs
    ----------------------------------------------------------------------------------------
    Variable        Variable Type       Units       Description
    ----------------------------------------------------------------------------------------
    dt              scalar              seconds     time between samples
    ----------------------------------------------------------------------------------------

    Outputs
    -------------------------------------------------------------------------------------------------------------------------------------------------------
    Variable      Variable Type       Units       Description
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    x             vector              meters      aircraft range
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    v             vector              m/s         aircraft velocity
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------

    """

    import numpy as np
    import matplotlib.pyplot as plt
    from Example_2.initParams_2 import initParams_2

    # init parameters
    params = initParams_2('scenario')

    x = np.zeros(params["n"])       # preset range
    v = params["v0"] * np.ones(params["n"])   # set velocity

    x[0] = params["x0"] + params["v0"] * dt

    for i in range(1, params["n"]):
        x[i] = x[i - 1] + v[i - 1] * dt


    if params["isPlotScenario"]:
        # plots of the aircraft position and velocity
        t = np.arange(0, x.size+1)*dt    # time vector

        fig, axs = plt.subplots(2, figsize=(17, 9))
        axs[0].plot(t, np.concatenate((np.array([params["x0"]]), x)) / 1e3, '-m', linewidth=3)
        axs[0].set_xlabel('Time (s)', fontsize=14, color='darkred')
        axs[0].set_ylabel('Range (km)', fontsize=14, color='darkred')
        axs[0].set_title('Range vs. Time', fontsize=22, color='darkred', fontweight='bold')

        axs[1].plot(t, np.concatenate((np.array([params["v0"]]), v)), '-c', linewidth=3)
        axs[1].set_xlabel('Time (s)', fontsize=14, color='darkred')
        axs[1].set_ylabel('Velocity (m/s)', fontsize=14, color='darkred')
        axs[1].set_title('Velocity vs. Time', fontsize=22, color='darkred', fontweight='bold')

        fig.tight_layout()
        # plt.show()

    return x, v