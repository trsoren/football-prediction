import tensorflow as tf
from tensorflow import keras
import pandas as pd
from sklearn.preprocessing import StandardScaler


# Load the csv data into pandas dataframes
df_train = pd.read_csv('nn_data_train.csv')
df_test = pd.read_csv('nn_data_test.csv')

# Convert the "outcome" column to numerical values
df_train['outcome'], label_strings = pd.factorize(df_train['outcome'])
df_test['outcome'], label_strings = pd.factorize(df_test['outcome'])

# Normalize the input features. Fit scalar on train data only, then apply to train and test.
scaler = StandardScaler()
X_train = scaler.fit_transform(df_train.drop(['outcome'], axis=1))
y_train = df_train['outcome'].values
X_test = scaler.transform(df_test.drop(['outcome'], axis=1))
y_test = df_test['outcome'].values


model = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(512,)),
    keras.layers.Dense(6, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))

test_loss, test_acc = model.evaluate(X_test, y_test)
print('Test accuracy:', test_acc)

import matplotlib.pyplot as plt

history = model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper right')
plt.show()