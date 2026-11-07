GLASS-IDEAL_VITRAJ - sayt + bot + baza (bitta loyiha)

PAPKA:
 server.py        - server: saytni beradi, bazaga ulanadi, Telegram botni ishga tushiradi
 static/index.html- sayt
 .env.example     - sozlamalar namunasi  ->  ".env" deb nusxalab to'ldiring
 supabase_setup.sql, requirements.txt, Procfile

KOMPYUTERDA SINASH:
 1. supabase.com da loyiha oching, SQL Editor da supabase_setup.sql ni RUN qiling.
 2. .env.example ni .env ga nusxalang va to'ldiring (SUPABASE_KEY = service_role).
 3. pip install -r requirements.txt
 4. uvicorn server:app --port 8000   ->  brauzerda http://localhost:8000
    (Telegram uchun HTTPS kerak, shuning uchun 5-qadamga o'ting)

INTERNETGA JOYLASH (Render.com yoki Railway.app, bepul tarif):
 5. Papkani GitHub ga yuklang (.env yuklanmaydi), Render da "New Web Service" tanlang.
    Build: pip install -r requirements.txt
    Start: uvicorn server:app --host 0.0.0.0 --port $PORT
    Environment bo'limiga .env dagi qiymatlarni kiriting. SITE_URL = Render bergan manzil.
 6. Telegramda botga /start yozing - katalog tugmasi chiqadi.

Admin: .env dagi ADMIN_USER / ADMIN_PASS bilan kirasiz.
