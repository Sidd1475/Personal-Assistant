# AI-Powered Personal Assistant

## Overview
An AI-powered personal assistant built using n8n and Google Gemini. It interprets natural-language requests and uses integrated tools to perform productivity-related tasks.

## Features
- **Email Management:** Retrieve, search and send emails using Gmail.
- **Calendar Management:** Create and retrieve Google Calendar events.
- **Task Management:** Create, retrieve and delete tasks.
- **Notes Management:** Create, update and retrieve notes.
- **Expense Tracking:** Add expenses and retrieve expense records.
- **Web Search:** Search for information using Google Search.
- **Conversational Memory:** Maintain conversational context using Simple Memory.

## Tech Stack
- n8n – Workflow automation
- Google Gemini – LLM and AI Agent
- Webhooks – Request handling
- Gmail API – Email operations
- Google Calendar API – Calendar operations
- Google Sheets – Data storage, if used by the workflow

## Architecture
User Request → Webhook → AI Agent → Gemini Chat Model → Integrated Tools → Response

## Setup Instructions
1. Install or access an n8n instance.
2. Import the exported workflow JSON.
3. Configure Google Gemini credentials.
4. Configure the required Google service credentials.
5. Verify the webhook configuration.
6. Activate the workflow and test its functionality.

## Configuration
Document the required credentials, webhook URL, permissions and any configuration values.

## Usage Examples
- Retrieve my latest emails.
- Schedule a meeting for tomorrow.
- Add an expense of ₹500.
- Create a task for completing an assignment.
- Search for information about a particular topic.

## Screenshots
<img width="807" height="577" alt="image" src="https://github.com/user-attachments/assets/0cb96a22-9ed6-4f0d-9f31-39c5e19e3ecb" />
<img width="1917" height="822" alt="image" src="https://github.com/user-attachments/assets/0a3dc381-cafd-4b6e-8fc3-09498692b601" />
<img width="1868" height="835" alt="image" src="https://github.com/user-attachments/assets/315bf6cc-01d6-4f1e-a4d0-f64f92873616" />



## Limitations
- Requires valid API credentials.
- Functionality depends on external API availability and usage quotas.
- Some Google integrations require account permissions.

## Future Improvements
- Support for multiple users and configurable credentials.
- Better error handling and retry mechanisms.
- Email prioritization and automated daily summaries.
