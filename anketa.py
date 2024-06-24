import telebot
from telebot import types
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

bot = telebot.TeleBot('')

def send_email(subject, body, to_email):
    from_email = ""
    from_password = ""
    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, from_password)
    text = message.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()

@bot.message_handler(commands=['start'])
def welcome(message):
    msg = bot.send_message(message.chat.id, "Введите ваш вопрос:")
    bot.register_next_step_handler(msg, process_question_step)

def process_question_step(message):
    question = message.text
    msg = bot.send_message(message.chat.id, "Введите ваш телефон:")
    bot.register_next_step_handler(msg, process_phone_step, question)

def process_phone_step(message, question):
    phone = message.text
    msg = bot.send_message(message.chat.id, "Введите ваш e-mail:")
    bot.register_next_step_handler(msg, process_email_step, question, phone)

def process_email_step(message, question, phone):
    email = message.text
    subject = "Новая анкета от пользователя"
    body = f"Вопрос: {question}\nТелефон: {phone}\nE-mail: {email}"
    send_email(subject, body, " ")
    bot.send_message(message.chat.id, "Ваша анкета отправлена. Спасибо!")

bot.polling(none_stop=True)
