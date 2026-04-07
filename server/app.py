import uvicorn
from openenv.server import create_app
from envs.simulator import EmailTriageEnv

app = create_app(EmailTriageEnv)

def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
