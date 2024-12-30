# **GPS Tracker - Simulated Movement Tracking**

This project is an application that simulates movement and tracks it in real-time on an interactive map. Data is transmitted via Kafka, enabling a distributed and scalable architecture. Each component (Kafka broker, producer, consumer) operates independently and can be deployed separately.

---

## **Features**

- **Movement Simulation**:  
  - Multiple producers generate simulated GPS coordinates.  
  - You can launch one or both producers simultaneously.  

- **Real-Time Tracking**:  
  - An interactive map displays positions in real-time.  
  - Previous positions are connected by a path, while the latest position is marked with a distinct icon.  

- **Distributed Architecture**:  
  - Kafka ensures smooth data transmission between producers and the consumer.  
  - Components can run on different machines.

---

## **Prerequisites**

- Docker and Docker Compose installed.  
- Ensure port **9094** is open if running across multiple machines.  
- Proper configuration of `.env` files for each component.  

---

## **Setup and Usage**

### **1. Start the Kafka Broker**  
The Kafka broker acts as the central hub for transferring data between components. Run the following command:  
```bash
docker compose -f brokerKafka/docker-compose.yml up
```

### **2. Start the Producer**  
Producers generate GPS data and send it to the Kafka broker. You can launch one or both producers:  
- To start only `producer1`:  
  ```bash
  docker compose -f producer/docker-compose.yml up producer1
  ```  
- To start only `producer2`:  
  ```bash
  docker compose -f producer/docker-compose.yml up producer2
  ```  
- To start both producers:  
  ```bash
  docker compose -f producer/docker-compose.yml up
  ```

### **3. Start the Consumer**  
The consumer processes GPS data from Kafka and displays it on the map. Run the following command:  
```bash
docker compose -f consumer/docker-compose.yml up
```

---

## **Configuration**

### **Environment Files**  
Each component (broker, producer, consumer) has its own `.env` file. Update the following fields in each file:  
1. **Database configuration**: Specify the database credentials for the consumer.  
2. **Kafka broker address**: Replace with your public IP address or `localhost`. You can find your public IP with:  
   ```bash
   ifconfig
   ```

### **Network Setup**  
If you are running components on different machines:  
- Ensure the Kafka broker is reachable over the network.  
- Open port **9094** on the machine hosting Kafka.  

### **Dependency Notes**  
- The producer and consumer **must** connect to the Kafka broker to function.  
- The broker, producer, and consumer can run on separate machines for flexibility.  

---

## **How It Works**

1. **Producer**: Generates GPS data and sends it to Kafka.  
2. **Broker**: Acts as a central hub to distribute data between producers and the consumer.  
3. **Consumer**: Reads data from Kafka, stores it in the database, and updates the interactive map in real-time.  
