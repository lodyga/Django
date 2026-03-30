import cohere
from django.http import JsonResponse
from codesite.auth.cohere_auth import COHERE_API_KEY

def get_cohere_response(request):
    user_message = request.POST.get("message")
    chat_history = request.session.get("chat_history", [])
    co = cohere.Client(COHERE_API_KEY)

    response = co.chat(
        model="command-a-03-2025",
        message=user_message,
        chat_history=chat_history,
    )

    chat_history.append({"role": "USER", "message": user_message})
    chat_history.append({"role": "CHATBOT", "message": response.text})    
    request.session["chat_history"] = chat_history

    return JsonResponse({"response": response.text})
