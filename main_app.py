from dotenv import load_dotenv
import os
import uvicorn


if __name__ == "__main__":
    load_dotenv()
    PORT = int(os.getenv("BACKEND_PORT"))
    APP = "myapplication.app:app_instance"
    uvicorn.run(APP, host="0.0.0.0", port=PORT, reload=True)
