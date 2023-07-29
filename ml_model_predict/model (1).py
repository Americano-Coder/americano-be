# Import Modules

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Read CSV
for encoding in ['utf-8', 'latin-1', 'ISO-8859-1', 'cp1252']:
    try:
        df = pd.read_csv('db.csv', encoding=encoding)
        break
    except UnicodeDecodeError:
        continue

# Preprocess Data
df = df[df['Category'] == 'Social Life']
df['Date'] = range(1, len(df) + 1)

# Set to array
time, series = df['Date'].values, df['Amount'].values

# Get only 1500 data from the time & series
time, series = time[:1500], series[:1500]

# Window Func
# Example, Window_Size = 4
# [1, 3, 5, 2, 7, 1, 3] -> [1, 3, 5, 2][7], [3,5,2,7][1], etc.
def windowed_dataset(series, window_size, batch_size, shuffle_buffer):
    series = tf.expand_dims(series, axis=-1)
    ds = tf.data.Dataset.from_tensor_slices(series)
    ds = ds.window(window_size + 1, shift=1, drop_remainder=True)
    ds = ds.flat_map(lambda w: w.batch(window_size + 1))
    ds = ds.shuffle(shuffle_buffer)
    ds = ds.map(lambda w: (w[:-1], w[1:]))
    return ds.batch(batch_size).prefetch(1)

# Split Data
split_time= int(0.9 * len(series))
time_train= time[:split_time]
x_train= series[:split_time]
time_valid= time[split_time:]
x_valid= series[split_time:]

# Set Parameters
window_size= 32
batch_size= 32
shuffle_buffer_size= 3500

# Window the current series data
train_set=windowed_dataset(x_train, window_size, batch_size, shuffle_buffer_size)

# Machine Learning
class myCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        if logs.get('mae') < 4:
            self.model.stop_training = True

callbacks = myCallback()

model=tf.keras.models.Sequential([
    tf.keras.layers.LSTM(64, input_shape=[None, 1], return_sequences=True,),
    tf.keras.layers.LSTM(64),
    tf.keras.layers.Dense(60, activation="relu"),
    tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dense(1),
])

model.compile(loss=tf.keras.losses.Huber(),
                optimizer=tf.keras.optimizers.SGD(),
                metrics=["mae"],
                run_eagerly=True)

history = model.fit(train_set, epochs=10, callbacks=[callbacks])

# Post Machine Learning
def create_input_sequences_for_prediction(x_train, x_valid, split_time, window_size):
    input_sequences = []
    for j in range(len(x_train) - window_size, split_time + len(x_valid) - window_size):
        input_sequences.append(series[j:j+window_size])
    return np.array(input_sequences)

# Generate input sequences for prediction for x_valid
input_sequences_x_valid = create_input_sequences_for_prediction(x_train, x_valid, split_time, window_size)


# Make predictions for x_valid
predictions_x_valid = model.predict(input_sequences_x_valid)

# Plot the original data and predictions
plt.figure(figsize=(10, 6))
plt.plot(time_train, x_train, label='x_train', color='blue')
plt.plot(time_valid, predictions_x_valid, label='x_pred', color='red')
plt.xlabel('Time')
plt.ylabel('Total Expenses')
plt.title('Expense Prediction')
plt.legend()
plt.grid(True)
plt.show()
