# Hate Speech Detection in Tweets

This Flask application is designed to detect hate speech in tweets from a specified Twitter/X account. The application fetches a set number of tweets from the user's timeline, classifies them using a pre-trained RoBERTa model, and displays the results on a web interface.

## Features

- **User Input**
  - Accepts a Twitter/X user handle to fetch tweets from the user's timeline.
- **Tweet Classification**
  - Classifies tweets as hate speech or not using a pre-trained RoBERTa model.
- **User Profile Display**
  - Shows user information, including name, followers, and metrics related to the hate speech detected in their tweets.
- **LIME Explainability**
  - Provides a visual explanation of the most frequently used hate words in the user's tweets using LIME (Local Interpretable Model-agnostic Explanations).
- **Web Interface**
  - Results are displayed on a web page styled with HTML and CSS.

## File Structure

- **app/forms.py**: Defines the forms used in the web application, including the input form for the Twitter/X user handle.
- **app/models.py**: Contains the application models.
- **app/views.py**: Handles the routing and rendering of HTML templates and the logic for fetching and processing tweets.
- **app/tweet-api.py**: Manages the interaction with the Twitter API, fetching tweets based on the specified user handle.
- **app/templates/**: Contains the HTML templates for the web pages.
- **app/static/css/**: Contains the CSS files for styling the web pages.

## How It Works

1. **Input**: The user provides a Twitter/X handle through the web interface.
2. **Fetch Tweets**: The application uses the Twitter API to fetch a specified number of recent tweets from the provided handle.
3. **Classification**: The fetched tweets are classified using a pre-trained RoBERTa model to determine if they contain hate speech.
4. **Display Results**: The results, including user information, metrics on hate speech, and a LIME-generated network of the most frequently used hate words, are displayed on the web page.

## Note

The fine-tuned model size is too large to be uploaded to Github, it was uploaded to hugging face website instead, please visit this link https://huggingface.co/Wahi3b/RoBERTa_Hate_Speech_Detection/tree/main for the model files, download all files, place them in a directory called roBERTa-model inside the /app directory.
**NB_Model**: Notebook that contains the code for training the NB model
**roBERTa_Model**: Notebook that contains the code for training the roBERTa model

## To run the application:

1. Clone the repository (git clone repository-url).
2. Create a Virtual Environment.
3. Install the required packages (pip install -r requirements.txt).
4. Run the application (flask run) in your terminal.
