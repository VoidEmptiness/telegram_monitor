# Telegram Monitor 🤖

## 👤 Developers

**Company:** Emptiness

**Main Developer:** Cascade AI
**Technical Curator:** Void Emptiness

## 🌟 About the Project

Telegram Monitor is a powerful tool for tracking keywords in Telegram channels. Designed to help users automatically monitor important information.

## 🚀 My Contribution and AI Contribution

### My Contribution (Void Emptiness):
- Defining project business requirements
- Testing and debugging functionality
- Formulating technical requirements

### AI Contribution (Cascade AI):
1. **Project Architecture**:
   - Developing Telegram bot structure
   - Creating channel monitoring module
   - Designing notification system

2. **Code and Functionality**:
   - Writing main Telegram monitor code
   - Implementing keyword search mechanism
   - Telegram API integration
   - Developing message handlers
   - Creating web interface

3. **Optimization and Security**:
   - Code refactoring
   - Adding error handling

4. **Documentation**:
   - Writing README

**Collaborative work allowed us to create a reliable and convenient tool for monitoring Telegram channels!**

## 🔧 How to Get Telegram API Keys

### Step 1: Creating an Application in Telegram
1. Go to [my.telegram.org](https://my.telegram.org/)
2. Log in with your phone number
3. Select "API development tools"
4. Fill out the form:
   - App title: Your application name
   - Short name: Short name (without spaces)
   - URL: Can be left empty
   - Platform: Choose platform (Windows, macOS, Linux)
   - Description: Brief application description

### Step 2: Getting API ID and API Hash
- After creating the application, you will be given:
  - `API ID` - numerical identifier
  - `API Hash` - secret key

### Step 3: Creating Telegram Bot
1. Open [@BotFather](https://t.me/BotFather) in Telegram
2. Send the `/newbot` command
3. Follow instructions to create a bot
4. Get `BOT TOKEN`

## 🛠 Installation

1. Clone the repository
```bash
git clone https://github.com/VoidEmptiness/telegram_monitor.git
cd telegram-monitor
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Create `.env` file and fill in:
```
API_ID='your_api_id'
API_HASH='your_api_hash'
CHANNEL_USERNAME='channel_link'
KEYWORDS='keyword1,keyword2,keyword3'
PERSONAL_CHAT_ID='your_personal_chat_id'
BOT_TOKEN='your_bot_token'
```

## 🚀 Launch

```bash
python start.py
```

## ⚠️ Important
- Make sure the bot is added to the channel
- Check the correctness of API keys
- Comply with Telegram API usage rules

## 📄 License

MIT License

Copyright (c) 2024 Void Emptiness

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 🤝 Support
For questions and suggestions: [voidemptiness63@gmail.com]
