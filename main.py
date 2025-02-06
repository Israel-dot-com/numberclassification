from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import math
import requests
from typing import List, Union
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
    number: Union[str, float]
    error: bool = True

class NumberResponse(BaseModel):
    number: Union[int, float]
    is_prime: bool
    is_perfect: bool
    properties: List[str]
    digit_sum: int
    fun_fact: str

def is_prime(n: Union[int, float]) -> bool:
    if not float(n).is_integer() or n < 2:
        return False
    n = int(n)
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: Union[int, float]) -> bool:
    if not float(n).is_integer() or n < 1:
        return False
    n = int(n)
    return sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n: Union[int, float]) -> bool:
    if not float(n).is_integer():
        return False
    n = int(n)
    num_str = str(abs(n))
    power = len(num_str)
    try:
        return sum(int(digit) ** power for digit in num_str) == abs(n)
    except OverflowError:
        return False

def get_digit_sum(n: Union[int, float]) -> int:
    return sum(int(digit) for digit in str(abs(int(n))))

def get_number_properties(n: Union[int, float]) -> List[str]:
    properties = []
    if is_armstrong(n):
        properties.append("armstrong")
    properties.append("odd" if int(n) % 2 else "even")
    return properties

async def get_fun_fact(n: Union[int, float]) -> str:
    try:
        response = requests.get(f"http://numbersapi.com/{(n)}/math", timeout=3)
        if response.status_code == 200:
            return response.text
    except:
        pass
    if is_armstrong(n):
        digits = list(str(abs(int(n))))
        power = len(digits)
        calculation = " + ".join(f"{d}^{power}" for d in digits)
        return f"{n} is an Armstrong number because {calculation} = {n}"
    return f"The number {n} is interesting in mathematics!"

@app.get("/api/classify-number", response_model=NumberResponse, responses={400: {"model": ErrorResponse}})
async def classify_number(number: str):
    try:
        num = float(number)
    except ValueError:
        raise HTTPException(status_code=400, detail={"number": number, "error": True})
    
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
