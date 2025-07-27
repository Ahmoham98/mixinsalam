import os
import typer
import uvicorn

# Create a Typer application
cli = typer.Typer()

# Get the host and port from environment variables, with defaults
# LOCALHOST = os.getenv("HOST", "myapp.dev")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

def print_loaded_config():
    """
    Imports the Config object and prints the currently loaded settings.
    This function is called AFTER the environment has been set.
    """
    # We import Config here, inside the function, to make sure
    # it's loaded AFTER os.environ['APP_ENV'] is set.
    from configure import Config
    
    print("-" * 40)
    print(f"Environment:         {Config.APP_ENV}")
    print(f"Basalam Client ID:   {Config.BASALAM_CLIENT_ID}")
    print(f"Basalam Secret:      ...{Config.BASALAM_SECRET[:-4]}") # Print only last 4 chars for security
    print(f"Basalam Redirect URI: {Config.BASALAM_REDIRECT_URI}")
    print("-" * 40)


@cli.command()
def dev():
    """
    Runs the development server with auto-reload.
    Sets APP_ENV to 'development'.
    """
    print("🚀 Starting server in DEVELOPMENT mode...")
    # Set the environment variable for this run
    os.environ['APP_ENV'] = 'development'
    
    # 2. Print the loaded configuration
    print_loaded_config()

    # Use uvicorn.run to start the server programmatically
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
    


@cli.command()
def start():
    """
    Runs the production server.
    Sets APP_ENV to 'production'.
    """
    print("🚀 Starting server in PRODUCTION mode...")
    # Set the environment variable for this run
    os.environ['APP_ENV'] = 'production'
    
    # 2. Print the loaded configuration
    print_loaded_config()

    # Use uvicorn.run without auto-reload for production
    uvicorn.run("main:app", host=HOST, port=PORT, reload=False)
    


if __name__ == "__main__":
    cli()