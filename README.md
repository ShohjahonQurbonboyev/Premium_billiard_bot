# 🎱 Premium Billiard Bot

Telegram bot billiard klub uchun mo‘ljallangan.
Bot orqali stol vaqtini hisoblash, mahsulot sotish, foyda va zarar (damage) hisoblash avtomatlashtirilgan.

---

## 🚀 Imkoniyatlar

- 🪑 Billiard stollarini boshqarish
- ⏱ Stol vaqtini avtomatik hisoblash
- 🛒 Stolga mahsulot qo‘shish
- 💰 Umumiy hisobni yopish
- 📈 Foyda (benefit) hisoblash
- 🧮 Zarar / tannarx (damage) hisoblash
- 📢 Hisob yopilganda kanalga xabar yuborish
- 🔐 FSM (state) orqali xavfsiz jarayonlar

---

## 🛠 Texnologiyalar

- Python 3.10+
- aiogram
- asyncpg
- PostgreSQL
- FSMContext
- Git / GitHub

---

## 📂 Loyiha tuzilishi

Premium_billiard/
├── handlers/
│ └── users/
├── keyboards/
│ ├── default/
│ └── inline/
├── states/
├── data/
│ └── config.py
├── utils/
│ └── calculations.py
├── loader.py
├── bot.py
├── requirements.txt
└── README.md
