import numpy as np
"""from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Load the model architecture
model = Sequential([
    Dense(64, activation='relu', input_shape=(3,)),
    Dense(64, activation='relu'),
    Dense(16, activation='softmax')
])

# Compile the model (this step is necessary even for inference)
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Load the saved weights
model.load_weights('model_weights.h5')"""

def predict_location(rssi_values):
    rssi_values = np.abs(rssi_values)
    # Ensure input shape is correct
    rssi_values = np.array(rssi_values).reshape(1, 3)
    
# Determine output based on probability
    if np.random.randint(0, 10) < 3:  # 30% probability
        predicted_location = 0
    else:
        predicted_location = np.random.randint(1, 16)  # Random number between 1 and 15
    
    # Return the predicted location
    return predicted_location
