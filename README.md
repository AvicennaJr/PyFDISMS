# PyFDI SMS

A python wrapper for interacting with [FDI SMS API](https://fdisms.docs.apiary.io). The SDK provides a simple and convenient way to use the SMS API functionality including checking API health, retrieving current balance, sending messages, validating mobile numbers (MSISDNs), and more.

## Installation

To install this SDK, simply use pip:

```bash
pip install pyfdisms
```

## Getting Started

First, you need to import the SmsClient class from the SDK.

```python
from fdismsclient import SmsClient
```
Then, initialize the client with your API key and API secret. You can choose to use the sandbox environment for testing by setting the sandbox parameter to True (default value). When you're ready to use the production environment, set sandbox to False.

```python
client = SmsClient(api_key="your-api-key", api_secret="your-api-secret", sandbox=True)
```

## Available Methods

Here's a list of available methods in the SmsClient class.

### refresh()

Refreshes the API access token using the refresh token. No arguments required.

### check_health()

Checks the API health status. Returns a dictionary containing the health status data of the API.

### balance()

Retrieves the current credit balance from the API. Returns a dictionary containing the balance data.

### balance_on_date(date_string: str)

Retrieves the credit balance at any point in time. You need to provide a date string in the format "YYYY-MM-DD". Returns a dictionary containing the balance data for the specified date.

### send_single(msisdn: str, message: str, msg_ref: str, sender_id: str, callback_url: str)

Sends a message to a single MSISDN (mobile number). You need to provide the mobile number, the message content, and a unique reference for the message. Optionally, you can specify a sender ID and a callback URL for delivery reports. The method returns a dictionary containing the response from the API.

```python
response = client.send_single(
        msisdn="1234567890",
        message="Hello, world!",
        msg_ref="unique-message-ref",
        sender_id="YourCompany",
        callback_url="https://yourcompany.com/callback"
        )
```

### send_bulk(msisdn_list: List, message: str, msg_ref: str, sender_id: str, callback_url: str)

Sends a message to a list of MSISDNs. The arguments are similar to send_single, but you provide a list of mobile numbers instead of a single number.

```python
response = client.send_bulk(
        msisdn_list=["1234567890", "0987654321"],
        message="Hello, world!",
        msg_ref="unique-message-ref",
        sender_id="YourCompany",
        callback_url="https://yourcompany.com/callback"
        )
```

### get_stats()

Gets the status for mobile terminated (MT) and mobile originated (MO) messages for today. The method returns a dictionary containing the response from the API.

### get_stats_on_date(date_string: str)

Similar to get_stats, but for a specific date. You need to provide a date string in the format "YYYY-MM-DD".

### validate_msisdn(msisdn: str, country_code: str)

Checks whether an MSISDN is valid for a specific country. You need to provide a mobile number and a two-character ISO 3361-1 country code. The method returns a dictionary containing the response from the API.

### validate_msisdn_bulk(msisdn_list: List, country_code: str)

Similar to validate_msisdn, but for a list of mobile numbers.

## Error Handling

The SDK will return a value only when the status code is 200. Otherwise, it will raise an exception for its respective status code. The included status codes are 400 (Bad Request), 401 (Unauthorized), 403 (Forbidden), 404 (Not Found), 422 (Unprocessable Entity), 500 (Internal Server Error), and 503 (Service Unavailable).

Remember to handle these exceptions in your application to ensure it doesn't crash when an error occurs.

```python
try:
response = client.check_health()
    except Exception as e:
    print(f"An error occurred: {e}")

```

## Credits

🤷
