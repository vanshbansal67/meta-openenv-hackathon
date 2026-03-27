import uvicorn
from openenv.server import create_app
from envs.simulator import EmailTriageEnv

# Tumhara environment load karega
app = create_app(EmailTriageEnv)

def main():
    # Port 7860 Hugging Face ke liye standard hai
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()