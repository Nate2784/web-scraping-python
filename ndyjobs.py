import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

token='6398422086:AAHKh0tI1-9IOvKNrn4wwpXfiSNS2j9wizQ'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
url = 'https://www.ethiojobs.net/jobs-in-ethiopia/'
jobs = {}
sent_jobs = set()  

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the jobs listing Bot!")

async def getjobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        count = int(update.message.text.replace('/getjobs ',''));
    except:
        await update.message.reply_text("message should follow: /getjobs <count>");

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    job_postings = soup.find_all('div', class_='single_listing')

    for posting in job_postings:
        job_title = posting.find('a').text.strip()
        link = posting.find('a').get('href')
        company = posting.find('p', class_='no-margin').text.strip()
        date = posting.find('span', class_='pull-right').text.strip()
        
        jobs[job_title] = {
            'Company': company,
            'Date': date,
            'Link': link
        }
    
    message = ""
    sent_count = 0
    for job_title, details in jobs.items():
        if job_title in sent_jobs:  
            continue
        message = f'Job Title:  {job_title}\nCompany Name:  {details['Company']}\nDate of post:  {details['Date']}\nFor more info:\n {details['Link']}\n\n'
        await update.message.reply_text(message);
        sent_jobs.add(job_title) 
        sent_count += 1
        if sent_count == count: 
            break
    if sent_count < count:
        await update.message.reply_text("There's currently no more job listing. Please try again later.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(token).build()
    
    start_handler = CommandHandler('start', start)
    getjobs_handler = CommandHandler('getjobs', getjobs)
    
    application.add_handler(start_handler)
    application.add_handler(getjobs_handler)
    
    application.run_polling()
