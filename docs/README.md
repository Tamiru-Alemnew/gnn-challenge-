# Interactive Leaderboard

This folder contains the GitHub Pages site for the interactive leaderboard.

## Setup

1. Enable GitHub Pages in repository settings
2. Set source to `docs/` folder
3. The leaderboard will be available at: `https://your-username.github.io/gnn-challenge/`

## Features

- 📊 Live leaderboard updates
- 🎯 Real-time statistics
- 🎨 Beautiful responsive design
- 🔄 Auto-refresh every 30 seconds
- 🏅 Human vs. LLM breakdown

## Local Development

To test locally:
```bash
cd docs
python -m http.server 8000
# Visit http://localhost:8000
```

## Files

- `index.html` - Main leaderboard page
- Fetches data from `../leaderboard/leaderboard.csv`



