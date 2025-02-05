from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import math
import requests
from typing import List
import os
from pydantic import BaseModel

app = FastAPI(title="Number Classification API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

class ErrorResponse(BaseModel):
    number: str
    error: bool = True

class NumberResponse(BaseModel):
    number: int
    is_prime: bool
    is_perfect: bool
    properties: List[str]
    digit_sum: int
    fun_fact: str

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    if n < 1:
        return False
    sum_factors = sum(i for i in range(1, n) if n % i == 0)
    return sum_factors == n

def is_armstrong(n: int) -> bool:
    num_str = str(n)
    power = len(num_str)
    try:
        return sum(int(digit) ** power for digit in num_str) == n
    except OverflowError:
        return False

def get_digit_sum(n: int) -> int:

    return sum(int(digit) for digit in str(n))
def get_number_properties(n: int) -> List[str]:
    properties = []
    if is_armstrong(n):
        properties.append("armstrong")
    properties.append("odd" if n % 2 else "even") 
    return properties
async def get_fun_fact(n: int) -> str:
    """Get a fun fact about the number from Numbers API."""
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math")
        if response.status_code == 200:
            return response.text
        else:
            if is_armstrong(n):
                digits = list(str(n))
                power = len(digits)
                calculation = " + ".join(f"{d}^{power}" for d in digits)
                return f"{n} is an Armstrong number because {calculation} = {n}"
            return f"The number {n} is interesting in mathematics!"
    except:
        return f"The number {n} is interesting in mathematics!"

@app.get("/api/classify-number", response_model=NumberResponse, responses={400: {"model": ErrorResponse}})
async def classify_number(number: str):
    """Classify a number and return its properties."""
    if any(c.isalpha() for c in number):
        raise HTTPException(
            status_code=400,
            detail={"number": "alphabet", "error": True}
        )
    
    try:
        if len(number) > 8:
            raise HTTPException(
                status_code=400,
                detail={"number": number, "error": True}
            )
            
        num = int(number)
        
        if num > 10**7:
            raise HTTPException(
                status_code=400,
                detail={"number": number, "error": True}
            )
            
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail={"number": number, "error": True}
        )
    
    properties = get_number_properties(num)
    fun_fact = await get_fun_fact(num)
    
    return {
        "number": num,
        "is_prime": is_prime(num),
        "is_perfect": is_perfect(num),
        "properties": properties,
        "digit_sum": get_digit_sum(num),
        "fun_fact": fun_fact
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))