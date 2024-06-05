import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from generate_data import (
    generate_text_message,
    generate_filtered_list,
    remove_sent,
)
from aux_tools import read_json, write_json

# Basic definitions
token = "placeholder_token"
my_chat_id = 123456789
group_chat_id = -123456789
global_sent_planes = dict()


# Commands
async def start_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "¡Hola! Este bot avisa de aviones que aterricen o despeguen del Aeropuerto de Vitoria (LEVT/VIT). Para recibir mensajes, únete al grupo LEVTradar https://t.me/+cOPgU047NjRkMWE0."
    )


async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Para recibir notificaciones de este bot, únete al grupo LEVTradar https://t.me/+cOPgU047NjRkMWE0."
    )


async def blacklist_command(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_message.chat_id
    if chat_id == my_chat_id:
        try:
            flnum = str(context.args[0]).upper()
        except IndexError:
            await update.message.reply_text(
                "No se ha proporcionado ningún código de vuelo."
            )
        else:
            blacklist = read_json("false_positive_callsigns")
            if flnum in blacklist:
                await update.message.reply_text(
                    "El código " + flnum + " ya está en la lista."
                )
            else:
                blacklist.append(flnum)
                await update.message.reply_text(
                    "Se ha añadido el código " + flnum + " a la lista."
                )
                write_json("false_positive_callsigns", blacklist)


async def whitelist_command(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_message.chat_id
    if chat_id == my_chat_id:
        try:
            flnum = str(context.args[0]).upper()
        except IndexError:
            await update.message.reply_text(
                "No se ha proporcionado ningún código de vuelo."
            )
        else:
            blacklist = read_json("false_positive_callsigns")
            if flnum in blacklist:
                blacklist.remove(flnum)
                await update.message.reply_text(
                    "Se ha eliminado el código " + flnum + " de la lista."
                )
                write_json("false_positive_callsigns", blacklist)
            else:
                await update.message.reply_text(
                    "El código " + flnum + " no está en la lista."
                )


# Errors
async def error(update: Update, context: CallbackContext) -> None:
    logging.warning(f"Update {update} caused error {context.error}")


# Generate text messages and send them
async def send_planes(context: CallbackContext) -> None:
    chat_id = context.job.chat_id
    all_plane_list = generate_filtered_list()
    global global_sent_planes
    old_global_sent_planes = global_sent_planes
    revised_plane_list, global_sent_planes = remove_sent(
        all_plane_list, old_global_sent_planes
    )
    if len(revised_plane_list) > 0:
        logging.warning("Message sent")
        await context.bot.send_message(
            chat_id=chat_id, text=generate_text_message(revised_plane_list)
        )


# Main function
def main() -> None:
    app = Application.builder().token(token).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("blacklist", blacklist_command))
    app.add_handler(CommandHandler("whitelist", whitelist_command))

    # Errors
    app.add_error_handler(error)

    # Starts sending messages to the groupchat
    app.job_queue.run_repeating(send_planes, chat_id=group_chat_id, interval=4)

    # Polls the bot
    app.run_polling()


# Run the main function
main()
