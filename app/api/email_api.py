# backend_flask/app/web/email_view.py

from flask import Blueprint, render_template, request, redirect, flash
import smtplib
from email.mime.text import MIMEText
from config import Config
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

webmail = Blueprint("mail", __name__)

@webmail.route("/formulario-email", methods=["GET"])
def formulario_email():
    return render_template("enviar_email.html")

@webmail.route("/enviar-email", methods=["POST"])
def enviar_email():
    destinatario = request.form["destinatario"]
    assunto = request.form["assunto"]
    mensagem = request.form["mensagem"]

    # Construção da mensagem
    msg = MIMEText(mensagem)
    msg["Subject"] = assunto
    msg["From"] = Config.EMAIL_REMETENTE
    msg["To"] = destinatario

    try:
        # Ligação SMTP
        with smtplib.SMTP_SSL(Config.SMTP_SERVIDOR, Config.SMTP_PORTA) as server:
            server.login(Config.EMAIL_REMETENTE, Config.EMAIL_PASSWORD)
            server.send_message(msg)
        flash("Email enviado com sucesso!")
    except Exception as e:
        flash(f"Erro ao enviar email: {e}")
    
    return redirect("/formulario-email")

@webmail.route("/enviar-email/novo-usuario", methods=["POST"])
def enviar_email_novo_usuario(email):
    destinatario = str(email)
    assunto = "Seja bem vindo a nossa loja"
    mensagem = "Bem vindo, a sua privacidade é nosso maior interesse"

    # Construção da mensagem
    msg = MIMEText(mensagem)
    msg["Subject"] = assunto
    msg["From"] = Config.EMAIL_REMETENTE
    msg["To"] = destinatario

    try:
        # Ligação SMTP
        with smtplib.SMTP_SSL(Config.SMTP_SERVIDOR, Config.SMTP_PORTA) as server:
            server.login(Config.EMAIL_REMETENTE, Config.EMAIL_PASSWORD)
            server.send_message(msg)
        flash("Email enviado com sucesso!")
    except Exception as e:
        flash(f"Erro ao enviar email: {e}")

'''

@webmail.route("/enviar-email/novo-usuario", methods=["POST"])
def enviar_email_novo_usuario(*email):
    destinatario = 'bentobsh@gmail.com'
    assunto = "Seja bem vindo a nossa loja"
    mensagem = "Bem vindo, a sua privacidade é nosso maior interesse"

    # Construção da mensagem
    msg = MIMEText(mensagem)
    msg = MIMEMultipart(mensagem)
    msg["Subject"] = assunto
    msg["From"] = Config.EMAIL_REMETENTE
    msg["To"] = destinatario

    # Create the plain-text and HTML version of your message
    text = """\
    Hi,
    How are you?
    Real Python has many great tutorials:
    www.realpython.com"""
    html = """\
    <html>
    <body>
        <p>Hi,<br>
        How are you?<br>
        <a href="http://www.realpython.com">Real Python</a> 
        has many great tutorials.
        </p>
    </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    msg.attach(part1)
    msg.attach(part2)

    try:
            # Ligação SMTP
            with smtplib.SMTP_SSL(Config.SMTP_SERVIDOR, Config.SMTP_PORTA) as server:
                server.login(Config.EMAIL_REMETENTE, Config.EMAIL_PASSWORD)
                server.send_message(msg)
            flash("Email enviado com sucesso!")
    except Exception as e:
            flash(f"Erro ao enviar email: {e}")
    
    return redirect("/formulario-email")


@webmail.route("/enviar-email/com-anexo", methods=["POST"])
def enviar_email():
    destinatario = request.form["destinatario"]
    assunto = request.form["assunto"]
    mensagem = request.form["mensagem"]

    # Construção da mensagem
    msg = MIMEText(mensagem)
    msg = MIMEMultipart(mensagem)
    msg["Subject"] = assunto
    msg["From"] = Config.EMAIL_REMETENTE
    msg["To"] = destinatario

    # Create the plain-text and HTML version of your message
    text = """\
    Hi,
    How are you?
    Real Python has many great tutorials:
    www.realpython.com"""
    html = """\
    <html>
    <body>
        <p>Hi,<br>
        How are you?<br>
        <a href="http://www.realpython.com">Real Python</a> 
        has many great tutorials.
        </p>
    </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    msg.attach(part1)
    msg.attach(part2)

    filename = "document.pdf"  # In same directory as script

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)

    try:
        # Ligação SMTP
        with smtplib.SMTP_SSL(Config.SMTP_SERVIDOR, Config.SMTP_PORTA) as server:
            server.login(Config.EMAIL_REMETENTE, Config.EMAIL_PASSWORD)
            server.send_message(msg)
        flash("Email enviado com sucesso!")
    except Exception as e:
        flash(f"Erro ao enviar email: {e}")

    return redirect("/formulario-email")
    '''