from Example_5.plots_5 import plots_5
import numpy as np
import scipy.io as sio

mat_contents = sio.loadmat('ex5_old.mat')

x_true = np.squeeze(mat_contents['trueVal'])
x_est = np.squeeze(mat_contents['currEst'])
x_pred = np.squeeze(mat_contents['prevEst'])

z = np.squeeze(mat_contents['measVal'])

p_est = np.squeeze(mat_contents['currErr'])
p_pred = np.squeeze(mat_contents['prevErr'])

k = np.squeeze(mat_contents['Kg'])
r = np.squeeze(mat_contents['measErr'])

plots_5(x_true, x_est, x_pred, p_est, p_pred, k, z, np.sqrt(r))
