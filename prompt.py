import re

#create prompt
def build_prompt(weather_data, clothes_data, user_input):
        #you are age, sex, height, body weight. 
        # //to be change based on user login data
        prompt = f"""
        You are a fashion assistant
        
          Current weather conditions:
          - Temperature: {weather_data.get('temperature', 'unknown')}°C
          - Wind: {weather_data.get('wind', 'unknown')}
          - Rain: {weather_data.get('rain', 'unknown')}%
          - Humidity: {weather_data.get('humidity', 'unknown')}%


        Available clothing options include the following types:
        {', '.join(clothes_data['types'])}

        and the following materials:
        {', '.join(clothes_data['materials'])}


               Destination:
          {user_input['destination']}

          Date:
          {user_input['when']}

          Environment:
          {user_input['environment']}


        Please suggest 3 outfits suitable for the conditions and location.
        for each outfit, provide:
        -suggestions materials,types, and colors in 3 points
        -simple explain why it fits the weather and location in one sentence
        -**Image Prompt:** "a short prompt for an image generation model to draw the outfit."

        Respond in clear text.
        """

        return prompt


#def return image prompt only
def image_prompt(result):
     #get only image prompt
     imageprompts = re.findall(r'\*\*Image Prompt:\*\*\s*"([^"]+)"', result)
    
    #fill  prompt
     throwback = "fashion outfit suitable for the current weather and location"
     while len(imageprompts) < 3:
        imageprompts.append(throwback)
    
     return imageprompts[:3]


if __name__ == "__main__":
     image_prompt()