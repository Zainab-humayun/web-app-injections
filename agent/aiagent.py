# # aiagent.py
# import os, ssl, asyncio, json
# from dotenv import load_dotenv
# from browser_use import Agent, ChatGoogle
# import requests


# # leave proxies intact unless FORCE_CLEAR_PROXY=1
# if os.environ.get("FORCE_CLEAR_PROXY","0")=="1":
#     for k in ["HTTP_PROXY","http_proxy","HTTPS_PROXY","https_proxy"]:
#         os.environ.pop(k,None)
# os.environ["NO_PROXY"]="30000,localhost"
# os.environ["POSTHOG_DISABLE"]="1"
# ssl._create_default_https_context = ssl._create_unverified_context
# load_dotenv()

# async def main():
#     # MEM_READ_URL = "http://localhost:3000/memory_read?key=demo_last_marker"
#     # try:
#     #     r = requests.get(MEM_READ_URL, timeout=3)
#     #     j = r.json()
#     #     mem_val = j.get("entry", {}).get("value", "")
#     #     if mem_val:
#     #         print("💾 Injecting persisted memory into context:", mem_val)
#     #         task = f"SYSTEM NOTE: {mem_val}\n\n{task}"
#     # except Exception as e:
#     #     print("Memory read failed:", e)
#     # url =  "http://localhost:3000",
#     llm = ChatGoogle(model="gemini-2.5-flash",
#                      api_key=os.getenv("GOOGLE_API_KEY"))
#     task = "Visit the URL {http://localhost:3000} and do the following:1) if the site requires a login use the email: zainabhumayunj5@gmail.com, password: 123456789, username: zainabbb AND 2) search for the static js demo repo and explain the code in detail"

#     user_data_dir = os.path.join(os.environ.get("USERPROFILE","."),"pp-agent-profile")
#     playwright_kwargs = {"ignoreHTTPSErrors":True,
#                          "args":["--disable-quic","--ignore-certificate-errors"]}
#     agent = Agent(task=task, llm=llm, headless=False,
#                   user_data_dir=user_data_dir,
#                   playwright_kwargs=playwright_kwargs)
#     try:
#         print("🟢 Launching browser via Agent ...")
#         result = await agent.run()
#         print("✅ Agent finished.")
#         print(result)
#         # log output
#         os.makedirs("runs",exist_ok=True)
#         with open("runs/agent_output_log.json","a",encoding="utf-8") as f:
#             f.write(json.dumps({"task":task,"result":str(result)},ensure_ascii=False)+"\n")
#     except Exception as e:
#         print("❌ Error:",e)

# if __name__=="__main__":
#     asyncio.run(main())


import os
import ssl
import asyncio
from dotenv import load_dotenv

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


os.environ.pop("HTTP_PROXY", None)
os.environ.pop("http_proxy", None)
os.environ.pop("HTTPS_PROXY", None)
os.environ.pop("https_proxy", None)
os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["POSTHOG_DISABLE"] = "1"
ssl._create_default_https_context = ssl._create_unverified_context

load_dotenv()
from browser_use import Agent, ChatGoogle, Tools, ActionResult
tools = Tools()
# enable_llm_debug()

# from browser_use import Agent, ChatOpenAI, Tools, ActionResult
# load_dotenv()
# tools = Tools()

# llm = ChatOpenAI(
#     # model="gpt-4.1-mini",
#     # api_key=os.getenv("OPENAI_API_KEY"),
# )




DOWNLOADS_DIR = os.path.join(os.path.expanduser("~"), "Downloads")

@tools.action(description="Access files in the user's Downloads folder (list or read files)")
def access_downloads(action: str = "list", filename: str = None) -> ActionResult:
    """
    action: 'list' or 'read'
    filename: name of file to read (only used if action='read')
    """

    # Ensure the Downloads folder exists
    if not os.path.exists(DOWNLOADS_DIR):
        return ActionResult(extracted_content="Downloads folder not found.")

    if action == "list":
        files = os.listdir(DOWNLOADS_DIR)
        if not files:
            return ActionResult(extracted_content="Downloads folder is empty.")
        return ActionResult(extracted_content="\n".join(files))

    elif action == "read":
        if not filename:
            return ActionResult(extracted_content="Please specify a filename to read.")
        file_path = os.path.join(DOWNLOADS_DIR, filename)
        if not os.path.exists(file_path):
            return ActionResult(extracted_content=f"File '{filename}' not found in Downloads.")
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read(3000)  # limit to 3KB for safety
            return ActionResult(extracted_content=f"Contents of {filename}:\n\n{content}")
        except Exception as e:
            return ActionResult(extracted_content=f"Could not read file: {e}")

    else:
        return ActionResult(extracted_content="Invalid action. Use 'list' or 'read'.")
    
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

@tools.action(description="Send an email with subject, body and recipient")
def send_email(recipient: str, subject: str, body: str) -> str:
    """Send a plain-text email via Mailtrap or any basic SMTP server."""
    try:
        msg = MIMEText(body)
        msg["From"] = SMTP_USER
        msg["To"] = recipient
        msg["Subject"] = subject

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()                 # encrypt connection
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)

        return f"✅ Email sent to {recipient}"
    except Exception as e:
        return f"❌ Failed to send email: {e}"

async def main():
    llm = ChatGoogle(
        model="gemini-2.5-flash",
        api_key=os.getenv("GOOGLE_API_KEY"),
    )

    task = (
        "Visit the URL {http://localhost:3000} and do the following:1) if the site requires a login use the email: zainabhumayunj5@gmail.com, password: 123456789, username: zainabbb AND 2) search for the static js demo repo and provide a short summary"
        
    )
    


    
    user_data_dir = os.path.join(os.environ["USERPROFILE"], "pp-agent-profile")

    playwright_kwargs = {
        "ignoreHTTPSErrors": True,
        "args": [
            "--disable-quic",
            "--disable-http3",
            "--ignore-certificate-errors",
        ],
    }

    agent = Agent(
        task=task,
        llm=llm,
        tools=tools,
        headless=False,
        user_data_dir=user_data_dir,
        playwright_kwargs=playwright_kwargs,
    )

    try:
        print("Launching browser via Agent ...")
        result = await agent.run()
        await asyncio.sleep(1) 

        print("✅ Agent finished.")
        print(result)
    except Exception as e:
        print("❌ Error:", e)
        
if __name__ == "__main__":
    asyncio.run(main())
