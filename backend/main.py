import uvicorn

if __name__ == "__main__":
    uvicorn.run("src.api:api", host="localhost", port=9061, reload=True)