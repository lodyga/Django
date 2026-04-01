import cohere
import json
from django.http import JsonResponse, StreamingHttpResponse
from codesite.auth.cohere_auth import COHERE_API_KEY


def get_cohere_response(request):
    user_message = request.POST.get("message")
    chat_history = request.session.get("chat_history", [])
    co = cohere.Client(COHERE_API_KEY)
    complete_response = {"text": ""}

    for event in co.chat_stream(
        model="command-a-03-2025",
        message=user_message,
        chat_history=chat_history,
    ):
        if event.event_type == "text-generation":
            print(event.text)
        elif event.event_type == "stream-end":
            print(event.finish_reason)
            complete_response = event.response
            chat_history.append({"role": "USER", "message": user_message})
            chat_history.append(
                {"role": "CHATBOT", "message": complete_response.text})

    request.session["chat_history"] = chat_history

    return JsonResponse({"response": complete_response.text})


def get_cohere_response_sse(request):
    user_message = request.GET.get("message") or request.POST.get("message")
    chat_history = request.session.get("chat_history", [])
    co = cohere.Client(COHERE_API_KEY)

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

    def event_stream():
        if not user_message:
            yield f"event: error"

        for event in co.chat_stream(
            model="command-a-03-2025",
            message=user_message,
            chat_history=chat_history,
        ):
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
