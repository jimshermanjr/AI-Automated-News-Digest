# AI-Automated-News-Digest
A simple automation that pulls news events from newsapi, summarizes and formats the information using openai api, and sends an email to a hardcoded recipient (must be verified in AWS if using sandbox environment)

The infrastrucutre is current deployable and functioning.

The python function is also working. We are successfully able to extract urls from relevant news articles (in this case, we are focusing on sports), parse the data from the urls using BeautifulSoup to gain article contents, pass these article contents into openAi model o4-mini to gain a unique title and summary, and format each summary into a correct html format. This would send emails correctly in AWS

All I need to do is package some of the 3rd party libaries (openAi, requests, bs4) locally so I can deploy to AWS
