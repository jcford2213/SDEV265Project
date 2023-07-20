## Time-Series Analyzer ##

import statsmodels.api as sm
import statsmodels.tsa.ar_model as ar
import statsmodels.tsa.arima.model as arima_model
from statsmodels.tsa.statespace.sarimax import SARIMAX

## The code of the models is not a one to one of the actual formulas.
## This is because we are using the statsmodels library to derive the
## AR, MA, and ARMA formulas for usage.

def getArModel(close_prices_week, close_prices_month):
 ## AR Model
  lag_order_ar = 1
  model_ar = ar.AutoReg(close_prices_week, lags=lag_order_ar) ## Makes model object and sets historical price and lags
  model_fit_ar = model_ar.fit() ## Fitting model to data
  fitted_values_weekly_ar = model_fit_ar.fittedvalues
  fitted_values_monthly_ar = model_fit_ar.predict(start=0, end=len(close_prices_month) - 1)
  return {
    'fitted_values_weekly': fitted_values_weekly_ar,
    'fitted_values_monthly': fitted_values_monthly_ar
  }
  

def getMaModel(close_prices_week, close_prices_month):
  ## MA Model
  lag_order_ma = 3
  model_ma = arima_model.ARIMA(close_prices_week, order=(0, 0, lag_order_ma)) ## There is no MA model in statsmodels library so we will use the ARIMA model restricting it to just its MA component
  model_fit_ma = model_ma.fit()
  fitted_values_weekly_ma = model_fit_ma.fittedvalues
  fitted_values_monthly_ma = model_fit_ma.predict(start=0, end=len(close_prices_month) - 1)
  return {
    'fitted_values_weekly': fitted_values_weekly_ma,
    'fitted_values_monthly': fitted_values_monthly_ma,
  }
  

def getArmaModel(close_prices_week, close_prices_month):
  ## ARMA Model
  lag_order_arma = (2, 0, 3)  # ARMA model has both AR and MA values
  model_arma = SARIMAX(close_prices_week, order=lag_order_arma) ## Issues with ARMA statsmodel datatype so using SARIMAX
  model_fit_arma = model_arma.fit()
  fitted_values_weekly_arma = model_fit_arma.fittedvalues
  fitted_values_monthly_arma = model_fit_arma.predict(start=0, end=len(close_prices_month) - 1)
  return {
    'fitted_values_weekly': fitted_values_weekly_arma,
    'fitted_values_monthly': fitted_values_monthly_arma,
  }