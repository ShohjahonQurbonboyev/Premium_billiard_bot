from datetime import datetime
from zoneinfo import ZoneInfo
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.units import mm
from loader import db










def now_tashkent():
    return datetime.now(ZoneInfo("Asia/Tashkent"))



def calculate_play_time(start_time, end_time, price ):

    
    start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

    duration = (end_time - start_time).total_seconds()
    duration_minutes = duration / 60
    cost = (duration_minutes / 60) * int(price)

    return duration_minutes, cost



def calculate_benefit(products, nakladnoy):
    total_benefit = 0

    for prod in products:
        prod_name = prod[1]          # product_name
        sold_qty = int(prod[4])      # product_number
        sold_price = int(prod[5])    # jami sotilgan summa

        for nak in nakladnoy:
            if nak[1] == prod_name:
                original_price = int(nak[3])  # 1 dona original price
                cost_price = original_price * sold_qty

                benefit = sold_price - cost_price
                total_benefit += benefit

                break

    return total_benefit




def calculate_benefit_sell(sold_products: dict, nakladnoy_list: list) -> int:
    benefit = 0

    for name, qty in sold_products.items():
        for nak in nakladnoy_list:
            if nak[1] == name:
                original_price = int(nak[3])
                sell_price = int(nak[4])
                benefit += (sell_price - original_price) * qty

    return benefit


async def calculate_damage_for_add(product_name: str, qty: int = 1):
    naklad = await db.select_nakladnoy(product_name=product_name)
    if not naklad:
        return 0

    cost_price = int(naklad[3])  # tannarx
    return cost_price * qty




def money_format(amount: int | str) -> str:
    return f"{int(amount):,}".replace(",", ".")





def generate_accounting_pdf(user, file_path):
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    # ------------------------
    # Fon va sarlavha
    # ------------------------
    c.setFillColor(colors.HexColor("#1F4E78"))  # Chiroyli ko'k rang
    c.rect(0, height-60, width, 60, fill=True, stroke=False)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 45, "📄 Buxgalteriya Hisoboti")

    # ------------------------
    # Foydalanuvchi ma'lumotlari
    # ------------------------
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 14)
    y = height - 100
    line_height = 20

    c.drawString(50, y, "Foydalanuvchi ma'lumotlari:")
    y -= line_height

    c.setFont("Helvetica", 12)
    c.drawString(70, y, f"Ism: {user[1]}")
    y -= line_height
    c.drawString(70, y, f"Username: {user[2]}")
    y -= line_height
    c.drawString(70, y, f"Telegram ID: {user[3]}")
    y -= line_height


    c.drawString(70, y, f"Sana : {now_tashkent().strftime('%Y-%m-%d %H:%M:%S')}")
    y -= line_height

    # Chiziq bilan bo'lim ajratish
    c.setStrokeColor(colors.HexColor("#1F4E78"))
    c.setLineWidth(1)
    c.line(50, y, width-50, y)
    y -= line_height

    # ------------------------
    # Hisobot bo‘limi
    # ------------------------
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Hisobot ma'lumotlari:")
    y -= line_height

    c.setFont("Helvetica", 12)

    # Bazadan kelayotgan qiymatlar string bo'lishi mumkin
    def safe_int(val):
        try:
            return int(val)
        except:
            return 0

    total_stol_profit = safe_int(user[4])
    total_product_profit = safe_int(user[5])
    total_income = safe_int(user[6])
    evening_rate = safe_int(user[7])
    day_rate = safe_int(user[8])
    total_seen_profit = safe_int(user[9])
    total_expense = safe_int(user[10])
    
    net_profit = total_income - total_expense
    profit_percent = (net_profit / total_income * 100) if total_income > 0 else 0

    c.drawString(70, y, f"Umumiy stoldan kelgan kirim/foyda: {total_stol_profit:,} so'm")
    y -= line_height
    c.drawString(70, y, f"Umumiy productdan kelgan kirim: {total_product_profit:,} so'm")
    y -= line_height
    c.drawString(70, y, f"Umumiy kirim: {total_income:,} so'm")
    y -= line_height
    c.drawString(70, y, f"Umumiy ko'rilgan foyda: {total_seen_profit:,} so'm")
    y -= line_height
    c.drawString(70, y, f"Umumiy xarajat summasi: {total_expense:,} so'm")
    y -= line_height
    c.drawString(70, y, f"Sof foyda: {net_profit:,} so'm")
    y -= line_height
    c.drawString(70, y, f"Umumiy foyda foizi: {profit_percent:.2f}%")
    y -= line_height
    c.drawString(70, y, f"Kechki stavka: {evening_rate:,} so'm")
    y -= line_height
    c.drawString(70, y, f"Kunduzgi stavka: {day_rate:,} so'm")
    y -= line_height

    # ------------------------
    # Footer
    # ------------------------
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(colors.gray)
    c.drawString(50, 30, "Hisobot Premium Billiard tizimi tomonidan tayyorlandi")

    c.save()


