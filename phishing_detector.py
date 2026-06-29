import tkinter as tk
from tkinter import messagebox
import random

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression


# ==========================
# DATA
# ==========================


phishing_urls = [

    # ===== NORMAL PHISHING =====
    "http://paypal-login-security.com",
    "http://verify-bank-account-now.com",

    # ===== MALFORMED PROTOCOLS =====
    "http//paypal.com/login",          # missing :
    "htp://secure-bank-login.com",     # wrong protocol
    "httpss://amazon-update.com",      # extra s
    "htt://facebook-login.net",        # incomplete http
    "hxxp://malicious-site.ru",        # obfuscated http

    # ===== MISSING SLASHES =====
    "http:/paypal.com",
    "https:/google.com",
    "http:paypal.com/login",

    # ===== TYPO + PROTOCOL MIX =====
    "htp://paypa1.com/login",
    "httpss://g00gle.com/security",
    "http//faceb00k-login.net",

    # ===== SUBDOMAIN TRICKS =====
    "http://paypal.com.verify-login.ru",
    "http://google.com.security-check.xyz",

    # ===== @ TRICK =====
    "http://paypal.com@malicious.ru",
    "https://amazon.in@fake-site.xyz",

    # ===== IP + PATH =====
    "http://192.168.0.1/login",
    "http://45.33.32.156/verify",

    # ===== SHORTENERS =====
    "http://bit.ly/free-login",
    "http://tinyurl.com/account-verify",

    # ===== ENCODED =====
    "http://%70%61%79%70%61%6c.com.verify.ru",
    "http://paypal.com%2Flogin%2Fsecure",

    # ===== FILE ATTACKS =====
    "http://secure-update.com/file.exe",
    "http://bank-login.com/document.pdf.exe",

    # ===== RANDOMIZED =====
    "http://login-secure-9923.xyz",
    "http://verify-account-88.top"
]

safe_urls = [
    "https://www.google.com",
    "https://www.quora.com",
    "https://www.wikipedia.org",
    "https://github.com",
    "https://www.microsoft.com",
    "https://www.apple.com",
    "https://www.amazon.in",
    "https://www.stackoverflow.com",
    "https://www.linkedin.com",
    "https://www.netflix.com",
    "https://www.facebook.com",
    "https://www.instagram.com",
    "https://www.twitter.com",
    "https://www.youtube.com",
    "https://www.reddit.com",
    "https://www.openai.com",
    "https://www.yahoo.com",
    "https://www.bing.com",
    "https://www.quora.com",
    "https://www.medium.com",
    "https://www.pinterest.com",
    "https://www.adobe.com",
    "https://www.nytimes.com",
    "https://www.bbc.com",
    "https://www.cnn.com",
    "https://www.ibm.com",
    "https://www.intel.com"

]


phishing_emails= [
    "Click here to unlock your account",
    "Unauthorized login detected, secure now",
    "Your payment failed, update details now",
    "Confirm your identity to continue using services",
    "Your ATM card has been disabled",
    "Update your KYC information urgently",
    "You have received a cashback reward, claim now",
    "Login attempt failed, verify immediately",
    "Act now to prevent account closure",
    "Suspicious activity detected on your account",
    "Click below to reset your credentials",
    "You have won a limited time reward",
    "Final warning: verify your account now",
    "Your email will be deactivated",
    "Update your password immediately",
    "You have an unclaimed refund",
    "Claim your tax refund now",
    "Security notice: unusual activity found",
    "Your subscription payment failed",
    "Your account requires urgent attention",
    "Verify details to avoid permanent ban",
    "Limited offer: free voucher inside",
    "Your account access is restricted",
    "Please confirm your billing information",
    "Urgent login required to secure account",
    "You have pending transactions",
    "Click to resolve account issues",
    "Your debit card has been blocked",
    "Confirm your OTP to proceed",
    "You are eligible for a reward",
    "Update your profile to avoid issues",
    "Account login failed multiple times",
    "You must verify your account today",
    "Your account has been flagged",
    "Immediate action required for security reasons",
    "Confirm your phone number now",
    "Verify your login details",
    "Reset your password using the link",
    "Claim your prize before it expires",
    "Free recharge offer available now",
    "Your wallet has been locked",
    "Re-activate your account immediately",
    "Submit your details to continue",
    "Your account is under review",
    "Security breach detected",
    "You must act now to secure account",
    "Click here to fix your account issue"
]


