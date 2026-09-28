from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from forms.user import Profile
import aiohttp
from aiogram.types import (Message,
                           ReplyKeyboardMarkup,
                           KeyboardButton,
                           InlineKeyboardButton,
                           InlineKeyboardMarkup,
                           CallbackQuery,
                           FSInputFile)



router = Router()


photo = FSInputFile("silly.jpg")
gif = FSInputFile("silly_gif.GIF")
video = FSInputFile("silly_vid.mov")
hi_gif = FSInputFile("hi_gif.GIF")


async def get_product(product_id: int):
    url = f"https://fakestoreapi.com/products/{product_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 404:
                return None
        data = await resp.json()
        return data


def get_main_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/start")],
            [KeyboardButton(text="/help"), KeyboardButton(text="/yo"), KeyboardButton(text="/repeat")],
            [KeyboardButton(text="/profile")],
            [KeyboardButton(text="/cat"), KeyboardButton(text="/gif"), KeyboardButton(text="/vid")],
        ],
        resize_keyboard=True,
    )
    return keyboard


def get_main_inline_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Start", callback_data="start")],
            [InlineKeyboardButton(text="Help", callback_data="help"),
             InlineKeyboardButton(text="Yo", callback_data="yo")],
            [InlineKeyboardButton(text="Profile", callback_data="profile")],
            [InlineKeyboardButton(text="Cat", callback_data="cat"),
             InlineKeyboardButton(text="GIF", callback_data="gif"),
             InlineKeyboardButton(text="Vid", callback_data="vid")]
        ],
    )
    return keyboard


@router.message(Command("cancel"))
async def cancel_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Profile was cancelled.")


@router.callback_query(lambda c: c.data == "start")
async def process_start(callback: CallbackQuery):
    await callback.message.answer("*Welcome to my testing bot!*\nI'm just tryng to test my skills and knowledge about tg bots.\n\n"
                         "Here is the commands in this bot:\n\n"
                         "*/start* - Show this message\n"
                         "*/help* - ?????\n"
                         "*/yo* - I'll say Hi to you\n"
                         "*/repeat* - I'll repeat your message\n"
                         "*/profile* - Make your profile\n"
                         "*/product* - Search random things from fake shop by num\n\n"
                         "*Secret* commands :OO\n\n"
                         "*/cat* - /&71$&$97????\n"
                         "*/gif* - !$(6$84)??????\n"
                         "*/vid* - $=$875§$?????????"
                         , parse_mode=ParseMode.MARKDOWN, reply_markup=get_main_reply_keyboard())
    await callback.answer()


@router.callback_query(lambda c: c.data == "help")
async def process_help(callback: CallbackQuery):
    await callback.message.answer("And WHY TF did you click that?..")
    await callback.answer()


@router.callback_query(lambda c: c.data == "yo")
async def process_yo(callback: CallbackQuery):
    await callback.message.answer(f"My greetings, {callback.from_user.full_name}")
    await callback.answer()


@router.callback_query(lambda c: c.data == "profile")
async def profile_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Lets create a profile!    (You cancel it with */cancel*)\nFirsly, enter your name:", parse_mode=ParseMode.MARKDOWN)
    await state.set_state(Profile.name)
    await callback.answer()


@router.callback_query(lambda c: c.data == "cat")
async def cat_command(callback: CallbackQuery):
    await callback.message.answer_photo(photo=photo, caption="Halo :D")
    await callback.answer()


@router.callback_query(lambda c: c.data == "gif")
async def gif_command(callback: CallbackQuery):
    await callback.message.answer_animation(animation=gif)
    await callback.answer()


@router.callback_query(lambda c: c.data == "vid")
async def vid_command(callback: CallbackQuery):
    await callback.message.answer_video(video=video)
    await callback.answer()


