# Quizzy.io

Meet Quizzy! It’s like having a trivia night right in your Discord server. Pulling questions from a Google Sheets database, it makes learning feel like a game. It’s not just a bot, it’s your fun-loving, trivia-toting study buddy!

## Features

- _Customizable Question Time:_ You can set the time limit for each question, making the quiz adaptable to your pace.
- _Easy Database Linking:_ Connects seamlessly with Google Sheets, allowing for easy access and updates to the question database.
- _Multiple Choice Format:_ Questions are presented in a multiple-choice format, making it easy and intuitive to use.
- _Scoring System:_ Keeps track of your scores, providing a fun and competitive element to learning.
- _User-Friendly Interface:_ The bot is designed to be user-friendly, making your learning experience smooth and enjoyable.

## Demo
![image](/Users/srirammk/Documents/GitHub/Quizzy.io/assets/ss1.png)
## Run Locally

`1. Clone the project`

```bash
  git clone https://github.com/mk-sriram/Quizzy.io
```

`2. Go to the project directory`

```bash
  cd my-project
```

`3. Install dependencies`

```bash
  npm install
```

Change `SAMPLE_SPREADSHEET_ID` in [main.py](https://github.com/mk-sriram/Quizzy.io/blob/main/first.py) to the Spreadsheet ID of your [example](https://docs.google.com/spreadsheets/d/1n7t6AKuqujrja0Zc7C9x8qRV0CU5O-H9ki08VclHfE4/edit?usp=sharing) Google Sheet database

![spreadsheetID](https://github.com/mk-sriram/Quizzy.io/blob/main/assets/spredsheet%20iD%20.png)

`5. Add new questions in your database`

`6. run main.py`

send command `!study <question number> <time for each question>` in server Chat
