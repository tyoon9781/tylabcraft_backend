from dotenv import load_dotenv
import os
import uvicorn


if __name__ == "__main__":
    load_dotenv()
    PORT = int(os.getenv("DEV_BACKEND_PORT"))
    uvicorn.run("myapplication.app:app_instance", host="0.0.0.0", port=PORT, reload=True)
