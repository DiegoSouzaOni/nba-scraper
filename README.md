# 🏀 NBA Stats Scraper

This is a personal project for scraping and analyzing NBA data, with a focus on betting strategies. The project is modularized and written in Python.

## 🚀 Project Features

- ✅ Extraction of game data from the official NBA API
- ✅ Player statistics for the last games
- ✅ Confidence scoring system for performance analysis
- ✅ Score interpretation with emojis and visual feedback
- ✅ HTML report generation for visualization
- ✅ Modular architecture and clear organization

## 📁 Project Structure

```
nba-scraper/
│
├── main.py                        # Main script
├── globals.py                    # Global variables and constants
├── services/
│   ├── game_service.py           # Game data handling
│   ├── player_service.py         # Player data handling
│   ├── boxscore_service.py       # Quarter-by-quarter and defense analysis
│   ├── analysis_service.py       # Performance and score calculations
│   ├── display_service.py        # Terminal and HTML visualization
│   └── game_analysis_service.py  # Comparative player analysis
├── formatters.py                 # Formatters and helpers
├── outputs/
│   └── *.html                    # HTML analysis reports
└── README.md
```

## 📊 Score System

Each player receives a confidence score based on:

- Average stats in the last games
- Position played
- Performance trends
- Opponent analysis (in progress)

## 🔧 How to Use

1. Clone the project:
   ```bash
   git clone https://github.com/your-user/nba-scraper
   cd nba-scraper
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the analysis:
   ```bash
   python main.py
   ```

4. Open the generated HTML files in the `outputs/` folder.

## 📦 Dependencies

- `requests`
- `pandas`
- `beautifulsoup4` (if needed for extra scraping)
- `matplotlib` / `seaborn` (optional for visualizations)

## 💡 Future Suggestions (top suggestions)

- Score comparison by player and position
- Opponent analysis per game
- Interactive dashboard (e.g., Streamlit or Power BI)
- Google Sheets integration
- Bet result history with green/red feedback

## ✨ Credits

Developed by @DiegoSouzaOni in partnership with [ChatGPT] 🤖 and fueled by coffee and passion for basketball ☕🏀