@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer("*Welcome to my testing bot!*\nI'm just tryng to test my skills and knowledge about tg bots.\n\n"
                         "Here is the commands in this bot:\n\n"
                         "*/start* - Show this message\n"
                         "*/help* - ?????\n"
                         "*/yo* - I'll say Hi to you\n"
                         "*/repeat* - I'll repeat your message\n"
                         "*/profile* - Make your profile\n"
                         "*/product* - Search random things from fake shop by num\n\n"
                         "*Secret* commands :OO\n\n"
                         "*/cat* - /&71$&$97????\n"
                         "*/gif* - !$(6$84)??????\n"
                         "*/vid* - $=$875§$?????????"
                         , parse_mode=ParseMode.MARKDOWN, reply_markup=get_main_reply_keyboard())


@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer("WYM \"HELP\"?? LOLL", reply_markup=get_main_inline_keyboard())


@router.message(Command("yo"))
async def yo_command(message: Message):
    await message.answer_animation(animation=hi_gif, caption=f"My greetings, {message.from_user.full_name}")


@router.message(Command("repeat"))
async def repeat_command(message: Message):
    text = message.text
    await message.answer(text)


@router.message(Command("profile"))
async def create_profile_command(message: Message, state: FSMContext):
    await message.answer("Lets create a profile!    (You cancel it with */cancel*)\nFirsly, enter your name:", parse_mode=ParseMode.MARKDOWN)
    await state.set_state(Profile.name)


@router.message(Profile.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Great!\nNow enter your age:")
    await state.set_state(Profile.age)


@router.message(Profile.age)
async def process_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Age must be a number!")
        return
    if not (1 <= int(message.text) <= 100):
        await message.answer("Age must be from 1 to 100!")
        return
    await state.update_data(age=message.text)
    await message.answer("Great!\nNow enter your gender (M/F/N):")
    await state.set_state(Profile.gender)


@router.message(Profile.gender)
async def process_gender(message: Message, state: FSMContext):
    if message.text.lower() not in ["m", "f", "n"]:
        await message.answer("Invalid gender)))))")
        return

    gender_map = {"m": "Melon", "f": "Fortnite", "n": "Nugget"}
    gender_key = message.text.lower()
    gender_label = gender_map[gender_key]

    await message.answer(f"Great, glad to hear that, {gender_label}!")
    await state.update_data(gender=gender_label)

    data = await state.get_data()
    await message.answer(
        f"Your profile is ready:\n\n"
        f"Name — {data['name']}\n"
        f"Age — {data['age']}\n"
        f"Gender — {data['gender']}"
    )
    await state.clear()


@router.message(Command("cat"))
async def cat_command(message: Message):
    await message.answer_photo(photo=photo, caption="Halo :D")


@router.message(Command("gif"))
async def gif_command(message: Message):
    await message.answer_animation(animation=gif)


@router.message(Command("vid"))
async def vid_command(message: Message):
    await message.answer_video(video=video)


@router.message(Command("product"))
async def product_command(message: Message):
    parts = message.text.strip().split(" ")

    if len(parts) != 2:
        await message.answer("Smth is wrong! Try: /product 1")

    product_id = parts[1]

    if not product_id.isdigit():
        await message.answer("Product id must be a number!")
        return

    await message.answer(f"Looking for {product_id}...")

    try:
        product = await get_product(int(product_id))
    except Exception:
        await message.answer("Server connection error.")
        return

    if product is None:
        await message.answer("Product not found.")
        return

    title = product.get("title", "No title")
    price = product.get("price", "—")
    desc = product.get("description", "No description")
    category = product.get("category", "No category")

    text = (
        f"<b>{title}</b>\n\n"
        f"Категория: <i>{category}</i>\n\n"
        f"Цена: <b>${price}</b>\n\n"
        f"{desc}"
    )

    await message.answer(text, parse_mode=ParseMode.HTML)


@router.message(Command("test"))
async def test_command(message: Message):
    pass


@router.message()
async def basic_message(message: Message):
    await message.answer("YOOO")