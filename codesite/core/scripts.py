import cohere
import json
from cerebras.cloud.sdk import Cerebras
from google import genai
from mistralai.client import Mistral
from codesite.auth.ai_auth import *
from django.http import JsonResponse, StreamingHttpResponse


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


def get_cerberas_response(request, model_name):
    # Cerebras:
    model_map = {
        "gpt": "gpt-oss-120b",
        "zai": "zai-glm-4.7",
        "llama": "llama3.1-8b",
        "qwen": "qwen-3-235b-a22b-instruct-2507",
    }
    model = model_map.get(model_name, model_map["gpt"])

    user_message = request.GET.get("message") or request.POST.get("message")
    client = Cerebras(api_key=CERBERAS_API_KEY)
    messages = [
        {
            "role": "user",
            "content": user_message,
        }
    ]

    def event_stream():
        if not user_message:
            yield "event: error\n\n"
            return

        tokens = []
        stream = client.chat.completions.create(
            messages=messages,
            model=model,
            stream=True,
        )
        # chunk.choices[0].delta.content or "", end=""
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


def get_cohere_response(request):
    # Cohere: Command
    user_message = request.GET.get("message") or request.POST.get("message")
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
    # google.genai.errors.ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}
    # Google: Gemini Flash 2.5
    user_message = request.GET.get("message") or request.POST.get("message")

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
            if chunk.event_type == "content.delta":
                if chunk.delta.type == "text":
                    delta = chunk.delta.text
                elif chunk.delta.type == "thought_summary":
                    delta = getattr(chunk.delta.content, "text", "")
                else:
                    delta = ""

                if delta:
                    tokens.append(delta)
                    yield f"data:{delta}\n\n"
            elif chunk.event_type == "interaction.complete":
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
    user_message = request.GET.get("message") or request.POST.get("message")
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
