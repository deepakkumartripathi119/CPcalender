# CP Calendar - Competitive Programming Calendar Sync

A Python application that automatically syncs upcoming programming contests from **Codeforces**, **LeetCode**, **CodeChef**, and **AtCoder** to your personal Google Calendar.

## Features

- **Multi-Platform Support**:
  - **Codeforces**: Direct API integration.
  - **LeetCode, CodeChef, AtCoder**: Via CLIST API Integration (Robust resource ID lookup).
- **Smart Deduplication**: Uses unique IDs to prevent duplicate events.
- **Timezone Awareness**: Events are automatically converted to `Asia/Kolkata` (Configurable in code).
- **Self-Cleaning Integration**: Includes robust tests that clean up after themselves.
- **Automated**: Ready for GitHub Actions.

---

## 🚀 Getting Started

### Prerequisites

1.  **CLIST Account**:
    - Sign up at [clist.by](https://clist.by/).
    - Go to Settings -> API to get your **Username** and **API Key**.

2.  **Google Cloud Platform (GCP)**:
    - Create a Project.
    - Enable the **Google Calendar API**.
    - Create a **Service Account**.
    - **Download the Key**: Save the JSON key file.

3.  **Google Calendar**:
    - You must **share** your target calendar with the Service Account.
    - Go to Calendar Settings -> "Share with specific people".
    - Add the **Service Account Email** (e.g., `bot@project.iam.gserviceaccount.com`).
    - **Permission**: Select "**Make changes to events**".

---

## 💻 Local Setup

1.  **Clone the repository**:

    ```bash
    git clone https://github.com/your-username/contest-calendar.git
    cd contest-calendar
    ```

2.  **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure `.env`**:
    Create a file named `.env` in the root folder and add your secrets:

    ```ini
    # CLIST Credentials
    CLIST_USERNAME=your_username
    CLIST_API_KEY=your_api_key

    # Google Service Account (Paste the entire JSON string on one line)
    GCP_SA_KEY='{"type": "service_account", ...}'

    # Target Calendar (Your Gmail address)
    GOOGLE_CALENDAR_ID=your.email@gmail.com
    ```

4.  **Run the Script**:
    ```bash
    python main.py
    ```

---

## 🤖 GitHub Actions (Automation)

To run this script automatically every hour:

1.  **Push to GitHub**: Upload this repository to your GitHub account.
2.  **Add Secrets**:
    Go to `Settings` -> `Secrets and variables` -> `Actions` and add the following **Repository Secrets**:
    - `CLIST_USERNAME`
    - `CLIST_API_KEY`
    - `GCP_SA_KEY` (The full JSON string)
    - `GOOGLE_CALENDAR_ID` (Your Gmail address)
3.  **Workflow**:
    The workflow at `.github/workflows/daily_sync.yml` (if present) will pick these up and run the script on schedule.

---

## 🧪 Testing

To verify everything is working without spamming your calendar, run the integration tests. These tests will:

1.  Fetch data from all APIs.
2.  Insert a test event into your calendar.
3.  **Immediately delete** the test event to clean up.

```bash
python tests/test_integration.py
```

---

## Directory Structure

```text
CPcalender/
├── main.py                     # Entry point
├── config.py                   # Configuration manager
├── platforms/                  # Platform specific logic
├── utils/                      # Helper modules (Calendar, API)
└── tests/                      # Integration tests
```
