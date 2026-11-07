import os
import httpx
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from telegram import Update, InlineKeyboardButton as B, InlineKeyboardMarkup as M, WebAppInfo
from telegram.ext import Application, CommandHandler

load_dotenv()
E = os.environ
URL = E["SUPABASE_URL"].rstrip("/") + "/rest/v1/kv"
H = {"apikey": E["SUPABASE_KEY"], "Authorization": "Bearer " + E["SUPABASE_KEY"], "Content-Type": "application/json"}
bot = Application.builder().token(E["BOT_TOKEN"]).build()


async def start(u: Update, c):
    kb = M([[B("💎 Katalogni ochish", web_app=WebAppInfo(url=E["SITE_URL"]))]])
    await u.message.reply_text("GLASS-IDEAL_VITRAJ katalogiga xush kelibsiz!", reply_markup=kb)

bot.add_handler(CommandHandler("start", start))


@asynccontextmanager
async def life(app):
    await bot.initialize(); await bot.start(); await bot.updater.start_polling()
    yield
    await bot.updater.stop(); await bot.stop(); await bot.shutdown()

app = FastAPI(lifespan=life)


async def read():
    async with httpx.AsyncClient(timeout=15) as c:
        r = await c.get(URL, headers=H, params={"select": "*"})
        r.raise_for_status()
        return {x["k"]: x["v"] for x in r.json()}


@app.get("/")
async def home():
    return FileResponse("static/index.html")


@app.get("/api/kv")
async def get_kv():
    return await read()


@app.post("/api/kv")
async def set_kv(req: Request):
    data = await req.json()
    old = {o["id"] for o in (await read()).get("o", [])}
    rows = [{"k": k, "v": v} for k, v in data.items() if k in ("u", "p", "o", "d", "st")]
    async with httpx.AsyncClient(timeout=15) as c:
        r = await c.post(URL, headers={**H, "Prefer": "resolution=merge-duplicates"}, json=rows)
        r.raise_for_status()
    chat = E.get("ADMIN_CHAT_ID")
    if chat:
        for o in data.get("o", []):
            if o["id"] not in old:
                t = {"paid": "To'liq to'langan", "debt": "QARZGA", "debtpay": "Qarz to'lovi"}.get(o["type"], "")
                txt = f"🛒 Yangi zakaz ({t})\n{o['name']} {o['phone']}\n{o['region']} {o.get('address') or ''}\nSumma: {o['total']} so'm"
                try:
                    await bot.bot.send_message(chat, txt)
                except Exception:
                    pass
    return {"ok": True}


@app.post("/api/admin")
async def admin(req: Request):
    d = await req.json()
    return {"ok": d.get("user") == E["ADMIN_USER"] and d.get("pass") == E["ADMIN_PASS"]}
