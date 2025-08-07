import boto3
import requests
import re
import ast
from openai import OpenAI
from datetime import date, timedelta, datetime
from bs4 import BeautifulSoup

# Initialize the SES client
ses = boto3.client('ses', region_name='us-east-1')  # Update region if needed
"""
YOU WILL NEED TO FILL THE BELOW VARIABLES TO MATCH YOUR USE CASE
"""
# Email parameters
senderEmail = "FILL ME IN" #make sure this same email is set for variable senderEmail in file terraform.tfvars 
recipientEmails = ["FILL ME IN", "FILL ME IN"]  # List of emails for sending to multiple sources. If using SES sandbox, these emails need to be verified in Amazon SES. AWS Console -> Amazon SES -> Configuration -> Identities
todayDate = date.today()
subject = "AI-Powered Sports News Feed for " + str(todayDate)

#Parameters for grabbing source data. This implementation uses the newsapi "Top-Headline" endpoint for certain sports related information from the previous day. https://newsapi.org/docs/endpoints/top-headlines
apiKey = "FILL ME IN"
keywords = ["sports"]
yesterdayDate = todayDate - timedelta(days=1)
newsSourceUrl = "https://newsapi.org/v2/top-headlines?country=us&category=sports&apiKey=" + apiKey

#Parameters for making the openai call. Please note you will likely need to update the "summarizeViaApi" function to match your needs
client = OpenAI(
    api_key = "FILL ME IN"
)

def lambdaHandler(event, context):
    print('enter lambda function')
    sourceData = extractNewsData(newsSourceUrl)
    summaries = summarizeViaAi(sourceData)
    sendEmail(summaries, senderEmail, recipientEmails)

def extractNewsData(url):
    rawData = requests.get(url)
    articles = rawData.json()['articles']
    print(yesterdayDate)
    dateFilteredData = [x for x in articles if datetime.strptime(x["publishedAt"], "%Y-%m-%dT%H:%M:%SZ").date() >= yesterdayDate] #we sometimes get some older articles. We are not interested in those
    urls = [x['url'] for x in dateFilteredData]
    titles = [x['title'] for x in dateFilteredData]
    data = []
    for i in range(len(urls)):
        url, title = urls[i], titles[i]
        print(url)
        try:
            response = requests.get(url, timeout=4)
        except Exception as e:
            continue
        if response.status_code == 200: #some sites do not allow external requets. We can only pull data from sites that allow us
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.findAll('p') #this will get only the paragraphs of the site
            text = re.sub(r"<a.*?</a>", "", str(text)) #let's remove some of those random links/ads to other sites
            data.append([title, url, text])
    return data

def summarizeViaAi(sourceData):
    print('entering ai code')
    summaries = []
    for data in sourceData:
        inp = [data[0].replace(",", ""), data[2]] #let's remove some commas to not confuse the model
        print(inp)
        message = [{"role": "system", "content": "You will help me summarize sports articles found online. You will receive a comma seperated list containing an article title and the text body from the article in html format. You need to create an altered title based on the given title and text body, and create a 2-6 sentence summary of the text body. Note that, since the article is webscraped in html format, you need to focus on pulling information from the article that pertain to sports. The output should be in a python list as such: [<new title>, <summary>]"},
                    {"role": "user", "content": str(inp)}]
        response = client.chat.completions.create(
            model = "o4-mini",
            messages = message
        )
        eval = ast.literal_eval(response.choices[0].message.content)
        summaries.append([eval[0], data[1], eval[1]])
        break
    return summaries
    
def sendEmail(summaries, senderEmail, recipientEmails):
    htmlString = ""
    for summary in summaries:
        htmlString += ("<h3>" + summary[0] + "</h3><p>" + summary[2] + "</p><p><a href=\"" + summary[1] + "\"target=\"_blank\"></a></p>")
    body_html = f"""
    <html>
    <head></head>
    <body>
      <h2>Today's Sports Summary</h2>
      {htmlString}
    </body>
    </html>
    """
    print(body_html)
    print(1/0)
    try:
        print("attempting to send emial")
        response = ses.send_email(
            Source=senderEmail,
            Destination={
                'ToAddresses': recipientEmails
            },
            Message={
                'Subject': {
                    'Data': subject
                },
                'Body': {
                    'Html': {
                        'Data': body_html
                    },
                    'Text': {
                        'Data': summary
                    }
                }
            }
        )
        print("email sent")
        return {
            'statusCode': 200,
            'body': f"Email sent! Message ID: {response['MessageId']}"
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
    

lambdaHandler("", "")