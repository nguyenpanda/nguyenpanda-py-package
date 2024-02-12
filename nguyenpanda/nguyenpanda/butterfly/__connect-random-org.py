import requests

def get_random_numbers(api_key, num_numbers, min_range, max_range):
    # API endpoint URL
    url = "https://api.random.org/json-rpc/2/invoke"

    # Headers for the HTTP request
    headers = {"Content-Type": "application/json"}

    # Prepare the JSON-RPC request payload
    payload = {
        "jsonrpc": "2.0",
        "method": "generateGaussians",
        "params": {
            "apiKey": api_key,
            "n": num_numbers,
            "min": min_range,
            "max": max_range,
            "replacement": True,
            "base": 10
        },
        "id": 42  # You can use any integer here as the request ID
    }

    # Make the HTTP request to the Random.org API
    response = requests.post(url, headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        result = response.json()

        # Check if the response contains random numbers
        if "result" in result and "random" in result["result"]:
            return result["result"]["random"]["data"]
        else:
            print("Error in response:", result)
    else:
        print("HTTP request failed with status code:", response.status_code)

    return None


# Replace 'YOUR_API_KEY' with your actual Random.org API key
api_key = '1aaffe1a-32a9-4172-87e6-7086c5630637'
num_numbers = 5
min_range = 1
max_range = 100

# Get random numbers from the Random.org API
random_numbers = get_random_numbers(api_key, num_numbers, min_range, max_range)

# Print the random numbers
if random_numbers:
    print("Random Numbers:", random_numbers)