safe_emails = [
            "Meeting agenda attached",
            "Happy birthday! Check out your gift",
            "Invoice for your purchase is attached",
            "Team meeting at 3 PM today",
            "Project report has been uploaded",
            "Lunch plan for tomorrow",
            "Weekly newsletter is here",
            "Client feedback attached",
            "Reminder: submit your assignment",
            "Office will remain closed tomorrow",
            "Meeting rescheduled to Friday",
            "Thanks for your payment",
            "Team outing this weekend",
            "Monthly report attached",
            "Happy anniversary wishes",
            "Your order has been delivered",
            "Please review the document",
            "Training session details attached",
            "Schedule for next week",
            "Project deadline extended",
            "Dinner plans tonight?",
            "Invoice for services rendered",
            "Team sync meeting link",
            "Performance review attached",
            "Notes from today's meeting",
            "Meeting scheduled at 10 AM tomorrow",
            "Please find attached the project report",
            "Let's catch up over coffee this weekend",
            "Your order has been successfully delivered",
            "Invoice for your recent purchase is attached",
            "Happy birthday! Have a great day",
            "Reminder for tomorrow's meeting",
            "Lunch plan for today?",
            "Project files have been uploaded",
            "Weekly update on project status",
            "Client feedback has been shared",
            "Please review the attached document",
            "Team meeting rescheduled to Monday",
            "Thanks for your support",
            "Payment received successfully",
            "Your booking has been confirmed",
            "Here is your ticket for the event",
            "Looking forward to meeting you",
            "Let me know your availability",
            "Your subscription has been renewed",
            "Please submit your report by evening",
            "Dinner tonight?",
            "Monthly newsletter is here",
            "Your request has been processed",
            "We appreciate your feedback",
            "Your package is out for delivery",
            "Meeting notes from today",
            "Here are the documents you requested",
            "Please check and confirm",
            "Thanks for your quick response",
            "The server maintenance is scheduled",
            "Update on your application status",
            "Training session starts at 2 PM",
            "Congratulations on your achievement",
            "Let's schedule a call",
            "Please find the details below",
            "Team outing planned this weekend",
            "Sharing the presentation slides",
            "Your order invoice is attached",
            "Reminder: deadline approaching",
            "Office will be closed tomorrow",
            "Please approve the request",
            "New policy updates attached",
            "Thanks for attending the meeting",
            "Here is your payment receipt",
            "Looking forward to your reply",
            "Meeting link for today's call",
            "Project deadline extended",
            "Please join the session on time",
]


# ==========================
# AI MODELS
# ==========================

email_model = Pipeline([
    ("tfidf",TfidfVectorizer()),
    ("clf",MultinomialNB())
])


email_model.fit(
    phishing_emails+safe_emails,
    ["phishing"]*len(phishing_emails)+
    ["safe"]*len(safe_emails)
)



url_model = Pipeline([
    ("tfidf",
     TfidfVectorizer(
         analyzer="char",
         ngram_range=(3,5)
     )),
    ("clf",LogisticRegression(max_iter=1000))
])


url_model.fit(
    phishing_urls+safe_urls,
    ["phishing"]*len(phishing_urls)+
    ["safe"]*len(safe_urls)
)



# ==========================
# GUI
# ==========================

root=tk.Tk()
root.title("Phishing Attack Simulation & Detection")
root.geometry("900x600")
root.configure(bg="black")


container=tk.Frame(root,bg="black")
container.pack(fill="both",expand=True)


frames={}


def show_page(name):
    frames[name].tkraise()



def create_page(name):

    frame=tk.Frame(
        container,
        bg="black"
    )

    frame.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    frames[name]=frame
    return frame



# ==========================
# EMAIL PAGE
# ==========================

email_page=create_page("email")


tk.Label(
    email_page,
    text="Email Phishing Detector",
    fg="lime",
    bg="black",
    font=("Arial",25,"bold")
).pack(pady=20)



email_box=tk.Text(
    email_page,
    width=70,
    height=10
)

email_box.pack(pady=20)



def fake_email():

    email_box.delete(
        "1.0",
        tk.END
    )

    email_box.insert(
        tk.END,
        random.choice(phishing_emails)
    )



def detect_email():

    text=email_box.get(
        "1.0",
        tk.END
    )


    result=email_model.predict([text])[0]

    messagebox.showinfo(
        "Email Scan",
        "Result : "+result.upper()
    )



tk.Button(
    email_page,
    text="Generate Phishing Email",
    command=fake_email,
    bg="red",
    fg="white"
).pack(pady=5)



tk.Button(
    email_page,
    text="Detect Email",
    command=detect_email,
    bg="green",
    fg="white"
).pack()



# ==========================
# URL PAGE
# ==========================


url_page=create_page("url")


tk.Label(
    url_page,
    text="URL Phishing Detector",
    fg="lime",
    bg="black",
    font=("Arial",25,"bold")
).pack(pady=20)



url_entry=tk.Entry(
    url_page,
    width=60,
    font=("Arial",15)
)

url_entry.pack(pady=20)



def fake_url():

    url_entry.delete(
        0,
        tk.END
    )

    url_entry.insert(
        0,
        random.choice(phishing_urls)
    )



def detect_url():

    url=url_entry.get()

    result=url_model.predict([url])[0]


    messagebox.showinfo(
        "URL Scan",
        "Result : "+result.upper()
    )



tk.Button(
    url_page,
    text="Generate Fake URL",
    command=fake_url,
    bg="red",
    fg="white"
).pack(pady=5)



tk.Button(
    url_page,
    text="Detect URL",
    command=detect_url,
    bg="green",
    fg="white"
).pack()



# ==========================
# NAVIGATION
# ==========================


nav=tk.Frame(
    root,
    bg="black"
)

nav.pack(side="bottom",pady=10)



tk.Button(
    nav,
    text="Email Detector",
    width=20,
    command=lambda:show_page("email"),
    bg="#00aa00",
    fg="white"
).pack(side="left",padx=5)



tk.Button(
    nav,
    text="URL Detector",
    width=20,
    command=lambda:show_page("url"),
    bg="#00aa00",
    fg="white"
).pack(side="left",padx=5)



show_page("email")

root.mainloop()