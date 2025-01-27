# IoT-Enabled-Health-Devices-for-Real-time-Health-Monitoring

This project simulates the generation and transmission of real-time data using Cintiki NG. The system involves RFID tags, border gateways, edge, and fog computing, focusing on efficient data transfer using various protocols.

Key Technologies & Components:
RFID: Used for real-time data generation and identification.
Border Gateway: Facilitates communication between networks, enabling data transmission.
Edge and Fog Computing: Decentralized computing model for processing data closer to the source (edge) and reducing latency.
Protocols: Data transfer is handled by MQTT and CoAP, chosen based on specific conditions to ensure efficient communication.
IPv6: Used for communication between devices, especially for external or application-level data exchange.
REST API: Enables data exchange between devices within the same network.
Data Flow
RFID tags generate real-time data.
Edge Devices collect and process this data, sending it through the network using MQTT or CoAP protocols depending on the situation.
The data is transferred between devices using IPv6 when traveling to external applications.
REST APIs facilitate communication between devices on the same network for sending and receiving data.
