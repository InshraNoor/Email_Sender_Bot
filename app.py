import streamlit as st
import pandas as pd
import smtplib
from email.message import EmailMessage

st.title("📧 Simple Email Sender Bot")


sender_email = st.text_input("Enter Your Gmail")
app_password = st.text_input("Enter Gmail App Password", type="password")

subject = st.text_input("Enter Email Subject")
message = st.text_area("Enter Email Message")

send = st.button("Send Emails")


if send:

    if sender_email == "" or app_password == "":
        st.error("Please enter email and app password")
    else:
        try:
            df = pd.read_csv("recipients.csv")

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, app_password)

            total = len(df)
            progress = st.progress(0)

            for i, row in df.iterrows():

                msg = EmailMessage()
                msg["From"] = sender_email
                msg["To"] = row["email"]
                msg["Subject"] = subject

                personalized_message = f"Hi {row['name']},\n\n{message}"
                msg.set_content(personalized_message)

                server.send_message(msg)

                # Log file
                with open("logs.txt", "a") as file:
                    file.write(f"Email sent to {row['email']}\n")

                progress.progress((i + 1) / total)

            server.quit()

            st.success("All Emails Sent Successfully 🎉")

        except Exception as e:
            st.error(f"Error: {e}")
