# 🍽️ Restaurant AI Agent + n8n Notifications

**Assignment 4 – Capstone Project (40 pts)**

An AI-powered restaurant chatbot that handles table reservations and cancellations.  
When a booking is created or cancelled, the system sends a webhook to **n8n**, which routes the event and sends a Telegram notification.

---

## 🏗️ System Architecture

```
Gradio UI  →  LangChain Chatbot  →  SQLite DB
                    │
                    ▼
              n8n Webhook
                    │
         ┌──────────┴──────────┐
         ▼                     ▼
   Reservation             Cancellation
   Notification            Notification
      (Telegram)              (Telegram)
```

---

## ✨ Features

### Python Backend
- **Intent classification** using LLM (with keyword fallback)
- **Natural language reservation extraction** (name, date, time, party size)
- **SQLite storage** with soft-delete (`status = 'cancelled'`)
- **Webhook integration** with n8n (fire-and-forget)
- **Gradio chat interface**

### n8n Workflow
- Webhook trigger (`POST /webhook/restaurant`)
- IF node that splits by `event` type
- Separate Telegram messages for:
  - New reservation
  - Cancellation

---

## 📁 Project Structure

```
4 - n8n/
├── restaurant_chatbot.py              # Main chatbot + Gradio UI
├── restaurant_db.py                   # SQLite helpers
├── restaurant_telegram_workflow.json  # n8n workflow export
├── restaurant.db                      # SQLite database
├── requirements.txt
├── docker-compose.yml                 # Optional n8n setup
├── .env.example
├── README.md
└── images/                            # Screenshots of the workflow & UI
```

---

## 🚀 Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

Copy the example file and fill in your keys:

```bash
cp .env.example .env
```

```env
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o-mini
N8N_WEBHOOK_URL=http://localhost:5678/webhook/restaurant
RESTAURANT_DB=restaurant.db
```

### 3. Start n8n

Using Docker Compose:

```bash
docker-compose up -d
```

Or directly:

```bash
docker run -p 5678:5678 n8nio/n8n
```

Open: [http://localhost:5678](http://localhost:5678)

### 4. Import the workflow

1. In n8n, go to **Workflows → Import from File**
2. Select `restaurant_telegram_workflow.json`
3. Configure your **Telegram credentials**
4. Set the correct **Chat ID**
5. **Activate** the workflow

### 5. Run the chatbot

```bash
python restaurant_chatbot.py
```

Open the Gradio interface (usually `http://127.0.0.1:7860` or `7861`).

---

## 🧪 How to Test

### Book a table
```
Book a table for 4 people tomorrow at 8:00 PM, my name is Alex
```

### Cancel a reservation
```
Cancel reservation #1
```

### Other examples
```
What is on the menu?
What are your opening hours?
```

---

## 📸 Screenshots

### Gradio Chat UI – Reservation & Cancellation

![Gradio Reservation](https://github.com/user-attachments/assets/9c0ffac6-b3fe-488c-abae-2420b04bdce1)

![Gradio Cancellation](https://github.com/user-attachments/assets/c9a8f348-a076-4dd6-9d8c-cf5e2f161024)

![Gradio Chat Flow](https://github.com/user-attachments/assets/090ace14-42e0-4203-ba6d-f86421b622f6)

### n8n Workflow

![n8n Execution / Telegram](https://github.com/user-attachments/assets/cdcf51a6-0ce8-45e2-ae43-19e9a92b7c5a)


![n8n Workflow Overview](https://github.com/user-attachments/assets/495f2f46-8272-458e-96a5-f3e877920de7)

The screenshots show:
- Successful table reservation through Gradio
- Successful cancellation with booking ID
- Full n8n workflow (Webhook → IF → Telegram)
- Telegram notification messages

---

## 📦 Database Schema

```sql
CREATE TABLE reservations (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    date          TEXT NOT NULL,
    time          TEXT NOT NULL,
    party_size    INTEGER NOT NULL,
    contact       TEXT,
    status        TEXT NOT NULL DEFAULT 'confirmed',
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔗 Webhook Payload

### Reservation
```json
{
  "id": 12,
  "customer_name": "Alex",
  "date": "2026-07-31",
  "time": "20:00",
  "party_size": 4,
  "contact": null,
  "event": "reservation"
}
```

### Cancellation
```json
{
  "id": 12,
  "customer_name": "Alex",
  "date": "2026-07-31",
  "time": "20:00",
  "party_size": 4,
  "event": "cancellation"
}
```

---

## ✅ Requirements Covered

| Requirement | Status |
|-------------|--------|
| `reservations` table | ✅ |
| `book_reservation()` | ✅ |
| `cancel_reservation()` | ✅ |
| LLM classifier (reservation / cancellation) | ✅ |
| LLM extraction of booking details | ✅ |
| Webhook to n8n on book & cancel | ✅ |
| n8n Webhook node | ✅ |
| IF node (reservation vs cancellation) | ✅ |
| Different notification messages | ✅ |
| Gradio UI | ✅ |

---

## 🛠️ Tech Stack

- **Python** + LangChain + OpenAI
- **SQLite**
- **Gradio**
- **n8n**
- **Telegram** (notifications)
- **Docker** (optional for n8n)
