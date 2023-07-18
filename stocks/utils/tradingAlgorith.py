## Time-Series Analyzer ##

import statsmodels.api as sm
import statsmodels.tsa.ar_model as ar
import matplotlib.pyplot as plt
from apiconnection import close_prices_week, close_prices_month

## Plot function
def plot_model_results(model_name, fitted_values_weekly, fitted_values_monthly, close_prices_week, close_prices_month):
    plt.figure()
    plt.plot(close_prices_week.index[:len(fitted_values_weekly)], close_prices_week[:len(fitted_values_weekly)], label='Close Prices (Weekly)')
    plt.plot(close_prices_week.index[:len(fitted_values_weekly)], fitted_values_weekly, label=model_name + ' Model (Weekly)')
    plt.plot(close_prices_month.index[:len(fitted_values_monthly)], fitted_values_monthly, label=model_name + ' Model (Monthly)')
    plt.plot(close_prices_month.index[:len(fitted_values_monthly)], close_prices_month[:len(fitted_values_monthly)], label='Close Prices (Monthly)')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title('Close Prices - ' + model_name + ' Model')
    plt.legend()
    plt.show()

selection = input("Select the model (AR, MA, or ARMA): ")

## The code of the models is not a one to one of the actual formulas.
## This is because we are using the statsmodels library to derive the
## AR, MA, and ARMA formulas for usage.

if selection.lower() == "ar":
    ## AR Model
    lag_order_ar = 1
    model_ar = ar.AutoReg(close_prices_week, lags=lag_order_ar) ## Makes model object and sets historical price and lags
    model_fit_ar = model_ar.fit() ## Fitting model to data
    print("AR Model:")
    print(model_fit_ar.summary()) ## Model Summary
    print()
    fitted_values_weekly_ar = model_fit_ar.fittedvalues
    fitted_values_monthly_ar = model_fit_ar.predict(start=0, end=len(close_prices_month) - 1)
    plot_model_results("AR", fitted_values_weekly_ar, fitted_values_monthly_ar, close_prices_week, close_prices_month) ## Plots all defined values

elif selection.lower() == "ma":
    ## MA Model
    lag_order_ma = 3
    model_ma = sm.OLS(close_prices_week, sm.add_constant(close_prices_week.shift(1)).dropna())
    model_fit_ma = model_ma.fit()
    print("MA Model:")
    print(model_fit_ma.summary())
    print()
    fitted_values_weekly_ma = model_fit_ma.fittedvalues
    fitted_values_monthly_ma = model_fit_ma.predict(start=0, end=len(close_prices_month) - 1)
    plot_model_results("MA", fitted_values_weekly_ma, fitted_values_monthly_ma, close_prices_week, close_prices_month)

elif selection.lower() == "arma":
    ## ARMA Model
    lag_order_arma = (2, 3) ## ARMA model has both AR and MA values
    model_arma = sm.tsa.ARMA(close_prices_week, order=lag_order_arma)
    model_fit_arma = model_arma.fit()
    print("ARMA Model:")
    print(model_fit_arma.summary())
    print()
    fitted_values_weekly_arma = model_fit_arma.fittedvalues
    fitted_values_monthly_arma = model_fit_arma.predict(start=0, end=len(close_prices_month) - 1)
    plot_model_results("ARMA", fitted_values_weekly_arma, fitted_values_monthly_arma, close_prices_week, close_prices_month)

else:
    print("Invalid selection")