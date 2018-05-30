from dotenv import load_dotenv

load_dotenv()
import app


maintenance_tracker = app.initialize_app()

if __name__ == '__main__':
    maintenance_tracker.run()
