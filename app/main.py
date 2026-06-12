from fastapi import FastAPI

app = FastAPI(
    title="ContractIQ",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "ContractIQ API Running"
    }