import boto3
import os

# Initialize the SES client
ses = boto3.client('ses', region_name='us-east-1')  # Update region if needed

# Email parameters
sender_email = "james.c.sherman.jr@gmail.com"
recipient_email = "jcsjr0014@gmail.com"  # Can be a comma-separated string for multiple
subject = "AWS Sent Email Test"
print('set variables')

def lambda_handler(event, context):
    print('enter lambda function')
    # News summary content from prior Lambda step
    #summary = event.get("summary", "No summary content provided.")
    summary = 'Hello World'
    
    # Construct email body
    body_html = f"""
    <html>
    <head></head>
    <body>
      <h2>Today's Summary</h2>
      <p>{summary}</p>
    </body>
    </html>
    """
    
    try:
        print("attempting to send emial")
        response = ses.send_email(
            Source=sender_email,
            Destination={
                'ToAddresses': [recipient_email]
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