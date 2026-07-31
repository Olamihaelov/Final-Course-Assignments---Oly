"""
Restaurant AI Chatbot - Task 4
"""

import os
import re
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional
from dotenv import load_dotenv
import gradio as gr
import requests

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from restaurant_db import (
    initialize_database, book_reservation, cancel_reservation,
    get_reservation_by_id, get_menu
)

# ==================== SETUP ====================

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
# Configure DB path and initialize
DB_PATH = os.path.join(os.path.dirname(__file__), "restaurant.db")
initialize_database(DB_PATH)

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("restaurant")

# --- In-code opening hours and helpers (inlined per request) ---
HOURS = {
    "Main": [
        {"day": "Monday", "open_time": "11:00", "close_time": "23:00"},
        {"day": "Tuesday", "open_time": "11:00", "close_time": "23:00"},
        {"day": "Wednesday", "open_time": "11:00", "close_time": "23:00"},
        {"day": "Thursday", "open_time": "11:00", "close_time": "00:00"},
        {"day": "Friday", "open_time": "11:00", "close_time": "01:00"},
        {"day": "Saturday", "open_time": "12:00", "close_time": "01:00"},
        {"day": "Sunday", "open_time": "12:00", "close_time": "22:00"},
    ],
    "Downtown": [
        {"day": "Monday", "open_time": "10:00", "close_time": "22:00"},
        {"day": "Tuesday", "open_time": "10:00", "close_time": "22:00"},
        {"day": "Wednesday", "open_time": "10:00", "close_time": "22:00"},
        {"day": "Thursday", "open_time": "10:00", "close_time": "23:00"},
        {"day": "Friday", "open_time": "10:00", "close_time": "02:00"},
        {"day": "Saturday", "open_time": "11:00", "close_time": "02:00"},
        {"day": "Sunday", "open_time": "11:00", "close_time": "21:00"},
    ]
}


def normalize_time(time_str: str) -> str:
    time_str = time_str.replace('.', ':').lower().strip()
    if 'am' in time_str or 'pm' in time_str:
        ampm = 'pm' if 'pm' in time_str else 'am'
        time_part = time_str.replace('am', '').replace('pm', '').strip()
        parts = time_part.split(':')
        hour = int(parts[0])
        minute = int(parts[1]) if len(parts) > 1 else 0
        if ampm == 'pm' and hour != 12:
            hour += 12
        if ampm == 'am' and hour == 12:
            hour = 0
        return f"{hour:02d}:{minute:02d}"
    return time_str


def parse_weekday(q_lower: str) -> Optional[str]:
    weekdays = {
        'monday': 0, 'tuesday': 1, 'wednesday': 2,
        'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6
    }
    for name, idx in weekdays.items():
        if re.search(r'\b' + name + r'\b', q_lower):
            today = datetime.now().date()
            days_ahead = (idx - today.weekday() + 7) % 7
            if days_ahead == 0:
                days_ahead = 7
            target = today + timedelta(days=days_ahead)
            return target.strftime('%Y-%m-%d')
    return None


