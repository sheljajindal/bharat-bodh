import openpyxl
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load the workbook and select the sheet
path = "clients.xlsx"
openFile = openpyxl.load_workbook(path)
sheet = openFile['clients']
print(sheet)
mail_list = []
amount = []
name = []

# Loop through the rows and collect client information
for row in sheet.iter_rows(min_row=2, values_only=True):
    client, email, _, paid, count_amount = row
    if paid == 'No':
        mail_list.append(email) 
        amount.append(count_amount)
        name.append(client)

# Email credentials and SMTP setup
email = 'jnuipcon@gmail.com' 
password = '18IP!@24#$' 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(email, password)

# Send emails to clients who haven't paid
for mail_to in mail_list:
    find_des = mail_list.index(mail_to)
    clientName = name[find_des]
    subject = f'{clientName}, you have a new email'
    message = f'Dear {clientName}, \n' \
              f'We inform you that you owe ${amount[find_des]}. \n' \
              '\nBest Regards'

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = mail_to
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    
    text = msg.as_string()
    print(f'Sending email to {clientName}...')
    server.sendmail(email, mail_to, text)

# Close the server
server.quit()
print('Process is finished!')
time.sleep(10)
