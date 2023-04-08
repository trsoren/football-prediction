import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from keras import regularizers

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

# Define the neural network model
def create_model():
    model = keras.Sequential([
        keras.layers.Dense(64, activation='relu', input_shape=(504,), kernel_regularizer=regularizers.l2(0.001)), # TODO: change this 512
        keras.layers.Dropout(0.5),
        keras.layers.Dense(64, activation='relu', kernel_regularizer=regularizers.l2(0.001)),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(6, activation='softmax')
    ])
    return model

# Set the initial learning rate
initial_learning_rate = 0.01

# Define the learning rate schedule
lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
    initial_learning_rate,
    decay_steps=2, # decrease the learning rate by factor of 2 every 5 epochs
    decay_rate=0.5
)

# Define early stopping to prevent overfitting
early_stopping = keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

# Define a function to calculate the UAR
def uar(y_true, y_pred):
    """
    Unweighted Average Recall (UAR) metric
    """
    true_positives = tf.math.count_nonzero(tf.math.logical_and(tf.math.equal(y_true, 1), tf.math.equal(tf.math.round(y_pred), 1)), axis=0)
    true_negatives = tf.math.count_nonzero(tf.math.logical_and(tf.math.equal(y_true, 0), tf.math.equal(tf.math.round(y_pred), 0)), axis=0)
    false_positives = tf.math.count_nonzero(tf.math.logical_and(tf.math.equal(y_true, 0), tf.math.equal(tf.math.round(y_pred), 1)), axis=0)
    false_negatives = tf.math.count_nonzero(tf.math.logical_and(tf.math.equal(y_true, 1), tf.math.equal(tf.math.round(y_pred), 0)), axis=0)
    
    recall = true_positives / (true_positives + false_negatives)
    uar = tf.reduce_mean(recall)
    return uar

kfold = KFold(n_splits=5, shuffle=True, random_state=42)
scores = []

for fold_idx, (train_idx, val_idx) in enumerate(kfold.split(X_train, y_train)):
    print(f"Fold {fold_idx+1}:")
    X_fold_train, y_fold_train = X_train[train_idx], y_train[train_idx]
    X_fold_val, y_fold_val = X_train[val_idx], y_train[val_idx]

    # Build and compile the model for the current fold
    model = create_model()
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=lr_schedule), 
                  loss='sparse_categorical_crossentropy', 
                  metrics=[uar])

    # Train the model on the current fold's training set
    history = model.fit(X_fold_train, y_fold_train, epochs=50, batch_size=32, validation_data=(X_fold_val, y_fold_val), callbacks=[early_stopping])

    # Evaluate the model on the current fold's validation set
    y_pred_fold_val = model.predict(X_fold_val)
    y_pred_fold_val_classes = np.argmax(y_pred_fold_val, axis=1)
    scores.append(uar(y_fold_val, y_pred_fold_val_classes))

# Compute the mean and standard deviation of the cross-validation scores
mean_score = np.mean(scores)
std_score = np.std(scores)
print(f"\nCross-validation scores: {mean_score:.3f} (+/- {std_score:.3f}) UAR")

# Assuming `model` is your trained Keras model and `X_test` is your test input data
y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)

# Compute the frequency of each class in the predicted labels
class_freq_pred = np.bincount(y_pred_classes, minlength=6)

# Normalize the class frequencies by the total number of predictions and multiply by 100
class_freq_pred_norm = class_freq_pred / len(y_pred_classes) * 100

# Compute the frequency of each class in the test dataset
class_freq_orig = np.bincount(y_test, minlength=6)

# Normalize the class frequencies by the total number of examples and multiply by 100
class_freq_orig_norm = class_freq_orig / len(y_test) * 100

# Print the results
print("Class frequencies in the predicted labels:\n", class_freq_pred_norm)
print("Class frequencies in the test dataset:\n", class_freq_orig_norm)