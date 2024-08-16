import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from ai_web_app.main import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host=app.config['server']['host'],
        port=app.config['server']['port'],
        debug=app.config['app']['debug']
    )