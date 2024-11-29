## Overview

This project provides an email service designed to act as an email plugin module. Developed in Python, this service is tailored for pre-production testing, ensuring that email notifications are correctly formatted, sent, and received before deployment. The service is designed to be implemented within a microservice based application architecture, making it easily integrable and scalable within any application ecosystem requiring email notification capabilities.

## Email Module Features

- **Email Template Engine**: Create, edit, and manage email templates with dynamic placeholders.
- **Pre-Production Testing**: Test email sending capabilities in a sandbox environment to ensure reliability and correctness.
- **Integration Ready**: Designed as a plug-and-play module for existing notification systems using Kakfa based system messaging.
- **Customizable Settings**: Configure SMTP settings, email content, and more through a user-friendly interface.

## Pre-Production Email Infrastructure

Email infrastructure is designed to ensure reliable and correct email delivery in a pre-production environment that can eventually be rolled out into a production enviornmnet  It includes the following components:

- **Mail Submission Agent (MSA)**: Acts as a liaison between the Mail Transfer Agent (MTA) and the Mail User Agent (MUA) to guarantee that emails are proofread in a sandbox before being sent.
- **Mail Transfer Agent (MTA)**: Manages the actual email sending process. The system is set up to mimic email delivery without really sending emails, ensuring that any potential problems are found and fixed.

## Event-Driven Architecture with Kafka

This email service leverages a Kafka-based event-driven architecture to handle email notifications efficiently and reliably. Kafka is used as the backbone for event streaming, ensuring that email events are processed asynchronously and at scale.

### Key Components:

- **Kafka Producer**: The application emits email-related events (e.g., user sign-up, purchase completed) to Kafka topics.
- **Kafka Broker**: Kafka brokers manage the storage and retrieval of event data, ensuring high throughput and fault tolerance.
- **Kafka Consumer**: The email service acts as a Kafka consumer, listening to relevant topics for email events. When an event is received, the service processes the event and sends the corresponding email.

### Application High-Level Flow:

1. **Event Generation**: An event is generated when a specific action occurs in the user application (e.g., a user signs up, application monitoring metric is met).
2. **Event Emission**: The user application emits an event, through a kafka producer, to a Kafka topic.
3. **Event Processing**: The email service, subscribed to corresponding Kafka topic, receives and processes the messge from the topic.
4. **Email Sending**: The email service formats the email using user defined templates and sends it using the configured MTA.

This architecture ensures that the email service is decoupled from the main application logic, allowing for independent scaling and maintenance. It also provides reliability through Kafka's fault-tolerant design, ensuring that no application events are lost.
## Source Code Modules
| Source code file name          | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| app/emailer.py (Incomplete) | Contains the ```emailer()``` class. Each instance of the emailer class represents an engine that sends emails. Each instance of the `emailer` class represents an engine responsible for sending emails. It uses SMTP settings to establish a connection to the SMTP server, formats the email content, and sends the email to the specified recipient. The class ensures that emails are sent reliably and logs the delivery status. |
| app/utils/database_connection | Contains the ```db_connect()``` class. Each instance of the db_connect class represesnts a connection to a database. |
|app/utils/smtp_connection.py | Contains the ```smtp_Settings()``` class. Each instance of the smtp_Settings class represents a loaded and managed SMTP config, which can be extracted from enviornmental variables or set as default values. The config is used to establish a connection to an SMTP server in which emails can be sent thorugh.
|app/utils/template_manager | Contains the ```TemplateManager``` class. Each instance of the TemplateManager class represents a managed configuration for rendering and styling email templates. Each instance of the `TemplateManager` class represents a manager responsible for rendering and styling email templates. It reads template files, applies advanced CSS styles for email compatibility, and renders templates with dynamic content to ensure consistent and professional email formatting. 
| app/kafka_consumer/consumer_config.py | Contains the ```Config()``` class.Loads kafka and logging configuration to be used by the ```consumer_processor()``` class, providing defaults and logging any unset config variables |
|app/kakfa_consumer/consumer_processor.py | Contains the ```consumer_processor``` class. A wrapper around kafka's ```consumer()```, providing core processing operations of messages being pulled off a topic. |
|app/kakfa_consumer/consumer_parser/parser.py | ...



## Local Environment Setup

1. **Clone the Repository and Navigate to Root of Application**
   ```
   git clone git@github.com:hallsamir14/Kafka_Email_Service.git
   ```
   ```
   cd Kafka_Email_Service/
   ```
2. **Enable Development Scripts to be Executable**
   ```
   chmod +x bootstrap_scripts/*.sh
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

## Unit Testing:

**Tests are made using pytests.**

1. **Install Pytest**
    ```
    pip install -U pytest
    ``` 


2. **Run Pytest**
    - In root of project directory
    ```
    pytest
    ``` 
All tests are in the "tests" folder. Pytest configurations are in `pytest.ini`
  - **Test Classes**
    - Test classes are implemented for organization purposes. They also allow fixtures containing objects to be passed to each test function.
    - When running pytest each test will be displayed with a path and test outcome
      - `tests/emailer_test.py::TestEmail::test_email PASSED`
      - `(test folder)/(test file)::Class::Function STATUS`
  - **Pytest Fixtures**
    - A fixture provides a defined, reliable and consistent context for the tests. We use fixtures here to pass the same data/objects to the other test functions.
- **Integration Test**: Integration test are in the "integration_tests" folder. They test components of the app that require some type of interfacing between each other (i.e. database API, kafka consumer, etc.)
  - Most will have simplified docker files that run necessary isolated components of the app. (E.g. mock database service)
  - In conftest.py the paths to the dockerfiles are added to the pytest command line options for organization and use across multiple files.
- **Robust Testing**: Every functioning module in the app has corresponding test associated unless said function is marked as private
