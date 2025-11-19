# Web-App Injections  
### A Demonstration Framework for Testing Agentic AI Vulnerabilities in Web Applications

This repository provides a complete environment for evaluating **prompt injections**,  
**agentic manipulations**, **silent redirections**, **phishing via DOM content**, and  
**multimodal (image-based) prompt injection attacks** using a fully functional Reddit-style web app  
and an autonomous web-browsing AI agent.

The project consists of:

- A **website** folder containing the vulnerable full-stack web application  
  (Flask backend + Vite/React frontend).
- An **agent** folder containing the autonomous agent script (`aiagent.py`) that interacts  
  with the website.
- A preloaded set of **attack payloads** automatically injected via `seed_attacks.py`.

---

Step by Step on how to run the files:
1. Clone the repo
2. Ensure that you have postresql setup done and connected to the repository
3. Create virtual environments to run the backend and frontend.
4. Navigate to the website/backend folder and run the "seed_attacks.py" file.

To run the agent:
Add a relevant task in the agent/aiagent.py file and run the aiagent.py file 
