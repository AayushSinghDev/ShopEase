import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from .models import ChatLog


def chat_send(request):
    """POST /chatbot/send/ — receives JSON {message: ...}, returns JSON {reply: ...}"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    # Parse JSON body
    try:
        body = json.loads(request.body)
        user_message = body.get('message', '').strip()
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'reply': 'Invalid request format.'}, status=400)

    if not user_message:
        return JsonResponse({'reply': 'Please type a message.'}, status=400)

    # Gather user context from session
    user_role = request.session.get('user_role', 'guest')
    user_id = request.session.get('user_id')
    user_name = request.session.get('user_name', 'Guest')
    session_key = request.session.session_key or 'anonymous'

    # Fetch recent orders if customer
    orders_summary = 'No recent orders'
    if user_role == 'customer' and user_id:
        try:
            from orders.models import Order
            recent = Order.objects.filter(
                customer_id=user_id
            ).prefetch_related('items').order_by('-created_at')[:3]

            if recent.exists():
                lines = []
                for o in recent:
                    item_names = ', '.join(i.product_name for i in o.items.all())
                    lines.append(
                        f"Order #{o.pk}: {item_names} — Status: {o.status} — ₹{o.total}"
                    )
                orders_summary = '\n'.join(lines)
        except Exception:
            orders_summary = 'Unable to fetch orders'

    # Build system prompt
    system_prompt = f"""You are ShopEase Assistant, a helpful AI customer service agent for ShopEase — an online shopping platform.

User context:
- Role: {user_role}
- Name: {user_name}
- Recent orders: {orders_summary}

You can help with:
1. Order status queries — tell users about their order status from context provided
2. Product search help — suggest products based on user queries
3. Return/refund policy — standard 7-day return policy for unused items
4. Account help — guide users to profile/settings pages
5. Discount code help — explain how to apply codes at checkout
6. General FAQs about ShopEase

Keep responses concise, friendly, and helpful. Use bullet points when listing multiple items.
If user asks about specific order details not in context, ask them to check /orders/my-orders/ page.
Always respond in the same language the user writes in (Hindi or English)."""

    # Call Anthropic Claude API
    reply = _call_claude(system_prompt, user_message)

    # Save to ChatLog
    ChatLog.objects.create(
        session_key=session_key,
        user_role=user_role if user_role != 'guest' else None,
        user_id=user_id,
        user_message=user_message,
        bot_response=reply,
    )

    return JsonResponse({'reply': reply})


def _call_claude(system_prompt, user_message):
    """Internal helper — calls Anthropic API and returns reply text."""
    try:
        import anthropic
        api_key = getattr(settings, 'ANTHROPIC_API_KEY', '')
        if not api_key or api_key == 'your-api-key-here':
            return "⚠️ ShopEase Assistant is not configured yet. Please contact support."

        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=500,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        return response.content[0].text

    except ImportError:
        return "⚠️ AI library not installed. Run: pip install anthropic"
    except Exception as e:
        error_str = str(e).lower()
        if 'authentication' in error_str or 'api_key' in error_str or 'invalid' in error_str:
            return "⚠️ Invalid API key. Please check your Anthropic API key in settings."
        elif 'rate' in error_str:
            return "I'm a bit busy right now. Please try again in a moment! 🙏"
        else:
            return "I'm having trouble connecting right now. Please try again in a moment."


def chat_logs(request):
    """Admin-only view to browse all chat logs."""
    if request.session.get('user_role') != 'admin':
        return redirect('/accounts/login/')

    logs = ChatLog.objects.all()[:100]
    return render(request, 'chatbot/logs.html', {'logs': logs})
