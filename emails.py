#---------------------------------------------------------------------------------------------------#
# File name: emails.py                                                                              #
# Autor: Chrissi2802                                                                                #
# Created on: 29.12.2022                                                                            #
#---------------------------------------------------------------------------------------------------#
# This file provides functions to send emails.
# Exact description in the functions.


import yaml
from yaml.loader import SafeLoader
import smtplib
import ssl
from email.mime.text import MIMEText


def send_email(recipient_email, subject, message):
    """This function sends emails.

    Args:
        recipient_email (string): Email address of the recipient
        subject (string): Subject of the email
        message (string): Message of the email
    """

    # Read yaml file, which contains the login data
    stream = open("emails.yaml", "r")
    login_data_yaml = list(yaml.load_all(stream, Loader = SafeLoader))[0]  # Data are only in the first element -> dictionary

    # Connect to the server
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL(host = login_data_yaml["host"], port = login_data_yaml["port"], context = context)
    server.login(login_data_yaml["email"], login_data_yaml["password"])
    
    # Create the email
    email = MIMEText(message, "plain")
    email["From"] = login_data_yaml["email"]
    email["To"] = recipient_email
    email["Subject"] = subject

    # Send the email
    server.sendmail(login_data_yaml["email"], recipient_email, email.as_string())

    # Close the connection
    server.quit()


if (__name__ == "__main__"):

    # Example 1: Send email
    recipient_email = "recipient_email_address@gmail.com"
    subject = "subject"
    message = "Hi, \nhow are you? \nBest regards"
    send_email(recipient_email, subject, message)


    # Example 2: Send email with error message, for example on a server / cluster
    recipient_email = "recipient_email_address@gmail.com"
    subject = "subject"
    message = "Hi, \nthe calculations are finished. \nBest regards"
    
    try:
        pass
        # Code here
    except Exception as e:
        print(e)
        message = "Hi, \nthe calculation was cancelled due to an error. \nBest regards \n \nError: \n"
        message += str(e)
    finally:
        send_email(recipient_email, subject, message)

    