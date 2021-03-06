import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import GradientBoostingRegressor
import pandas as pd
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
from sklearn import metrics


# plots mse vs n_estimators to find optimal n_tree for gradient boosting
def plot_n_trees(features, label, n_trees):
    num_trees = []
    errors = []

    for num in range(1, n_trees):
        num_trees.append(num)

    for n in range(1, n_trees):
        X = np.array(features)
        y = np.array(label)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, shuffle=True, random_state=0)
        regressor = GradientBoostingRegressor(n_estimators=n, learning_rate=0.1,  random_state=0).fit(X_train, y_train)
        regressor.fit(X_train, y_train)
        y_pred = regressor.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        errors.append(mse)

    fig, axs = plt.subplots(1)
    axs.plot(num_trees, errors)
    axs.set_xlabel('Number of Estimators')
    axs.set_ylabel('MSE')

    plt.show()

if __name__ == '__main__':
    df = pd.read_csv('../raw_csvs/bitcoin_truncated.csv', low_memory=False)
    df['market_price'] = df['market_price'].shift(-1)
    df.drop(len(df)-1, axis=0, inplace=True)
    df_label = df['market_price']
    df.drop(['date', 'Unnamed: 0', 'Unnamed: 0.1'], 1, inplace=True)
    df = df.sample(frac=1, random_state=0)

    X = np.array(df)
    y = np.array(df_label)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, shuffle=False, random_state=0)
    regressor = GradientBoostingRegressor(n_estimators=50, learning_rate=0.1,
                                          random_state=0, loss='ls').fit(X_train, y_train)
    y_pred = regressor.predict(X_test)

    print('Performance')
    print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
    print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
    print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
    print()
    print(y_pred[-10:])

    # plot_n_trees(df, df_label, 200)
