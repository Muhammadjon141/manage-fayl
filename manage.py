import sys
import subprocess

def runserver():
    """ FastAPI serverini ishga tushurish. """
    print("runed succesfully")
    subprocess.run(["uvicorn", "app:app", "--reload"])

def main():
    if len(sys.argv) < 2:
        print("Usage: manage.py [command]")
        print("Commands: runserver, makemigrations, migrate")
        sys.exit(1)
    
    command = sys.argv[1]

    if command == "runserver":
        runserver()
    else:
        print("Unknown command:", command)
        sys.exit(1)

if __name__ == "main":
    main()