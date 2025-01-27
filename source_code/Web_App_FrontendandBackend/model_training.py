#Training the Machine Learning Model with past RFID data (dummy)

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Generate dummy data
num_samples = 1000
X = np.random.randint(50, 101, size=(num_samples, 3))  # Input: Three RSSI values
y = np.random.randint(1, 16, size=num_samples)         

# Build the neural network
model = Sequential([
    Dense(64, activation='relu', input_shape=(3,)),
    Dense(64, activation='relu'),
    Dense(16, activation='softmax')
])

# Compile the model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
model.fit(X, y, epochs=100, batch_size=32, validation_split=0.2)

# Save the weights to a file
model.save_weights('model_weights.h5')

# Evaluate the model
loss, accuracy = model.evaluate(X, y)
print("Accuracy:", accuracy)

num_test_samples = 10
X_test = np.random.randint(50, 101, size=(num_test_samples, 3))  # Random test samples between 50 and 100

# Predict using the trained model
predictions = model.predict(X_test)

# Print corresponding output
for i in range(num_test_samples):
    print("Input:", X_test[i])
    predicted_class = np.argmax(predictions[i])
    print("Predicted class:", predicted_class)
    print()