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

## **Configuration**

### **Environment Files**  
Each component (broker, producer, consumer) has its own `.env` file. Update the following fields in each file:  
1. **Database configuration**: Specify the database credentials for the consumer,or leave the default values as they are.  
2. **Kafka broker address**: Replace with your IP address or `localhost`. You can find your public IP with:  
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

## **Setup**

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
## **Usage Guide**

### **1. The Website Interface**
- The **main website** is hosted on a front-end service built with Vue.js.
- **Access it via**: [http://localhost:5173](http://localhost:5173)
  - The site serves as the primary interface for interacting with the GPS coordinates management system.


### **2. Backend API (FastAPI)**
- The back-end API is powered by **FastAPI**, which handles business logic and communication with the database.
- **Access it via**: [http://localhost:8000](http://localhost:8000)
  - API documentation is available at [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI).


### **3. PostgreSQL Database**
- A **PostgreSQL** instance stores the GPS coordinates and related data.
- **Access it via**: 
  - Command-line:  
    ```bash
    psql -h localhost -U ekip -d coord_gps
    ```
  - Port: **5432**


### **4. Kafka and Kafka UI**
- **Kafka** is used for event streaming and messaging.
  - Ports:  
    - Broker accessible at **localhost:9094**
    - Internal listener for container communication at **localhost:9092**

- **Kafka UI** provides a user-friendly interface to manage Kafka clusters.
  - **Access it via**: [http://localhost:8080](http://localhost:8080)

---

## **How It Works**

1. **Producer**: Generates GPS data and sends it to Kafka.  
2. **Broker**: Acts as a central hub to distribute data between producers and the consumer.  
3. **Consumer**: Reads data from Kafka, stores it in the database, and updates the interactive map in real-time.  


