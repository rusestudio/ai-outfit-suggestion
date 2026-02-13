# About this branch

1. clothes_data
   - this folder have clothes data type and material data that were crawl from website
   - refer src folder clothes_data_crawl.py
   
3. database-fastapi-html
   - this folder have sub folder of templates with user.html
   - template sub folder is must to use jinjatemplates
   - this folder also have dummy_database_model as well as main.py
   - here we are trying  to send the data that were saved in database to user.html
   - which later user.html will be the page that user can see the result of clothes recommendation
   
4. generated_img_data
   - this is the folder that the generated img data will be store
   - refer src folder gemini_suggest_dummy.py
   - later this data might be save in database
   
5. html-input-to-fastapi-database
   - this folder have sub folder of templates with index.html
   - template sub folder is must to use jinjatemplates
   - this folder also have main.py
   - here we are trying to get the input data from user in index.html and send it to database through fastapi
   - the dummy data here is login data

6. src
   - this folder contains
     1. clothes_data_crawl.py
        - here is the part where we crawl the clothes data from websites.
     2. data_to_be_prompt.py
        - here is where all the data that will be send to llm model prompt
          where it will be called from database
     3. llm_model_suggest.py
        - here is the part where we send the weather,clothes,user info to llm model
          to get clothes suggestion and also images prompt.
        - due to no budget project we use different llm model to generate images.
        - the images the will be saved at generated_img_data folder.
     4. prompt.py
        - here is where the prompts is build for clothes suggestion and also
        - for image to be generate

## Setup and Run

1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variables:
   - `API_KEY_WEATHER`: OpenWeatherMap API key (get from https://openweathermap.org/api)
   - `API_KEY`: Google Gemini API key
3. Run the server: `uvicorn main:app --reload`
4. Open http://localhost:8000 in browser.

Note: Image generation is now free using Puter.js (user-pays model), no Stability API key needed.
Note: Gemini API has free tier limits. If you hit quota, wait for reset or upgrade your plan at https://ai.google.dev.
