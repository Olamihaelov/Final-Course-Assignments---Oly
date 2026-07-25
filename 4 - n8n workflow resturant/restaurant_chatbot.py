import os
import json
import requests
import re
from typing import Optional

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from restaurant_db import (
    initialize_database,
    book_reservation,
    cancel_reservation,
    get_reservations,
)

class RestaurantChatbot:
    def __init__(self, db_path: str = "restaurant.db", llm: Optional[ChatOpenAI] = None):
        self.db_path = db_path
        initialize_database(self.db_path)
        self.llm = llm or ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY"),
        )

    def classify_question(self, question: str) -> str:
        """Use the LLM to classify the user's intent."""
        if not self.llm:
            return "general"

        fallback_category = self._fallback_category(question)
        if fallback_category != "general":
            return fallback_category

        classify_prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are a router for a restaurant chatbot. "
             "Classify the user message into exactly one of these categories:\n"
             "reservation - user wants to book a table\n"
             "cancellation - user wants to cancel an existing booking\n"
             "menu - questions about food, drinks, or prices\n"
             "hours - questions about opening hours or location\n"
             "general - anything else\n"
             "Return ONLY the single category word. No punctuation, no explanation."),
            ("human", "{question}")
        ])

        chain = classify_prompt | self.llm | StrOutputParser()
        try:
            result = chain.invoke({"question": question}).strip().lower()
        except Exception as error:
            print(f"Warning: Intent classification failed: {error}")
            return fallback_category
        
        valid = {"reservation", "cancellation", "menu", "hours", "general"}
        return result if result in valid else "general"

    @staticmethod
    def _fallback_category(question: str) -> str:
        """Classify common requests locally when the LLM is unavailable."""
        text = question.lower()
        if any(word in text for word in ("cancel", "cancellation")):
            return "cancellation"
        if any(word in text for word in ("reserve", "reservation", "book", "table")):
            return "reservation"
        if any(word in text for word in ("menu", "food", "drink", "price")):
            return "menu"
        if any(word in text for word in ("hour", "hours", "open", "opening", "location")):
            return "hours"
        return "general"

    def _handle_reservation(self, question: str) -> str:
        """Extract booking details with LLM, save to DB, notify n8n."""
        extract_prompt = ChatPromptTemplate.from_messages([
            ("system",
             "Extract reservation details from the message. "
             "Return ONLY valid JSON with keys: "
             "customer_name, date, time, party_size, contact. "
             "Use null for missing fields. No explanation. "
             "Do not wrap the JSON in markdown code blocks."),
            ("human", "{question}")
        ])

        if not self.llm:
            return "Please call us directly to make a reservation!"

        chain = extract_prompt | self.llm | StrOutputParser()
        try:
            raw = chain.invoke({"question": question})
        except Exception as error:
            print(f"Warning: Reservation detail extraction failed: {error}")
            return (
                "I need your name, date, time, and party size to book a table. "
                "Example: 'Table for 2 on Sunday at 7pm, name is Kim'"
            )

        raw = raw.strip()
        if raw.startswith("```json"):
            raw = raw[7:]
        if raw.startswith("```"):
            raw = raw[3:]
        if raw.endswith("```"):
            raw = raw[:-3]
        raw = raw.strip()

        try:
            details = json.loads(raw)
            required = ["customer_name", "date", "time", "party_size"]
            
            if not all(details.get(k) for k in required):
                return ("I need your name, date, time, and party size to book a table. "
                        "Example: 'Table for 2 on Friday at 7pm, name is Sara'")

            res_id = book_reservation(
                self.db_path,
                str(details["customer_name"]), 
                str(details["date"]),
                str(details["time"]), 
                int(details["party_size"]),
                str(details.get("contact")) if details.get("contact") else None
            )
            
            self._notify_n8n({**details, "id": res_id}, event="reservation")

            return (f"✅ Reservation confirmed!\n"
                    f"Name: {details['customer_name']}\n"
                    f"Date: {details['date']} at {details['time']}\n"
                    f"Party of {details['party_size']} · Booking #{res_id}")
                    
        except (json.JSONDecodeError, ValueError, TypeError):
            return "Sorry, I couldn't process that. Please try again."

    def _handle_cancellation(self, question: str) -> str:
        """Look for a booking ID in the message and cancel it."""
        match = re.search(r'\b(\d+)\b', question)
        if match:
            res_id = int(match.group(1))
            cancel_reservation(self.db_path, res_id)
            self._notify_n8n({"id": res_id}, event="cancellation")
            return f"Reservation #{res_id} has been cancelled."
        
        return "Please provide your booking ID number to cancel (e.g., 'Cancel booking 123')."

    def _handle_menu(self, question: str) -> str:
        """Stub for menu handling. Replace with RAG or static menu logic."""
        return "Our menu features delicious pasta, fresh salads, and amazing desserts. Please visit our website for the full menu."

    def _handle_hours(self, question: str) -> str:
        """Stub for hours handling."""
        return "We are open Monday to Sunday, from 10:00 AM to 10:00 PM."

    def _handle_general(self, question: str) -> str:
        """Fallback general response."""
        return "I'm here to help with reservations, menu questions, and opening hours. How can I assist you today?"

    def _notify_n8n(self, data: dict, event: str) -> None:
        """Fire-and-forget webhook to n8n. Never crashes the chatbot."""
        webhook_url = os.getenv("N8N_WEBHOOK_URL")
        if not webhook_url:
            print("Warning: N8N_WEBHOOK_URL not set. Skipping notification.")
            return
            
        try:
            requests.post(
                webhook_url,
                json={**data, "event": event},
                timeout=5
            )
        except Exception as e:
            print(f"Failed to notify n8n: {e}")

    def answer(self, question: str) -> str:
        """Main entry point for user questions. Routes to the correct handler."""
        category = self.classify_question(question)
        
        if category == "reservation":
            return self._handle_reservation(question)
        elif category == "cancellation":
            return self._handle_cancellation(question)
        elif category == "menu":
            return self._handle_menu(question)
        elif category == "hours":
            return self._handle_hours(question)
        else:
            return self._handle_general(question)


# --- Example Usage / Testing ---
if __name__ == "__main__":
    # Ensure you have OPENAI_API_KEY in your .env file
    from dotenv import load_dotenv
    load_dotenv()
    
    bot = RestaurantChatbot()
    
    print("Chatbot initialized. Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        
        response = bot.answer(user_input)
        print(f"Bot: {response}\n")
