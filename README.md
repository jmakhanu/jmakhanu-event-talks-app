# BigQuery Release Notes Hub

An interactive, responsive dashboard built using **Python Flask** and **Vanilla JS/CSS** that fetches the live Google Cloud BigQuery Release Notes feed, categorizes the updates, and allows users to search, filter, and draft tweets about specific updates.

---

## 🌟 Key Features

*   **Granular Update Splitting**: Automatically splits bundled daily release feed entries into individual, category-specific release cards.
*   **Dynamic Categorization**: Groups and color-codes updates by their type: `Feature` (Emerald), `Announcement` (Blue), `Issue` (Amber), and `Deprecation` (Rose).
*   **Live Sidebar Filters**: Instantly filters releases by type with real-time badges indicating counts for each category.
*   **Instant Text Search**: Instant client-side search across entry titles, dates, types, and body copy.
*   **Sort Toggle**: Allows users to view updates in chronological or reverse-chronological order.
*   **Custom Tweet Composer**: Integrated modal drafts a pre-formatted tweet containing the update summary, hashtags, and a direct anchor link to Google's official release page, complete with a character counter.
*   **Loading State Skeletons**: Displays animated shimmer cards during API requests for a premium user experience.

---

## 🛠️ Technology Stack

*   **Backend**: Python Flask, Requests, Feedparser, BeautifulSoup4
*   **Frontend**: Vanilla HTML5, CSS3 (Modern Flexbox/Grid, Glassmorphism, animations), ES6 JavaScript
*   **Icons**: Lucide Icons
*   **Fonts**: Inter & JetBrains Mono (from Google Fonts)

---

## 📂 Project Structure

```text
├── app.py                  # Flask server and feed parsing logic
├── templates/
│   └── index.html          # Web dashboard and Tweet composer client
├── requirements.txt        # Python dependency manifest
├── news.txt                # Cached world news headlines
├── summary.txt             # Summarized world news headlines
├── .gitignore              # standard files and environments to ignore
└── README.md               # Project documentation
```

---

## 🚀 Installation & Running Locally

### 1. Prerequisites
Make sure you have **Python 3** installed on your system.

### 2. Clone and Setup
Navigate to the project directory:
```bash
cd /home/idriss/agy-cli-projects
```

### 3. Create and Activate Virtual Environment
```bash
# Create venv
python3 -m venv venv

# Activate venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Application
```bash
python app.py
```

### 6. View the App
Open your browser and navigate to:
```text
http://127.0.0.1:5000
```

---

## 💡 How It Works (Parsing Flow)

```text
Google Cloud Feed (XML)
       │
       ▼ (requests & feedparser)
Flask app.py
       │
       ▼ (BeautifulSoup splits entries by <h3> tags)
JSON Payload ──► Client Browser (index.html)
                       │
                       ▼ (Dynamically rendering cards)
                 Dashboard View (Search / Filter / Tweet)
```

1.  When you open the application or click **Refresh Feed**, the browser makes an asynchronous `GET` request to `/api/notes`.
2.  The backend server downloads the Google XML feed.
3.  `BeautifulSoup` splits the text by `<h3>` tags to extract individual updates within a single day.
4.  The server constructs a JSON payload containing details like unique IDs, direct links, and pre-formatted short descriptions.
5.  The client-side JavaScript receives the JSON, performs counts, handles active search filters, and populates the dashboard.
