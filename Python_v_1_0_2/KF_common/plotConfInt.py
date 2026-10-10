def plotConfInt(x, p, t, pctConf):
    """
    Description
    This function plots confidence intervals

    Inputs
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Variable      Variable Type       Description
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    x             vector              Estimates
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    p             vector              Record of estimates uncertainties for each filter iteration
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    t             vector              Time stamps
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    pctConf       scalar              Confidence Interval (Percents)
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    """
    import numpy as np
    from matplotlib import pyplot as plt
    from scipy.stats import norm

    xStd = np.sqrt(p)  # theta estimation uncertainty (std)
    zScore = norm.ppf(1-(1-pctConf/100)/2)  # z-score for 95% confidence
    xConf = xStd * zScore

    art = plt.fill_between(t, x - xConf, x + xConf, color='#FFFF99', edgecolor='#FF804D',
                           linewidth=1, alpha=0.6, label='95% confidence interval')
    art.set_edgecolor('#FF804D')