def plotConfEllipse(mu, C, styleInd, confInterval = 0):
    """
        This function creates a 2D confidence ellipses for a set of estimations

        Inputs
        ----------------------------------------------------------------------------------------------------------------------------------
        Variable        Variable Type       Units       Description
        ----------------------------------------------------------------------------------------------------------------------------------
        mu              matrix                          ellipse centers
                                                        (first row is the X axis coordinates)
                                                        (second row is the Y axis coordinates)
                                                        (columns represent estimates at different time samples)
        ----------------------------------------------------------------------------------------------------------------------------------
        C               matrix                          estimates covariances
                                                        (the first and the second dimensions represent 2x2 covariance matrix)
                                                        (the third dimension represent estimates at different time samples)
        ----------------------------------------------------------------------------------------------------------------------------------
        styleInd       integer                          ellipse style (color)
        ----------------------------------------------------------------------------------------------------------------------------------
        confInterval    matrix                          ellipse confidence interval. if confInterval = 0 , calculate 1 sigma uncertainty
        ----------------------------------------------------------------------------------------------------------------------------------

        Outputs
        ----------------------------------------------------------------------------------------------------------------------------------
        Variable        Variable Type       Units       Description
        ----------------------------------------------------------------------------------------------------------------------------------
        h               handle                          plot handle
        ----------------------------------------------------------------------------------------------------------------------------------
    """
    from matplotlib import pyplot as plt
    from KF_common.confEllipse import confEllipse

    confInterval  = confInterval/100

    ellipseArray = confEllipse(mu, C, confInterval)  # covariance ellipse

    for i in range(len(ellipseArray)):
        elps = ellipseArray[i]
        if styleInd == 1:
            h, = plt.fill(elps[:, 0], elps[:, 1], '#FFFF99', edgecolor='#FF804D', linewidth=1, alpha=0.7)
        else:
            h, = plt.fill(elps[:, 0], elps[:, 1], '#F5D2A3', edgecolor='#E79425', linewidth=1, alpha=0.7)

    return h