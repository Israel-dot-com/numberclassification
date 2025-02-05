# Number Classification API

This API classifies numbers based on various mathematical properties and provides random facts about them

## Features

- Checks if a number is prime
- Checks if a number is perfect
- Identifies Armstrong numbers
- Determines if a number is odd or even
- Calculates digit sum
- Provides fun mathematical facts

## API Endpoint

### GET `/api/classify-number/{number}`

Classifies a number and returns its properties.

#### Query Parameters

- `number` (required): The number to classify

#### Success Response (200 OK)

```json
{
    "number": 371,
    "is_prime": false,
    "is_perfect": false,
    "properties": ["armstrong", "odd"],
    "digit_sum": 11,
    "fun_fact": "371 is a narcissistic number."
}
```

#### Error Response (400 Bad Request)

```json
{
    "number": "alphabet",
    "error": true
}
```

## Local Development; Wanna test it out?

1. Clone the repository:
   ```bash
   git clone https://github.com/Israel-dot-com/number-classifier-api.git
   cd number-classifier-api
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the server:
   ```bash
   python main.py
   ```

The API will be available at `http://0.0.0.0:8000`.


## Technologies

- Python 3.8+
- FastAPI
- Uvicorn
- Pydantic
- Numbers API (for fun facts)

## License

MIT