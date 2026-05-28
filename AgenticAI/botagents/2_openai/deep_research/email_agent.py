import os
from typing import Dict

import requests
from sendgrid.helpers.mail import Email, Mail, Content, To
from agents import Agent, function_tool


@function_tool
def send_email(subject: str, html_body: str) -> str:
    """Send out an email with the given subject and HTML body """
    
    from_email = "Mr <onboarding@resend.dev>"
    to_email = "moumita.ray.soft8@gmail.com"
    RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
    
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "from": from_email,
        "to": [to_email],
        "subject": subject,
        "html": html_body
    }
    
    response = requests.post("https://api.resend.com/emails", json=payload, headers=headers)
    
    if response.status_code == 202:
        return "Email sent successfully"
    else:
        return f"Email failed to send due to {response.text}"


INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the 
report converted into clean, well presented HTML with an appropriate subject line."""


email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini"
)