def parse_natural_date(text: str) -> Optional[str]:
    m = re.search(r'(\d{4}-\d{2}-\d{2})', text)
    if m:
        return m.group(1)

    m = re.search(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b", text)
    if m:
        d, mo, y = map(int, m.groups())
        try:
            return datetime(y, mo, d).strftime('%Y-%m-%d')
        except ValueError:
            return None

    months = {m.lower(): i for i, m in enumerate(["January","February","March","April","May","June","July","August","September","October","November","December"], start=1)}
    m = re.search(r"\b([A-Za-z]{3,9})\s+(\d{1,2})(?:,?\s*(\d{4}))?\b", text)
    if m:
        mon, day, year = m.group(1), int(m.group(2)), m.group(3)
        mon_l = mon.lower()
        mon_full = next((k for k in months.keys() if k.startswith(mon_l)), None)
        if mon_full:
            mon_i = months[mon_full]
            y = int(year) if year else datetime.now().year
            try:
                return datetime(y, mon_i, day).strftime('%Y-%m-%d')
            except ValueError:
                return None

    m = re.search(r"\b(\d{1,2})\s+([A-Za-z]{3,9})(?:,?\s*(\d{4}))?\b", text)
    if m:
        day, mon, year = int(m.group(1)), m.group(2), m.group(3)
        mon_l = mon.lower()
        mon_full = next((k for k in months.keys() if k.startswith(mon_l)), None)
        if mon_full:
            mon_i = months[mon_full]
            y = int(year) if year else datetime.now().year
            try:
                return datetime(y, mon_i, day).strftime('%Y-%m-%d')
            except ValueError:
                return None

    return None


def extract_location_from_question(question: str) -> Optional[str]:
    q = question.lower()
    if 'downtown' in q:
        return 'Downtown'
    if 'main' in q or 'sunset' in q or 'bistro' in q:
        return 'Main'
    m = re.search(r"\b(?:at|in|for)\s+([A-Za-z0-9\- ]{3,30})\b", question, re.I)
    if m:
        candidate = m.group(1).strip().title()
        if candidate.lower() in ('downtown', 'main', 'airport'):
            return candidate.title()
    return None


def extract_day_from_question(question: str) -> Optional[str]:
    q = question.lower()
    if re.search(r"\btoday\b", q):
        return datetime.now().strftime('%A')
    if re.search(r"\btomorrow\b", q):
        return (datetime.now() + timedelta(days=1)).strftime('%A')
    for d in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']:
        if re.search(r'\b' + d + r'\b', q):
            return d.title()
    return None


def needs_location_for_hours(question: str) -> bool:
    q = question.lower().strip()
    generic = {"hours", "opening hours", "what are your hours", "when are you open", "when do you close", "working hours"}
    if q in generic or len(q.split()) <= 2:
        return True
    if re.search(r"\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday|today|tomorrow)\b", q):
        return False
    if re.search(r"\d{1,2}:\d{2}|\b\d{1,2}\s?(am|pm)\b", q):
        return False
    if re.search(r"\b(branch|downtown|airport|main|location|branch name)\b", q):
        return False
    return False




class RestaurantChatbot:
    # Restaurant assistant

    def __init__(self):
        self.db_path = DB_PATH
        self.llm = self._init_llm()
        # use in-code hours data
        self.hours = HOURS
        logger.info("RestaurantChatbot initialized")

    def _init_llm(self) -> Optional[ChatOpenAI]:
        # Init LLM if key present
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or not api_key.startswith("sk-"):
            logger.warning("No OpenAI API key found; running in fallback mode.")
            return None
        try:
            llm = ChatOpenAI(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                temperature=0
            )
            logger.info(f"LLM loaded: {llm.model_name}")
            return llm
        except Exception as e:
            logger.exception("LLM initialization error: %s", e)
            return None

    # ==================== CLASSIFICATION ====================

    def classify_question(self, question: str) -> str:
        # Classify intent
        if self.llm:
            return self._classify_with_llm(question)
        return self._classify_with_keywords(question)

    def _classify_with_llm(self, text: str) -> str:
        prompt = ChatPromptTemplate.from_messages([
            {"role": "system", "content": "Classify into ONE word: reservation, cancellation, menu, hours, general. Return ONLY the word."},
            {"role": "user", "content": "{text}"}
        ])
        try:
            result = (prompt | self.llm | StrOutputParser()).invoke({"text": text}).strip().lower()
            if result in {"reservation", "cancellation", "menu", "hours", "general"}:
                return result
        except Exception:
            pass
        return self._classify_with_keywords(text)

    def _classify_with_keywords(self, text: str) -> str:
        text_lower = text.lower()
        if any(k in text_lower for k in ["reserve", "book", "table", "reservation"]):
            return "reservation"
        elif any(k in text_lower for k in ["cancel", "cancellation", "remove"]):
            return "cancellation"
        elif any(k in text_lower for k in ["menu", "food", "dish", "price"]):
            return "menu"
        elif any(k in text_lower for k in ["hour", "open", "close", "time"]):
            return "hours"
        return "general"

    # ==================== MAIN ROUTER ====================

    def answer(self, question: str) -> str:
        # Route to handler
        q_lower = question.lower()
        # Keyword override: if user explicitly asks to cancel, prefer cancellation
        if any(k in q_lower for k in ["cancel", "cancel my", "cancel reservation", "cancel order", "i want to cancel"]):
            category = "cancellation"
        else:
            category = self.classify_question(question)
        logger.debug("Category: %s", category)

        handlers = {
            "reservation": self._handle_reservation,
            "cancellation": self._handle_cancellation,
            "menu": self._handle_menu,
            "hours": self._handle_hours,
            "general": self._handle_general
        }
        return handlers[category](question)

    # ==================== 🎯 RESERVATION HANDLER (REDESIGNED) ====================

    def _handle_reservation(self, question: str) -> str:
        # Reservation handler
        if self.llm:
            try:
                return self._extract_with_llm(question)
            except Exception as e:
                logger.exception("LLM extraction error: %s", e)

        return self._extract_with_keywords(question)

    def _extract_with_llm(self, question: str) -> str:
        # Extract reservation with LLM
        current_date = datetime.now().strftime("%Y-%m-%d")
        prompt = ChatPromptTemplate.from_messages([
            {"role": "system", "content": f"Today is {current_date}. Extract reservation details as JSON with keys: "
                      "customer_name, date (YYYY-MM-DD), time (HH:MM), party_size (number), contact (optional). "
                      "Resolve 'today'/'tonight'/'tomorrow' to dates. Return ONLY valid JSON."},
            {"role": "user", "content": "{question}"}
        ])
        raw = (prompt | self.llm | StrOutputParser()).invoke({"question": question}).strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        details = json.loads(raw)
        # Require the user to explicitly supply a date/day token
        if not self._user_supplied_date(question):
            return ("💡 To complete your reservation, please provide a date or day. "
                    "Examples: 'today', 'tomorrow', 'Monday', or '2026-07-30'.")
        return self._process_reservation(details)

    def _user_supplied_date(self, question: str) -> bool:
        # Detect explicit date/day tokens
        q = question.lower()
        if re.search(r"\b(today|tomorrow|tonight)\b", q):
            return True
        if re.search(r"\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b", q):
            return True
        if re.search(r"\d{4}-\d{2}-\d{2}", q):
            return True
        # also accept explicit 'on <month name> <day>' patterns (simple)
        if re.search(r"\bon\s+\w+\s+\d{1,2}\b", q):
            return True
        return False

    def _extract_with_keywords(self, question: str) -> str:
        # Fallback extraction
        details = {
            "customer_name": "Guest",
            "date": None,
            "time": None,
            "party_size": 2,
            "contact": None
        }

        # --- Party Size ---
        party_match = re.search(r'for\s+(\d+)\s*(?:people|guests|ppl)?', question, re.I)
        if party_match:
            details["party_size"] = int(party_match.group(1))

        # --- Time ---
        time_match = re.search(r'at\s+(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)', question, re.I)
        if time_match:
            details["time"] = normalize_time(time_match.group(1))

        # --- Date ---
        q_lower = question.lower()
        if "today" in q_lower or "tonight" in q_lower:
            details["date"] = datetime.now().strftime("%Y-%m-%d")
        elif "tomorrow" in q_lower:
            details["date"] = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        else:
            # check weekday names (e.g., Monday) and resolve to next occurrence
            weekday_date = parse_weekday(q_lower)
            if weekday_date:
                details["date"] = weekday_date
            else:
                # ISO format
                date_match = re.search(r'(\d{4}-\d{2}-\d{2})', question)
                if date_match:
                    details["date"] = date_match.group(1)
                else:
                    # Try common natural formats (DD/MM/YYYY, 'July 30', '30th July')
                    parsed = parse_natural_date(question)
                    if parsed:
                        details["date"] = parsed
        

        # --- Name ---
        # Prefer explicit phrases: "my name is X", "I'm X", "name: X"
        name_match = re.search(r"\b(?:my name is|i'm|i am|name[:\-]?|this is)\s+([A-Za-z][A-Za-z'\- ]{1,40})\b", question, re.I)
        if name_match:
            name = name_match.group(1).strip()
            if name.lower() not in {"people", "guests", "table", "family", "party"}:
                details["customer_name"] = name.title()
        else:
            # last resort: look for a capitalized word not likely to be a common token
            cap_match = re.search(r"\b([A-Z][a-z]{1,20})\b", question)
            if cap_match and cap_match.group(1).lower() not in {"table", "people", "tomorrow", "today", "tonight", "reservation", "book"}:
                details["customer_name"] = cap_match.group(1)

        if not details["date"] or not details["time"]:
            return self._get_missing_info_prompt(details)

        return self._process_reservation(details)

    

    def _get_missing_info_prompt(self, details: Dict) -> str:
        # Prompt for missing fields
        missing = []
        if not details.get("date"):
            missing.append("date or day (e.g., 'today', 'tomorrow', 'Monday', '2026-07-30')")
        if not details.get("time"):
            missing.append("time (e.g., '19:30', '7:30 PM')")
        if not details.get("customer_name") or details["customer_name"] == "Guest":
            missing.append("your name")

        return (f"Please provide: {', '.join(missing)}. Example: 'tomorrow 8pm, 4 people, name Alex'")

    

    

    def _process_reservation(self, details: Dict) -> str:
        required = ["customer_name", "date", "time", "party_size"]
        if not all(details.get(k) for k in required):
            return self._get_missing_info_prompt(details)
        try:
            res_id = book_reservation(self.db_path, details["customer_name"], details["date"], details["time"], details["party_size"], details.get("contact"))
            logger.info("Reservation #%s created locally", res_id)
            self._notify_n8n({**details, "id": res_id}, event="reservation")
            contact_line = f"📧 **Contact:** {details['contact']}" if details.get("contact") else ""
            return (
                f"🎉 **Your Reservation is Confirmed!**\n\n"
                f"📜 **Booking ID:** #{res_id}\n"
                f"👤 **Name:** {details['customer_name']}\n"
                f"📅 **Date:** {details['date']}\n"
                f"⏰ **Time:** {details['time']}\n"
                f"👥 **Party Size:** {details['party_size']} guests\n"
                f"{contact_line}\n\n"
                f"💬 **Thank you for booking!** Our team has reserved your table.\n"
                f"We look forward to welcoming you at **Sunset Bistro**! 🌅"
            ).strip()
        except Exception as e:
            logger.exception("Reservation error: %s", e)
            return "Error processing reservation. Please try again."

    # ==================== ❌ CANCELLATION HANDLER (REDESIGNED) ====================

    def _handle_cancellation(self, question: str) -> str:
        # Cancellation handler
        match = re.search(r'\b(\d+)\b', question)
        if not match:
            return ("🔍 Need your booking ID\n"
                    "Example: 'Please cancel my reservation #123'")

        res_id = int(match.group(1))
        reservation = get_reservation_by_id(self.db_path, res_id)

        if not reservation:
            return f"❌ Reservation #{res_id} not found\nPlease double-check the ID."

        if reservation['status'] == 'cancelled':
            return (f"ℹ️ Already cancelled\n"
                    f"Reservation #{res_id} was previously cancelled.")

        try:
            success = cancel_reservation(self.db_path, res_id)
            if not success:
                return f"⚠️ No active reservation #{res_id} to cancel."
            logger.info("Reservation #%s cancelled locally", res_id)
            self._notify_n8n({
                "id": res_id,
                "customer_name": reservation["customer_name"],
                "date": reservation["date"],
                "time": reservation["time"],
                "party_size": reservation["party_size"],
                "contact": reservation.get("contact")
            }, event="cancellation")
            contact_line = f"📧 **Contact:** {reservation['contact']}" if reservation.get("contact") else ""
            return (
                f"🚫 **Reservation Cancelled**\n\n"
                f"📜 **Booking ID:** #{res_id}\n"
                f"👤 **Name:** {reservation['customer_name']}\n"
                f"📅 **Date:** {reservation['date']}\n"
                f"⏰ **Time:** {reservation['time']}\n"
                f"👥 **Party Size:** {reservation['party_size']} guests\n"
                f"{contact_line}\n\n"
                f"💔 **We're sorry to see you go!** Your table has been released.\n"
                f"We'd love to welcome you again in the future! 🌟"
            ).strip()
        except Exception as e:
            logger.exception("Cancellation error: %s", e)
            return "Error cancelling reservation. Please try again."

    # ==================== OTHER HANDLERS ====================

    def _handle_menu(self, question: str) -> str:
        # Menu info
        if not self.llm:
            menu = get_menu(self.db_path)
            return "🍽️ **Our Menu**\n" + "\n".join(
                f"• {item['name']} - ${item['price']:.2f} ({item['category']})"
                for item in menu
            )
        prompt = ChatPromptTemplate.from_messages([
            {"role": "system", "content": "Answer menu questions concisely and enthusiastically."},
            {"role": "user", "content": "{question}"}
        ])
        return (prompt | self.llm | StrOutputParser()).invoke({"question": question})

    def _handle_hours(self, question: str) -> str:
        # Hours info
        # If the user asked generically (e.g., 'hours'), ask which location/branch
        if needs_location_for_hours(question):
            return ("Which location or branch are you asking about? "
                    "For example: 'Downtown', 'Airport branch', or the restaurant name.")
        # prefer explicit location/day parsing in fallback mode
        if not self.llm:
            loc = extract_location_from_question(question) or "Main"
            day = extract_day_from_question(question)
            loc_hours = self.hours.get(loc)
            if not loc_hours:
                return (f"I don't have hours for '{loc}'. Available locations: "
                        f"{', '.join(self.hours.keys())}")

            if day:
                match = next((h for h in loc_hours if h['day'].lower() == day.lower()), None)
                if match:
                    return f"⏰ **{loc} Hours** — {match['day']}: {match['open_time']}–{match['close_time']}"
                return f"No hours found for {day} at {loc}."

            # full week
            return "⏰ **Opening Hours**\n" + "\n".join(
                f"• {h['day']}: {h['open_time']}–{h['close_time']}" for h in loc_hours
            )

        prompt = ChatPromptTemplate.from_messages([
            {"role": "system", "content": "Answer hours/location questions clearly."},
            {"role": "user", "content": "{question}"}
        ])
        return (prompt | self.llm | StrOutputParser()).invoke({"question": question})

    def _needs_location_for_hours(self, question: str) -> bool:
        """Return True if the user's hours query is too generic and should ask for location."""
        return needs_location_for_hours(question)

    def _extract_location_from_question(self, question: str) -> Optional[str]:
        return extract_location_from_question(question)

    def _extract_day_from_question(self, question: str) -> Optional[str]:
        return extract_day_from_question(question)

    def _handle_general(self, question: str) -> str:
        """Handle general inquiries."""
        if not self.llm:
            return "Welcome to Sunset Bistro — how can I help?"
        prompt = ChatPromptTemplate.from_messages([
            {"role": "system", "content": "You are a friendly restaurant assistant. Be warm and helpful."},
            {"role": "user", "content": "{question}"}
        ])
        return (prompt | self.llm | StrOutputParser()).invoke({"question": question})

    # ==================== N8N WEBHOOK ====================

    def _notify_n8n(self, data: Dict, event: str) -> None:
        webhook_url = os.getenv("N8N_WEBHOOK_URL") or os.getenv("N8N_WEBHOOK")
        if not webhook_url:
            logger.debug("N8N webhook URL not configured; skipping notify")
            return

        payload = {
            **data,
            "event": event,
            "timestamp": datetime.now().isoformat(),
        }

        try:
            response = requests.post(webhook_url, json=payload, timeout=5)
            if response.ok:
                logger.info("Webhook: %s sent", event)
            else:
                logger.warning("Webhook: %s failed with status %s", event, response.status_code)
        except Exception:
            logger.exception("Webhook error when sending event %s", event)

# ==================== GRADIO UI ====================

def build_gradio_ui(bot: RestaurantChatbot) -> gr.Blocks:
    """Create a simple chat interface for the restaurant assistant."""

    def respond(message: str, history):
        if not message or not message.strip():
            return ""
        reply = bot.answer(message)
        return reply

    with gr.Blocks(title="Restaurant Reservation Assistant") as demo:
        gr.Markdown("# 🍽️ Restaurant Reservation Assistant")
        gr.Markdown("Book tables, cancel reservations, or ask about our menu and hours.")
        chatbot = gr.Chatbot(
            height=500,
        )
        textbox = gr.Textbox(
            placeholder="Type your message here...",
            lines=1,
            max_lines=1,
            show_label=False,
            container=False,
        )
        with gr.Row():
            submit_btn = gr.Button("Send")
            clear_btn = gr.Button("Clear")

        examples = gr.Examples(
            examples=[
                "Book a table for 4 tomorrow at 8:00 PM for Alex",
                "Cancel reservation #1",
                "What is on the menu?",
                "What are your hours?",
            ],
            inputs=[textbox],
        )

        def chat_submit(message, history):
            if not message or not message.strip():
                return history, ""
            reply = bot.answer(message)
            history = history or []
            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": reply})
            return history, ""

        submit_btn.click(
            chat_submit,
            inputs=[textbox, chatbot],
            outputs=[chatbot, textbox],
        )
        textbox.submit(
            chat_submit,
            inputs=[textbox, chatbot],
            outputs=[chatbot, textbox],
        )
        clear_btn.click(lambda: [], inputs=None, outputs=[chatbot])

    return demo


if __name__ == "__main__":
    print("Starting Gradio chatbot on http://127.0.0.1:7861/")
    bot = RestaurantChatbot()
    demo = build_gradio_ui(bot)
    demo.launch(server_name="127.0.0.1", server_port=7861, show_error=True, debug=False)
