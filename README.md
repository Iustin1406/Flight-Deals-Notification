# Flight Deals Notification

This project is designed to find the best flight deals available for the next 6 months and notify the user via SMS using the Twilio API. It leverages the Amadeus API to search for flights and the Sheety API to manage flight data stored in a Google Sheet.

## Features

- **Flight Data Management**: Uses Sheety API to fetch and manage flight data stored in Google Sheets.
- **Flight Search**: Uses Amadeus API to search for the cheapest flights from a specified home airport to various destinations.
- **Notifications**: Sends SMS notifications about the best flight deals found, using Twilio API.

## Prerequisites

- Python 3.6 or higher
- Twilio Account
- Amadeus API credentials
- Sheety API credentials
