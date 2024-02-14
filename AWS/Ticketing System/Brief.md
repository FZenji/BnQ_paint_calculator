# Project Brief: ITSM/Ticketing System Integration with AWS

## Objective:

To develop a component of an IT Service Ticketing system that automates the classification and routing of support tickets. This system will leverage AWS services to manage ticket queues, improving the efficiency and responsiveness of IT support services.

## Scope:

Development of a Python application that listens to incoming webhooks from Microsoft Teams.

- Ticket Parsing: The application must extract essential information from the webhook or a front end developed by you, data, including title, description, and priority.
- AWS Integration: Utilize the Boto3 library to interact with AWS Simple Queue Service (SQS). Based on the ticket's priority, it should be sent to one of three predetermined SQS queues (e.g., High Priority, Medium Priority, Low Priority).
- Documentation: Provide clear documentation on how to set up the webhook in Microsoft Teams, deploy the Python application, and configure AWS services (IAM roles, SQS queues).

## Deliverables:

- Python application source code.
- Comprehensive documentation covering setup, deployment, and configuration.
- A report summarizing the project's approach, challenges encountered, and solutions implemented.
