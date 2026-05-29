import teto

# 토큰을 여기에 입력하세요 (절대 공유하지 마세요)
TOKEN = "YOUR_TOKEN_HERE"

bot = teto.Bot(token=TOKEN)


@bot.event
async def on_ready(user):
    print(f"Logged in as {user['username'] if user else 'unknown'}")


@bot.event
async def on_chat(msg):
    print(f"[chat] {msg}")


@bot.event
async def on_social_dm(msg):
    print(f"[DM] {msg}")


bot.run()
