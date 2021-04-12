#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

cerveza_df = pd.read_csv("./datasets/Consumo_cerveja.csv")
# cerveza_df.head()
# cerveza_df.info()

X1 = cerveza_df['Temperatura Media (C)']
X2 = cerveza_df['Temperatura Minima (C)']
X3 = cerveza_df['Temperatura Maxima (C)']
X4 = cerveza_df['Precipitacao (mm)']
X5 = cerveza_df['Final de Semana']
y = cerveza_df['Consumo de cerveja (litros)']

def lin_reg_betas(x, beta1, beta0):
	y_hat = (beta1 * x) + beta0
	return y_hat

def resultado(X_n, x_input):
	if X_n == 1:
		x = X1
	elif X_n == 2:
		x = X2
	elif X_n == 3:
		x = X3
	elif X_n == 4:
		x = X4
	elif X_n == 5:
		x = X5
	else:
		x = X3

	beta_1 = np.sum((x - np.mean(x)) * (y - np.mean(y))) / np.sum((x - np.mean(x))**2)
	beta_0 = np.mean(y) - (beta_1 * np.mean(x))
	# print(beta_1,beta_0)

	SST = np.sum((y - np.mean(y))**2)
	SSR = np.sum((y - lin_reg_betas(x, beta_1, beta_0))**2)
	R = 1 - (SSR/SST) 
	# print(R)

	mse = np.sum((y - lin_reg_betas(x, beta_1, beta_0))**2) / len(y)
	mae = np.sum(np.abs(y - lin_reg_betas(x, beta_1, beta_0))) / len(y)
	mape = np.sum(np.abs((y - lin_reg_betas(x, beta_1, beta_0))/y)) / len(y)
	# print(mse,mae,mape)

	# fig, ax = plt.subplots(1, 1, figsize=(20,10))
	# ax.plot(x,lin_reg_betas(x, beta_1, beta_0))
	# ax.scatter(x,y)
	# ax.vlines(x, y, lin_reg_betas(x, beta_1, beta_0), color = 'red', alpha = 0.5)
	# plt.show()

	return lin_reg_betas(x_input, beta_1, beta_0)
