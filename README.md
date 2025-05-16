# Full Ollama Automation

A fully automated script for managing and processing tasks related to the Ollama system. This project aims to simplify and speed up common operations, making it easier to handle large-scale workflows.

## 📁 Project Structure

```
scraping_application/
├── venv/
├── quelltext_scraper/
│   └── quelltext_scraper/
│       ├── spiders/
│       │   └── __pycache__/
│       └── __pycache__/
├── requirements.txt
├── README.md
└── full_ollama_automation.py
```

## 🛠️ Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Frutschli/scraping_application
   cd scraping_application
   ```
2. **Set Up a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. **Install Dependencies:**

   ```bash
   ollama run lama3.2:3b
   pip install -r requirements.txt
   ```

## ▶️ Running the Script

To run the main automation script, use:

```bash
python main.py
```

## 📄 Requirements

Make sure you have Python 3.8+ installed. All required packages are listed in `requirements.txt`.

## 🤝 Contributing

Feel free to fork this repo, create a new branch, and submit a pull request. All contributions are welcome!

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
