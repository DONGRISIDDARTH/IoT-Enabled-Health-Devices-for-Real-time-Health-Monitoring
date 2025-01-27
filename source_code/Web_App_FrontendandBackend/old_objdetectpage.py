import streamlit as st
import pandas as pd
from localization_algorithm import predict_location

# Load the CSV file
@st.cache_data()
def load_data():
    return pd.read_csv("all_readers_data.csv")

# Define the number of rows and columns for the room zones
num_zone_rows = 4
num_zone_cols = 4

# Define the default grey color
default_color = "#CCCCCC"

# Add the main content to the main area
st.title("Object tracking with RFID")

# Define the colors for each zone
zone_colors = [default_color] * (num_zone_rows * num_zone_cols)

# Define the initial room title
room_title = st.header("The object is found in Room X")

# Define the callback function to update the room title and display RSSI data
def update_room_title(tag_id):
    global zone_colors
    
    room_number = tag_id // 1000
    room_title.header(f"The object is found in Room {room_number}")
    df = load_data()
    tag_data = df[df['tag_id'] == tag_id]
    if not tag_data.empty:
        rssi_data = tag_data[['rssi_1', 'rssi_2', 'rssi_3']].values[0]
        predicted_location = predict_location(rssi_data)
        
        # Change color of the predicted zone to red
        if predicted_location != 0:
            predicted_zone = predicted_location
            zone_colors[predicted_zone - 1] = "green"  # Change color of new predicted zone
            room_title.markdown(f"<h2 style='color: white;'>The object is found in Room {room_number}</h2>", unsafe_allow_html=True)
            st.write("The area of the room where the object is found:")
        else:
            # Reset color and update room title if object is not detected
            room_title.markdown(f"<h2 style='color: red;'>The object is not found anywhere</h2>", unsafe_allow_html=True)
            zone_colors = [default_color] * (num_zone_rows * num_zone_cols)
        
# Add buttons to the sidebar
st.sidebar.title("Tags")

# Define the tag numbers according to the specified scheme
tag_numbers = [
    range(1001, 1004),  # Tags 1001 to 1003
    range(2001, 2005),  # Tags 2001 to 2004
    range(3001, 3004),  # Tags 3001 to 3003
    range(4001, 4005),  # Tags 4001 to 4004
    range(5001, 5005),  # Tags 5001 to 5004
    range(6001, 6003),  # Tags 6001 to 6002
    range(7001, 7004)   # Tags 7000 to 7002
]

# Listen for button clicks on the tag buttons and update the room title and display RSSI data
for tag_range in tag_numbers:
    for tag_id in tag_range:
        if st.sidebar.button(f"Tag {tag_id}"):
            update_room_title(tag_id)

# Define the size of each zone in the grid
zone_size = 100  # Adjust as needed

# Create a container for the zones
with st.container():
    # Create a grid layout using Streamlit columns
    for i in range(num_zone_rows):
        cols = st.columns(num_zone_cols)
        for j in range(num_zone_cols):
            index = i * num_zone_cols + j
            with cols[j]:
                st.write(f"Zone {index + 1}")
                zone_color = zone_colors[index]
                st.markdown(f'<div style="background-color: {zone_color}; width: {zone_size}px; height: {zone_size}px; padding: 20px; text-align: center; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">', unsafe_allow_html=True)
