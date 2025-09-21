import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, ConversationHandler

import os
TOKEN = os.getenv("TOKEN")

ESCOLHER_RACA, ESCOLHER_ORIGEM = range(2)

# Raças
racas = {
    "Humano": {"bonus": {"Intelecto": 1, "Agilidade": 1}, "defesa": {"fisica": 1, "magica": 0}, "vida": 8, "eter": 6, "stamina": 5},
    "Elfo": {"bonus": {"Intelecto": 2}, "defesa": {"fisica": -1, "magica": 3}, "vida": 6, "eter": 10, "stamina": 3},
    "Orc": {"bonus": {"Força": 2}, "defesa": {"fisica": 3, "magica": -2}, "vida": 10, "eter": 4, "stamina": 7},
    "Goblin": {"bonus": {"Agilidade": 3}, "defesa": {"fisica": -2, "magica": 2}, "vida": 4, "eter": 3, "stamina": 3},
    "Ciclope": {"bonus": {"Força": 3}, "defesa": {"fisica": 4, "magica": 0}, "vida": 10, "eter": 7, "stamina": 9},
    "Feral": {"bonus": {"Força": 1, "Agilidade": 2}, "defesa": {"fisica": -1, "magica": 2}, "vida": 7, "eter": 7, "stamina": 7},
    "Anão": {"bonus": {"Força": 2}, "defesa": {"fisica": 3, "magica": 0}, "vida": 8, "eter": 5, "stamina": 7},
    "Golem": {"bonus": {"Força": 4}, "defesa": {"fisica": 5, "magica": -2}, "vida": 15, "eter": 8, "stamina": 10},
    "Insectoide": {"bonus": {"Intelecto": 2, "Agilidade": 1}, "defesa": {"fisica": -2, "magica": 3}, "vida": 3, "eter": 6, "stamina": 5},
    "Tritão": {"bonus": {"Intelecto": 2, "Agilidade": 1}, "defesa": {"fisica": 1, "magica": 2}, "vida": 6, "eter": 7, "stamina": 5}
}

# Origens
origens = {
    "Bandido": {"Visão": 1, "Audição": 1, "Tato": 2},
    "Burguês": {"Audição": 1, "Tato": 2, "Fala": 1},
    "Camponês": {"Visão": 1, "Audição": 1, "Tato": 3},
    "Nobre": {"Audição": 1, "Tato": 1, "Fala": 1},
    "Mercenário": {"Visão": 2, "Audição": 1, "Tato": 1},
    "Ferreiro": {"Visão": 2, "Tato": 2},
    "Explorador": {"Visão": 1, "Audição": 1, "Tato": 1, "Olfato": 1},
    "Ninja": {"Visão": 2, "Audição": 1, "Tato": 1},
    "Assassino": {"Visão": 2, "Tato": 2},
    "Pirata": {"Visão": 1, "Tato": 2, "Fala": 1},
    "Sacerdote": {"Visão": 1, "Audição": 1, "Tato": 1, "Fala": 1},
    "Monge": {"Visão": 1, "Audição": 2, "Tato": 1},
    "Músico": {"Audição": 2, "Tato": 2},
    "Cozinheiro": {"Tato": 1, "Olfato": 3}
}

def gerar_personagem(raca_nome, origem_nome):
    raca = racas[raca_nome]
    origem = origens[origem_nome]

    # Atributos
    atributos = {"Força": 0, "Intelecto": 0, "Agilidade": 0}
    for atr, val in raca["bonus"].items():
        atributos[atr] += val

    # Sentidos
    sentidos = {"Visão": 0, "Audição": 0, "Tato": 0, "Fala": 0, "Olfato": 0, "Adução": 0}
    for s, val in origem.items():
        sentidos[s] += val
    sentidos["SG"] = sum(sentidos.values()) // 5

    # Defesa
    defesa_fisica = 10 + raca["defesa"]["fisica"]
    defesa_magica = 10 + raca["defesa"]["magica"]

    # Vida, Éter e Estamina
    vida_max = atributos.get("Força",0) * 3 + raca["vida"]
    eter_max = atributos.get("Intelecto",0) * 3 + raca["eter"]
    estamina_max = atributos.get("Agilidade",0) * 3 + raca["stamina"]

    personagem = f"""
🎲 Personagem Gerado 🎲
Raça: {raca_nome}
Origem: {origem_nome}

❤️ Vida Máx: {vida_max}
🔮 Éter Máx: {eter_max}
⚡ Estamina Máx: {estamina_max}

📊 Atributos Básicos:
- Força: {atributos['Força']}
- Intelecto: {atributos['Intelecto']}
- Agilidade: {atributos['Agilidade']}

👀 Sentidos:
- Visão: {sentidos['Visão']}
- Audição: {sentidos['Audição']}
- Tato: {sentidos['Tato']}
- Fala: {sentidos['Fala']}
- Olfato: {sentidos['Olfato']}
- SG: {sentidos['SG']}

🛡️ Defesa Natural:
- Física: {defesa_fisica}
- Mágica: {defesa_magica}
"""
    return personagem

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teclado = [[InlineKeyboardButton(r, callback_data=r)] for r in racas.keys()]
    await update.message.reply_text(
        "Olá! Escolha a raça do personagem:",
        reply_markup=InlineKeyboardMarkup(teclado)
    )
    return ESCOLHER_RACA

async def escolher_raca(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['raca'] = query.data

    teclado = [[InlineKeyboardButton(o, callback_data=o)] for o in origens.keys()]
    await query.edit_message_text(
        text="Agora escolha a origem do personagem:",
        reply_markup=InlineKeyboardMarkup(teclado)
    )
    return ESCOLHER_ORIGEM

async def escolher_origem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['origem'] = query.data

    personagem = gerar_personagem(context.user_data['raca'], context.user_data['origem'])
    await query.edit_message_text(personagem)
    return ConversationHandler.END

async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Criação de personagem cancelada.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ESCOLHER_RACA: [CallbackQueryHandler(escolher_raca)],
            ESCOLHER_ORIGEM: [CallbackQueryHandler(escolher_origem)]
        },
        fallbacks=[CommandHandler('cancelar', cancelar)]
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == '__main__':
    main()

