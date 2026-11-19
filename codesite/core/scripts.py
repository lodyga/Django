import cohere
import json
import os
from google import genai
from mistralai.client import Mistral
from django.http import JsonResponse, StreamingHttpResponse


COHERE_API_KEY = os.getenv("COHERE_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")


def test_cohere_connection():
    if not COHERE_API_KEY:
        return False, "COHERE_API_KEY is not configured"

    co = cohere.Client(COHERE_API_KEY)
    co.chat(
        model="command-a-03-2025",
        message="Reply with OK.",
        max_tokens=5,
    )
    return True, "Connected"


def test_gemini_connection():
    if not GEMINI_API_KEY:
        return False, "GEMINI_API_KEY is not configured"

    client = genai.Client(api_key=GEMINI_API_KEY)
    client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Reply with OK.",
    )
    return True, "Connected"


def test_mistral_connection():
    if not MISTRAL_API_KEY:
        return False, "MISTRAL_API_KEY is not configured"

    client = Mistral(api_key=MISTRAL_API_KEY)
    client.chat.complete(
        model="codestral-latest",
        messages=[{"role": "user", "content": "Reply with OK."}],
        max_tokens=5,
    )
    return True, "Connected"


def format_sse(data, event=None):
    data = (data or "").replace("\r", "")
    lines = data.split("\n")
    payload_lines = []
    if event:
        payload_lines.append(f"event: {event}")
    for line in lines:
        # No space after ":" to preserve leading spaces in data
        payload_lines.append(f"data:{line}")
    return "\n".join(payload_lines) + "\n\n"


def get_cohere_response(request):
    # Cohere: Command
    user_message = request.GET.get("message")
    chat_history = request.session.get("chat_history", [])
    co = cohere.Client(COHERE_API_KEY)

    def event_stream():
        if not user_message:
            yield f"event: error"

        stream = co.chat_stream(
            model="command-a-03-2025",
            message=user_message,
            chat_history=chat_history,
        )

        for event in stream:
            if event.event_type == "text-generation":
                yield f"data:{event.text} \n\n"
            elif event.event_type == "stream-end":
                complete_response = event.response
                chat_history.append({"role": "USER", "message": user_message})
                chat_history.append(
                    {"role": "CHATBOT", "message": complete_response.text})
                request.session["chat_history"] = chat_history
                # Send final, full text as JSON so newlines are preserved safely
                final_text = (complete_response.text or "").replace("\r", "")
                payload = json.dumps({"final": final_text})
                yield format_sse(payload, event="done")

    response = StreamingHttpResponse(
        event_stream(),
        content_type="text/event-stream",
    )
    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"
    return response


def get_gemini_response(request):
    user_message = request.GET.get("message")

    client = genai.Client(api_key=GEMINI_API_KEY)

    def event_stream():
        if not user_message:
            yield "event: error\n\n"
            return

        tokens = []

        stream = client.interactions.create(
            model="gemini-2.5-flash",
            input=user_message,
            stream=True,
        )

        for chunk in stream:
            if chunk.event_type == "step.delta":
                delta = ""

                if chunk.delta.type == "text":
                    delta = chunk.delta.text

                if delta:
                    tokens.append(delta)
                    yield f"data:{delta}\n\n"

            elif chunk.event_type == "interaction.completed":
                break

        payload = json.dumps({"final": "".join(tokens)})
        yield format_sse(payload, event="done")

    response = StreamingHttpResponse(
        event_stream(),
        content_type="text/event-stream",
    )
    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"
    return response


def get_mistral_response(request):
    # Mistral: Medium
    # Codestral
    # "role": "user", "assistant"
    user_message = request.GET.get("message")
    model = "mistral-medium-latest"
    model = "codestral-latest"
    client = Mistral(api_key=MISTRAL_API_KEY)

    messages = [
        {
            "role": "user",
            "content": user_message,
        },
    ]

    def event_stream():
        if not user_message:
            yield "event: error\n\n"
            return

        tokens = []
        # llm = client.chat
        stream = client.chat.stream(
            model=model,
            messages=messages
        )

        for chunk in stream:
            delta = None
            if hasattr(chunk, "choices"):
                delta = chunk.choices[0].delta.content
            elif hasattr(chunk, "data"):
                delta = chunk.data.choices[0].delta.content

            if delta:
                tokens.append(delta)
                yield f"data:{delta}\n\n"

        payload = json.dumps({"final": "".join(tokens)})
        yield format_sse(payload, event="done")

    response = StreamingHttpResponse(
        event_stream(),
        content_type="text/event-stream",
    )
    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"
    return response
