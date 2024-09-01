# Pre-Production Email Testing - Instructions & Configuration

## Overview
This project provides an email service designed to act as an email plugin module. Developed in Python, this service is tailored for pre-production testing, ensuring that email notifications are correctly formatted, sent, and received before deployment. The service is designed to be implemented within a microserive based application architecture, making it easily integrable and scalable within any application ecosystem requiring email notification capabilities.

## Email Module Features
- **Email Template Engine**: Create, edit, and manage email templates with dynamic placeholders.
- **Pre-Production Testing**: Test email sending capabilities in a sandbox environment to ensure reliability and correctness.
- **Integration Ready**: Designed as a plug-and-play module for existing notification systems using Kakfa based system messaging.
- **Customizable Settings**: Configure SMTP settings, email content, and more through a user-friendly interface.

## Email Infrastructure
The email infrastructure is designed to ensure reliable and correct email delivery in a pre-production environment. It includes the following components:

- **Mail Submission Agent (MSA)**: Acts as a liaison between the Mail Transfer Agent (MTA) and the Mail User Agent (MUA) to guarantee that emails are proofread in a sandbox before being sent.
- **Mail Transfer Agent (MTA)**: Manages the actual email sending process. The system is set up to mimic email delivery without really sending emails, ensuring that any potential problems are found and fixed.

## Event-Driven Architecture with Kafka
This email service leverages a Kafka-based event-driven architecture to handle email notifications efficiently and reliably. Kafka is used as the backbone for event streaming, ensuring that email events are processed asynchronously and at scale.

### Key Components:
- **Kafka Producer**: The application emits email-related events (e.g., user sign-up, purchase completed) to Kafka topics.
- **Kafka Broker**: Kafka brokers manage the storage and retrieval of event data, ensuring high throughput and fault tolerance.
- **Kafka Consumer**: The email service acts as a Kafka consumer, listening to relevant topics for email events. When an event is received, the service processes the event and sends the corresponding email.

### Workflow:
1. **Event Generation**: An event is generated when a specific action occurs in the application (e.g., a user signs up).
2. **Event Emission**: User management system for application emits the event to a Kafka topic.
3. **Event Processing**: The email service, subscribed to corresponding Kafka topic, receives the event.
4. **Email Sending**: The email service formats the email using user defined templates and sends it using the configured MTA.
5. **Delivery Confirmation**: The MTA delivers the email to the recipient's mail server, and the email service logs the delivery status.

This architecture ensures that the email service is decoupled from the main application logic, allowing for independent scaling and maintenance. It also provides reliability through Kafka's fault-tolerant design, ensuring that no email events are lost.


## Local Configuration & Setup
1. **Clone the Repository and Navigate to Root of Application**
   ```
   git clone git@github.com:hallsamir14/Kafka_Email_Service.git
   ```
   ```
   cd Kafka_Email_Service/
   ```
2. **Enable Development Scripts to be Executable**
   ```
   chmod +x devops_scripts/*.sh
   ```
3. **Start Application Dependencies Using Docker Compose**
   - Ensure Docker and Docker Compose are installed on your local machine.
   - Docker Compose facilitates dependencies for application so simulate fundmaental mechansims. These depedences come in the form of services and include:MySQL Database (Mock Database), Kafka Server, Kafka Producer (Mock Producer Interface) Zookeeper (Depdendecny for Kafka), 
     ```
     docker-compose up --build -d
     ```
     ### or
     ```
     devops_scripts/build_dockerCompose.sh
     ```
4. **Run App**
   - Execute the main Python file to start the email service:
     ```
     python main.py
     ```
