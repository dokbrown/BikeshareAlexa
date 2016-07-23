# Bikeshare for Alexa
Works with Amazon Echo to tell me how many Capital Bikeshare bikes are nearby

By default, this uses a dictionary of my closest stops

## Reuse
You are welcome to reuse this code.

### Resources
You will need to get a (free) developer setup with Amazon:  
https://developer.amazon.com/home.html
and an AWS account (also free for I think a million calls a month)  
https://console.aws.amazon.com/console/home?region=us-east-1  
note that you must select the us-east-1 region for Alexa skills  

### Then to use the code:  
**Code:**  
* Change the station list in the getspeech() function to the list of stations and you want to query with your preferred name for each

**Lambda:**  
* Go to the AWS console and select "lambda"  
* Click "Create a Lambda function"  
* Skip selecting a blueprint by clicking next
* in "Configure Triggers", click in the box and select Alexa Skills Kit
* Name the function BikeshareAlexa, and add a description if you like
* Select "python" as runtime  
* Paste in the whole .py file  
* Under "Role", select lambda_basic_execution  
* you may want to turn up the timeout since we're hitting an API (I use 6 seconds)  
* Click next  

*Keep this open since you'll need the ARN from the top right shortly*

**Alexa Skill:**
* Go to developer.amazon.com and log in
* Click "alexa" on the top bar
* Click "add a new skill"
* For name, use "WhenIsMyBus"
* For invocation name use "when is my bus"
* Click next
* Paste the intent schema into the top box
* Paste the sample utterances into the bottom box
* Click save, it should build the model
* Click next.

*If you want to customize:*  
Change the list of stop IDs and route names to the ones that interest you.

That's it! Your echo should have the skill immediately. Just say:  
*Alexa, ask when is my bus*
