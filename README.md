# ChatGPT API chat.py Ver 1.1

## This simple Python program takes OpenAI's API and allows you to interact with it through the command line. 

You have the option to set the model, max token limit, temperature (creativity in choices of words), text stream, sessions, and embedding's.

## Project Structure
```
API_Chat
├── chat.py           # Main program
├── README.md
├── requirements.txt
├── sessions/
│   └──               # Where your chat sessions will be saved.
└── venv/             # You won't need to deal with any of these
    └── bin/
```

## Added in Version 1.1:

You now have the ability to track embedding's in your session's json file and also display the first 5 embedded values. These can be changed per prompt or in your chat.py file.

## Download:

### Step 1:

Start with <strong>git clone https://github.com/15stitch/chat.py.git</strong>.

Change directory (<strong>cd chat.py</strong>) into the working directory.

NOTE: You will need to have Python installed.

### Step 2: Create a virtual environment (highly recommended!)

Create your virtual environment with <strong>python -m venv venv</strong>

Activate your virtual environment: 

On MacOS & Linux: <strong>source venv/bin/activate</strong>

On Windows: <strong>venv\Scripts\activate</strong>

### Step 3: Install required packages

Run <strong>pip install -r requirements.txt</strong>


### Step 4: Setting OpenAI API Key

You will need an OpenAI API key to be able to interact with the API. Follow OpenAI's guide on how to make this (https://platform.openai.com/docs/quickstart).

Once you have your API Key made, you'll want to export it (while inside your virtual environment).

On MacOS and Linux: <strong>export OPENAI_API_KEY="YOUR_API_KEY_HERE"</strong>

On Windows: <strong>$env:OPENAI_API_KEY="YOUR_API_KEY_HERE"</strong>


### Step 5: Use chat.py!

The most basic way to communicate with the API now is in the form of <strong>python chat.py "Your prompt here"</strong>. See the rest of this README to use chat.py's added functionality.




## Extra functionality

### Sessions

You have the option to set sessions so you can speak with the API with it being able to recount previous messages. This can be helpful when you are debugging, having a conversation on a 
specific topic, etc.

Set your session by adding the <strong>session="SESSION_NAME"</strong> tag. By default, your conversation will be saved as "default". You can change this inside chat.py if you don't want 
to keep adding the session tag.

You can locate your session files in API_Chat/sessions/ . The files will be saved as .json files.


### Text Stream

Text stream allows you to see the text generate per token rather than waiting for the API to finish it's full message before presenting it. Personally, I prefer seeing the streaming on,
but you can turn this off per prompt with <strong>stream=False</strong> in your prompt, or changing the default <strong>stream=True</strong> in the chat.py file. 


### Model Selection

By default, chat.py uses OpenAI's gpt-3.5-turbo model, but you can choose to change the model (provided the OpenAI plan you are using allows that certain model).

To change the model in the prompt, add the <strong>model="MODEL_NAME"</strong> tag. You can find the names of the models at https://platform.openai.com/docs/models.

If you'd like to default to a certain model besides 3.5-turbo, you can make the change in the chat.py file.


### Token Limit Control

OpenAI tracks pricing for users based on the amount of tokens used in both input and output. This means it can be very important to limit the amount of tokens you are using. 

By default, chat.py has a max token limit of 300 tokens which I've found to be plenty for most projects. If you'd like to raise or lower the limit, you can change it per prompt with the 
<strong>max_token=TOKEN_INT</strong> tag, or change the default in chat.py.


### Temperature Control

With AI models, temperature refers to the randomness or "creativity" of words used in your prompt. With OpenAI's models, the range is from 0 to 2 with 0 being very clear-cut and 
informative, and 2 being much more creative/unpredictable. By default, chat.py uses a temp of 1 which is a good balance between the two. You can change the default temperature in the 
chat.py file which will be the most reliable way to do it, but you can also try it per prompt using a feature I added that seems to work well from my tests.

If you want to change the temperature per prompt, I've added a feature where you can add the <strong>temp="TEMP_DESC"</strong>. Instead of adding a integer or float value like 1.3, you 
can add a description like "silly wording" or "scientific and informative". Try experimenting with this! It likely isn't perfect, so for total reliability change the value in chat.py.

### Tracking and Displaying Embedding

For embedding's, you have two variables you can change: <strong>show_embedding</strong> and <strong>track_embedding</strong>. <strong>show_embedding</strong> displays the first 5 embedded 
values in your live prompt response. <strong>track_embedding</strong> controls the tracking of embedding's in your session's json file. 

<strong>NOTE:</strong> If you have track_embedding turned off but show_embedding on, you will not be able to view the embedding data because chat.py is not prompting the API for them in 
the first place.


### Example usage

An example using all the tags would look something like this: <strong>python chat.py session="writing" model="gpt-4o" temp="slightly poetic" max_tokens=200 track_embedding=True show_embedding=False 
"Write me a story about a frog"</strong>











