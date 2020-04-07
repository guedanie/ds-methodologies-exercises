# Create a file named evaluate.py that contains the following functions.

# plot_residuals(y, yhat): creates a residual plot
# regression_errors(y, yhat): returns the following values:
# sum of squared errors (SSE)
# explained sum of squares (ESS)
# total sum of squares (TSS)
# mean squared error (MSE)
# root mean squared error (RMSE)
# baseline_mean_errors(y): computes the SSE, MSE, and RMSE for 
# the baseline model

# better_than_baseline(y, yhat): returns true if your model 
# performs better than the baseline, otherwise false

# model_significance(ols_model): that takes the ols model as 
# input and returns the amount of variance explained in your model, 
# and the value telling you whether your model is significantly
#  better than the baseline model (Hint: use the rsquared and 
# f_pvalue properties from the ols model)

import pandas as pd
import seaborn as sns
import numpy as np
from math import sqrt
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score, explained_variance_score


def calculate_y_hat(df, model):
    df["yhat"] = model.predict(df.x)
    return df
    


def plot_residuals(x, y, df, not_residual=True):
    '''
    Plot the residuals for the linear regression model that you made.
    '''
    if not_residual:
        sns.scatterplot(x=y, y=x, data=df)
        plt.figure(figsize=(8, 5))
        plt.scatter(x, x - y, color='dimgray')

        # add the residual line at y=0
        plt.annotate('', xy=(70, 0), xytext=(100, 0), xycoords='data', textcoords='data', arrowprops={'arrowstyle': '-', 'color': 'darkseagreen'})

        # set titles
        plt.title(r'Baseline Residuals', fontsize=12, color='black')
        # add axes labels
        plt.ylabel(r'$\hat{y}-y$')
        plt.xlabel('var $x$')

        # add text
        plt.text(85, 15, r'', ha='left', va='center', color='black')

        return plt.show()
        
    else:
        df['residual'] = df["yhat"] - df["y"]
        sns.scatterplot(x="yhat", y="residual", data=df)
        plt.figure(figsize=(8, 5))
        plt.scatter(df.x, df.residual, color='dimgray')

        # add the residual line at y=0
        plt.annotate('', xy=(70, 0), xytext=(100, 0), xycoords='data', textcoords='data', arrowprops={'arrowstyle': '-', 'color': 'darkseagreen'})

        # set titles
        plt.title(r'Baseline Residuals', fontsize=12, color='black')
        # add axes labels
        plt.ylabel(r'$\hat{y}-y$')
        plt.xlabel('var $x$')

        # add text
        plt.text(85, 15, r'', ha='left', va='center', color='black')

        return plt.show()

def regression_errors(df):
    '''
    Returns a dataframe with the following values: SSE, ESS, TSS, MSE, RMSE for the y 
    '''

    # SSE
    SSE = mean_squared_error(df.y, df.yhat) * len(df)
    # # ESS
    # ESS = sum((df.yhat - df["y"].mean())**2)
    # # TSS
    # TSS = ESS + SSE
    # MSE
    MSE = mean_squared_error(df.y, df.yhat)
    # RMSE
    RMSE = sqrt(mean_squared_error(df.y, df.yhat))
    ss = pd.DataFrame(np.array(["SSE", "MSE", "RMSE"]), columns=["metric"])
    ss["model_values"] = np.array([SSE, MSE, RMSE])
    return ss


def baseline_mean_errors(df, mean=True):
    '''
    Returns a dataframe with the following values: SSE, ESS, TSS, MSE, RMSE for the baseline
    '''
    if mean:
        df["yhat_baseline"] = df["y"].mean()
        # SSE
        SSE_bl = mean_squared_error(df.y, df.yhat_baseline) * len(df)
        # MSE
        MSE_bl = mean_squared_error(df.y, df.yhat_baseline)
        # RMSE
        RMSE_bl = sqrt(mean_squared_error(df.y, df.yhat_baseline))
        ss_bl = pd.DataFrame(np.array(["SSE_Baseline", "MSE_Baseline", "RMSE_Baseline"]), columns=["metric"])
        ss_bl["model_values"] = np.array([SSE_bl, MSE_bl, RMSE_bl])
        return ss_bl
    else:
        df["yhat_baseline"] = df["y"].median()
        # SSE
        SSE_bl = mean_squared_error(df.y, df.yhat_baseline) * len(df)
        # MSE
        MSE_bl = mean_squared_error(df.y, df.yhat_baseline)
        # RMSE
        RMSE_bl = sqrt(mean_squared_error(df.y, df.yhat_baseline))
        ss_bl = pd.DataFrame(np.array(["SSE_Baseline", "ESS_Baseline", "TSS_Baseline", "MSE_Baseline", "RMSE_Baseline"]), columns=["metric"])
        ss_bl["model_values"] = np.array([SSE_bl, MSE_bl, RMSE_bl])
        return ss_bl

def mean_errors_delta(df):
    '''
    returns a dataframe with the mean errors for the target variable, as well as the delta for the mean erors for the baseline
    '''
    ss = regression_errors(df)
    ss_bl = baseline_mean_errors(df) 
    ss["delta"] = ss["model_values"] - ss_bl["model_values"]
    return ss

def better_than_baseline(df):
    '''
    returns true if your model performs better than the baseline, otherwise false
    '''
    RMSE = sqrt(mean_squared_error(df.y, df.yhat))
    RMSE_bl = sqrt(mean_squared_error(df.y, df.yhat_baseline))
    if RMSE < RMSE_bl:
        return True
    else:
        return False

def model_significance(model):
    '''
    Returns the R^2 and the p value based on the model that we feed the function
    '''
    return {
        'r^2 -- variance explained': model.rsquared,
        'p-value -- P(data|model == baseline)': model.f_pvalue,
    }