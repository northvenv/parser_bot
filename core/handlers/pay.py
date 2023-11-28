from aiogram import Bot
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery

async def order(message: Message, bot: Bot):
    await bot.send_invoice(
        chat_id=message.chat.id,
        title='Покупка через Telegram',
        description='Учимся принимать платежи через tg bot',
        payload='Payment through a bot',
        provider_token='test_r8drdG9OqRa7qGyQFXxuHyntS9mm2ybuxfhX6qvQhKA ',
        currency='rub', 
        prices=[ 
            LabeledPrice(
                label='Доступ к секретной информации',
                amount=999
            ),
            LabeledPrice(
                label='НДС',
                amount=99900
            ),
            LabeledPrice(
                label='Скидка',
                amount=-20000
            ),
            LabeledPrice(
                label='Бонус',
                amount=-40000
            )
        ],
        max_tip_amount=5000,
        suggested_tip_amounts=[1000, 2000, 5000],
        provider_data=None,
        photo_url='',
        photo_size=100,
        photo_height=450,
        photo_width=800,
        need_name=True,
        need_phone_number=True,
        need_email=True,
        need_shipping_address=False,
        send_email_to_provider=False,
        is_flexible=False,
        disable_notification=False,
        protect_content=False,
        reply_to_message_id=None,
        allow_sending_without_reply=True,
        reply_markup=None,
        request_timeout=15,
    )
    



async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=True, ok=True)

async def succesful_payment(message: Message):
    msg=f'Спасибо за покупку {message.successful_payment.total_amount // 100} {message.successful_payment.currency}.'
    await message.answer(msg)






