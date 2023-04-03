import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf

# Load the csv data into a pandas dataframe
df = pd.read_csv('nn_data.csv')

value_counts = df['outcome'].value_counts(normalize=True) * 100
print("Full dataset balance")
print(value_counts)

# Convert the "outcome" column to numerical values
df['outcome'], label_strings = pd.factorize(df['outcome'])

# count the number of occurrences of each value and compute the percentage

# Split the dataframe into training and testing sets
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

train = train_df.drop(['outcome'], axis=1)
test = test_df.drop(['outcome'], axis=1)

# Normalize the input features
scaler = StandardScaler()

train_X = scaler.fit_transform(train)
train_y = train_df['outcome'].values
test_X = scaler.transform(test)
test_y = test_df['outcome'].values

# Build a neural network model using TensorFlow
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(512,)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(6, activation='softmax')
])

# Compile the model with appropriate loss function and optimizer
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model on the training set
model.fit(train_X, train_y, epochs=10, batch_size=32, validation_split=0.2)

# Evaluate the model on the testing set
test_loss, test_acc = model.evaluate(test_X, test_y, verbose=2)
print('\nTest accuracy:', test_acc)

# assuming `model` is your trained Keras model and `test_X` is your test input data
predictions = model.predict(test_X)

# get the index of the max value in each row
predicted_labels = predictions.argmax(axis=1)

# assuming `predicted_labels` is your 1D array of predicted integer labels
predicted_strings = [label_strings[label] for label in predicted_labels]

# convert the predictions to a pandas dataframe with one column
predictions_df = pd.DataFrame(predicted_strings, columns=['outcome'])

# count the number of occurrences of each value and compute the percentage
value_counts = predictions_df['outcome'].value_counts(normalize=True) * 100

# print the result
print("Prediction balance")
print(value_counts)
