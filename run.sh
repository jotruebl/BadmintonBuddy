#!/bin/bash

# Run the Typer app using the environment variables
python main.py --username "$USERNAME" --password "$PASSWORD" --cvv "$CVV_CODE" --email-sender-password "$SENDER_PASSWORD" --dry-run "$DRY_RUN"
