import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# TODO: store credentials in a more secure way
class Notifier:
    # Handles messages to the users
    def __init__(self, user, article_list):
        self.user = user
        self.article_list = article_list
        self.message = MIMEMultipart('')
        self.from_address, self.password = self.get_credentials()
        self.to_address = self.user.email
        self.message['From'] = self.from_address
        self.message['To'] = self.to_address
        self.content = self.get_email_content()
        self.message.attach(self.content)
        self.mail = smtplib.SMTP('smtp.gmail.com', 587)
        self.mail.ehlo()
        self.mail.starttls()
        self.mail.login(self.from_address, 'Interview@Humanz')

    def send_email(self):
        # Sends the email
        self.mail.sendmail(self.from_address, self.to_address, self.content)
        self.mail.close()

    def get_credentials(self):
        # Gets credentials from an external file
        f = open('credentials.txt', 'r')
        credentials = f.read()
        credentials = credentials.split('\n')
        from_address = credentials[0]
        password = credentials[1]
        return from_address, password

    def get_email_content(self):
        # Creates email content
        email_text_content = ''
        email_text_content += 'Hey {}, \n'.format(self.user.name)
        email_text_content += 'Here\'s the news that\'s right for you: \n\n'
        for idx, article in enumerate(self.article_list):
            email_text_content += '{} \n'.format(article[1])
            email_text_content += '{} \n'.format(article[4])
            email_text_content += '{} \n'.format(article[2])
            email_text_content += '\n'

        return email_text_content
