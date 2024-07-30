# Text to Game API

This Text to Game API generates images based on text prompts using Celery and Stability AI's text-to-image generation API.
It allows you to submit text prompts for image generation and retrieve the generated images.

## Setup Instructions

1. Clone the repository:
   
git clone <repository_url>
cd Text_To_Game

2.Create and activate a virtual environment

python3 -m venv venv
source venv/bin/activate

3. Install dependencies
   
pip install -r requirements.txt

4. Run database migrations
   
python manage.py migrate

5. Start the Redis server:

redis-server

6. Start the Celery worker:

celery -A your_project_name worker --loglevel=info

7. Run the Django development server:

python manage.py runserver

8. Generate images by hitting the API:

http://127.0.0.1:8000/image_generator/generate-images/

## API Endpoints

#### Generate Images
**URL:** /image_generator/generate-images/
**Method:** GET
**Description:** Generate images based on predefined text prompts.
**Response:** JSON array representing the list of generated images.
