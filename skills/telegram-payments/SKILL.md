---
name: telegram-payments
description: >-
  Implement Telegram Bot payments including Stars, invoices, pre_checkout_query,
  and successful_payment handlers. Use when adding paid features, donations,
  or digital goods to a bot.
---

# Telegram Payments

Telegram supports **Telegram Stars** (XTR) and traditional provider-based payments.

## Payment flow (required order)

1. Bot sends invoice (`send_invoice` or `sendInvoice`)
2. User opens payment UI
3. Bot receives **`pre_checkout_query`** — must answer within ~10 seconds
4. On success, bot receives **`successful_payment`** message
5. Deliver goods **only after** `successful_payment`, never after pre-checkout alone

## Stars (recommended for digital goods)

- Currency code: `XTR`
- Provider token: empty string `""` for Stars
- No external payment provider needed

```python
from aiogram.types import LabeledPrice

await bot.send_invoice(
    chat_id=chat_id,
    title="Premium access",
    description="30 days premium",
    payload=f"premium:{user_id}:{plan_id}",  # your internal id, max 128 bytes
    provider_token="",  # empty for Stars
    currency="XTR",
    prices=[LabeledPrice(label="Premium", amount=100)],  # 100 Stars
)
```

## pre_checkout_query handler (critical)

```python
@router.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery):
    # Validate payload, stock, user eligibility
    if not is_valid_payload(query.invoice_payload):
        await query.answer(ok=False, error_message="Offer expired")
        return
    await query.answer(ok=True)
```

## successful_payment handler

```python
@router.message(F.successful_payment)
async def on_payment(message: Message):
    payment = message.successful_payment
    # Idempotent grant: check if telegram_payment_charge_id already processed
    await grant_access(
        user_id=message.from_user.id,
        charge_id=payment.telegram_payment_charge_id,
        payload=payment.invoice_payload,
    )
```

## Idempotency rules

- Store `telegram_payment_charge_id` before granting access
- Duplicate `successful_payment` deliveries must not double-grant
- Payload should encode product + user; validate server-side, never trust client

## Refunds

- Stars refunds via Bot API `refundStarPayment`
- Keep audit log of charge IDs

## Testing

- Use Telegram test environment when available
- Test: valid pay, rejected pre_checkout, duplicate payment callback, expired payload

## Anti-patterns

- Granting access on `pre_checkout_query` alone
- Missing timeout handling on pre_checkout (user sees spinner forever)
- Hardcoded prices without server-side validation
- Storing card data (Telegram handles PCI; you never touch cards)
