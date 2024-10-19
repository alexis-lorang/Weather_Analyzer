############################################################################
# Imports
############################################################################

import json
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

############################################################################
# Variables
############################################################################

File_Path = os.path.abspath(__file__)
Mail_Configuration_Path = os.path.join(os.path.dirname(File_Path),"../Configurations/Mail_Configuration.json")

############################################################################
# Private Methods
############################################################################

def _read_mail_configuration():

    with open(Mail_Configuration_Path) as Mail_Configuration_File:

        Mail_Configuration_Data = json.load(Mail_Configuration_File)

    Sender_Email = Mail_Configuration_Data["Sender_Email"]
    Sender_Password = Mail_Configuration_Data["Sender_Password"]
    Receiver_Email = Mail_Configuration_Data["Receiver_Email"]

    return Sender_Email, Sender_Password, Receiver_Email

def _send_email(From, From_Password, To, Subject, Message):
        
    try:

        # Create Message Object
        msg = MIMEMultipart()
        msg['From'] = From
        msg['To'] = From_Password
        msg['Subject'] = Subject

        # Ajouter le texte au corps de l'email
        msg.attach(MIMEText(Message, 'plain'))

        # Connexion au serveur Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # Connexion à l'adresse email
        server.login(From, From_Password)

        # Envoi de l'email
        text = msg.as_string()
        server.sendmail(From_Password, To, text)

        # Fermer la connexion
        server.quit()

        print("Email envoyé avec succès !")

    except Exception as e:
        print(f"Échec de l'envoi de l'email: {e}")


############################################################################
# Public Methods
############################################################################

def Send_Clear_Sky_Alert(Date, Start_Hour, End_Hour):

    Sender_Email, Sender_Password, Receiver_Email = _read_mail_configuration()

    Subject = f"ALERTE - Nuit dégagée en prévision le {Date}"
    Message = f"La soirée du {Date} devrait être dégagée de {Start_Hour} à {End_Hour}"

    _send_email(Sender_Email, Sender_Password, Receiver_Email, Subject, Message)