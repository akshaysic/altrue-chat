# Altrue Chatbot (MVP)


The **Altrue Chatbot** is a lightweight, browser-based conversational interface that helps users **discover and select effective charities**.  
It connects to the **GlobalGiving API** to source credible, up-to-date information on charitable projects worldwide, ensuring users can make informed donation choices.

The chatbot is part of the **Altrue** initiative — a social micro-donation subscription-based platform designed to make charitable giving simple, transparent, and impactful.

## Features
- Conversational guidance to match users with causes they care about
- Integration with **GlobalGiving API** for verified charity/project data
- Clean, minimal UI matching Altrue’s brand (rounded buttons, gradients, soft cards)
- AI-powered intent understanding and recommendations using OpenAI
- Ready for deployment as a browser-based app or embedded widget

## Tech Stack
- Frontend: HTML/CSS/JS (or React/Vite)  
- Backend: Python (Flask)  
- AI: OpenAI API

> If you’re using a different stack, update this section and the commands below accordingly.

## Quick Start

### 1) Clone & install
```bash
git clone https://github.com/akshaysic/altrue-chat.git
cd altrue-chat

# Python env (recommended)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt