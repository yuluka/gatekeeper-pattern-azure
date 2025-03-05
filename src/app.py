from fastapi import FastAPI, Request, HTTPException, Depends
from pydantic import BaseModel

app = FastAPI()

API_GATEKEEPER_KEY = "5349de7f2de547568c5ca7ef26b28c9c"  

class InputData(BaseModel):
    input: str

async def verify_apim_key(request: Request):
    api_key = request.headers.get("Ocp-Apim-Subscription-Key")
    if api_key != API_GATEKEEPER_KEY:
        raise HTTPException(status_code=403, detail="Access forbidden: Only APIM is allowed")

@app.get("/", dependencies=[Depends(verify_apim_key)])
def read_root():
    return {"message": "¡Hola, la API por acá!"}

@app.get("/items/{item_id}", dependencies=[Depends(verify_apim_key)])
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/sensitive-data/", dependencies=[Depends(verify_apim_key)])
def get_sensitive_data():
    return {"message": "Esto es información sensible"}

@app.post("/test-xss", dependencies=[Depends(verify_apim_key)])
def test_xss(data: InputData):
    return {"message": "Request received", "input": data.input}
