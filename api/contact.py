"""
api/contact.py — Spectra Media AI contact form handler
Uses Mailjet API. Credentials loaded from Vercel environment variables:
  MJ_API_KEY
  MJ_SECRET_KEY
"""

import json
import os
import re
from http.server import BaseHTTPRequestHandler

RECIPIENT_EMAIL = "contact@spectramedia.online"
RECIPIENT_NAME = "Spectra Media AI"

PROJECT_LABELS = {
    "mybetty_fr": "MyBetty AI — France",
    "mybetty_us": "MyBetty AI — United States",
    "ai_website": "AI Website (Custom)",
    "automation": "AI Automation / Integration",
    "other": "Other",
}


def is_valid_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))


def send_via_mailjet(name: str, company: str, email: str, project_type: str, message: str) -> dict:
    import urllib.request

    mj_api_key = os.environ.get("MJ_API_KEY", "")
    mj_secret_key = os.environ.get("MJ_SECRET_KEY", "")

    if not mj_api_key or not mj_secret_key:
        raise ValueError("Mailjet credentials not configured")

    project_label = PROJECT_LABELS.get(project_type, project_type)

    html_body = f"""
    <div style="font-family: 'DM Sans', Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #05060d; color: #f0f2f8; padding: 40px; border-radius: 16px;">
      <div style="margin-bottom: 32px; padding-bottom: 24px; border-bottom: 1px solid rgba(255,255,255,0.1);">
        <div style="font-size: 11px; letter-spacing: 0.12em; text-transform: uppercase; color: #3dd6f5; margin-bottom: 8px;">⬡ Spectra Media AI</div>
        <h1 style="font-size: 24px; font-weight: 800; margin: 0;">New Project Inquiry</h1>
      </div>

      <table style="width: 100%; border-collapse: collapse;">
        <tr style="border-bottom: 1px solid rgba(255,255,255,0.07);">
          <td style="padding: 12px 0; font-size: 12px; text-transform: uppercase; letter-spacing: 0.1em; color: #4d5669; width: 140px;">From</td>
          <td style="padding: 12px 0; font-size: 15px; font-weight: 600;">{name}</td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(255,255,255,0.07);">
          <td style="padding: 12px 0; font-size: 12px; text-transform: uppercase; letter-spacing: 0.1em; color: #4d5669;">Company</td>
          <td style="padding: 12px 0; font-size: 15px;">{company or "—"}</td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(255,255,255,0.07);">
          <td style="padding: 12px 0; font-size: 12px; text-transform: uppercase; letter-spacing: 0.1em; color: #4d5669;">Email</td>
          <td style="padding: 12px 0; font-size: 15px;"><a href="mailto:{email}" style="color: #3dd6f5;">{email}</a></td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(255,255,255,0.07);">
          <td style="padding: 12px 0; font-size: 12px; text-transform: uppercase; letter-spacing: 0.1em; color: #4d5669;">Project</td>
          <td style="padding: 12px 0;">
            <span style="background: rgba(61,214,245,0.12); border: 1px solid rgba(61,214,245,0.25); color: #3dd6f5; font-size: 12px; padding: 4px 12px; border-radius: 100px;">{project_label}</span>
          </td>
        </tr>
      </table>

      <div style="margin-top: 24px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.07); border-radius: 12px; padding: 24px;">
        <div style="font-size: 12px; text-transform: uppercase; letter-spacing: 0.1em; color: #4d5669; margin-bottom: 12px;">Message</div>
        <div style="font-size: 15px; line-height: 1.7; color: #8892a4; white-space: pre-wrap;">{message}</div>
      </div>

      <div style="margin-top: 32px; text-align: center; font-size: 12px; color: #4d5669;">
        Spectra Media AI · contact@spectramedia.online
      </div>
    </div>
    """

    text_body = f"""New inquiry from spectramedia.online

From: {name}
Company: {company or "—"}
Email: {email}
Project: {project_label}

Message:
{message}

---
Spectra Media AI
"""

    payload = {
        "Messages": [
            {
                "From": {"Email": "contact@spectramedia.online", "Name": "Spectra Media AI Website"},
                "To": [{"Email": RECIPIENT_EMAIL, "Name": RECIPIENT_NAME}],
                "ReplyTo": {"Email": email, "Name": name},
                "Subject": f"[Spectra] New inquiry from {name} — {project_label}",
                "TextPart": text_body,
                "HTMLPart": html_body,
            }
        ]
    }

    import base64
    credentials = base64.b64encode(f"{mj_api_key}:{mj_secret_key}".encode()).decode()

    req = urllib.request.Request(
        "https://api.mailjet.com/v3.1/send",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length)

        try:
            body = json.loads(raw_body.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self._respond(400, {"success": False, "error": "Invalid JSON"})
            return

        # Validate required fields
        name = (body.get("name") or "").strip()
        email = (body.get("email") or "").strip()
        project_type = (body.get("project_type") or "").strip()
        message = (body.get("message") or "").strip()
        company = (body.get("company") or "").strip()

        if not name:
            self._respond(400, {"success": False, "error": "Name is required"})
            return
        if not email or not is_valid_email(email):
            self._respond(400, {"success": False, "error": "Valid email is required"})
            return
        if not project_type:
            self._respond(400, {"success": False, "error": "Project type is required"})
            return
        if not message or len(message) < 10:
            self._respond(400, {"success": False, "error": "Message must be at least 10 characters"})
            return

        try:
            send_via_mailjet(name, company, email, project_type, message)
            self._respond(200, {"success": True, "message": "Email sent successfully"})
        except ValueError as ve:
            self._respond(500, {"success": False, "error": str(ve)})
        except Exception as e:
            self._respond(500, {"success": False, "error": "Failed to send email. Please try again."})

    def _respond(self, status: int, data: dict):
        self.send_response(status)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def log_message(self, format, *args):
        pass  # Suppress default logging on Vercel
