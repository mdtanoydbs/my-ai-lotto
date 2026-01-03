import streamlit as st
import yfinance as yf
import re
from collections import Counter

# 1. ตั้งค่าหน้าเว็บแบบกว้าง
st.set_page_config(page_title="AI Lotto Analytics Pro", layout="wide")

# 2. ฟังก์ชันช่วยแสดงผลตาราง 64 ชุด
def display_table(res, highlights, color="#D1C4E9"):
    html_code = f'<table style="width:100%; border-collapse: collapse;">'
    for i in range(0, len(res), 8):
        row_items = res[i:i+8]
        html_code += '<tr>'
        for item in row_items:
            bg_color = color if item in highlights else "#FFFFFF"
            html_code += f'<td style="border: 1px solid #ddd; padding: 12px; text-align: center; font-family: monospace; background-color: {bg_color}; font-size: 18px; font-weight: bold;">{item},</td>'
        html_code += '</tr>'
    html_code += '</table>'
    st.markdown(html_code, unsafe_allow_html=True)

# 3. เมนูด้านข้างสลับโหมด
st.sidebar.title("🚀 AI Lotto Menu")
mode = st.sidebar.radio("เลือกประเภทการลงทุน:", ["📈 วิเคราะห์หุ้น", "🎯 วิเคราะห์ยี่กี"])

# --- โหมดที่ 1: วิเคราะห์หุ้น ---
if mode == "📈 วิเคราะห์หุ้น":
    st.title("🤖 AI วิเคราะห์หุ้น (บน-ล่าง อัตโนมัติ)")
    target_stock = st.radio("📍 เลือกตำแหน่ง:", ["บน (ปิดดัชนี)", "ล่าง (ปิด Change)"], horizontal=True)
    market_list = {"นิเคอิ": "^N225", "ฮั่งเส็ง": "^HSI", "หุ้นไทย": "^SET.BK", "ดาวโจนส์": "^DJI"}
    choice = st.selectbox("🎯 เลือกตลาดหุ้น:", list(market_list.keys()))
    
    if st.button("🪄 สั่ง AI วิเคราะห์ราคาหุ้น"):
        ticker = yf.Ticker(market_list[choice])
        data = ticker.history(period="1d")
        if not data.empty:
            price = data['Close'].iloc[-1]
            st.metric(label=f"📊 ราคา {choice} ล่าสุด", value=f"{price:,.2f}")
            price_str = f"{price:.2f}"
            seed = int(price_str[-1]) if "บน" in target_stock else (int(price_str[-2]) + 1) % 10
            tens = [(seed + i) % 10 for i in range(8)]
            units = [0, 1, 2, 4, 5, 6, 7, 9]
            all_64 = [f"{t}{u}" for t in tens for u in units]
            highlights = all_64[:30]
            st.subheader(f"🔥 AI คัดเน้น 30 ชุด ({target_stock})")
            display_table(all_64, highlights, color="#FFE0B2")

# --- โหมดที่ 2: วิเคราะห์ยี่กี (เน้นสถิติ 50 อันดับ) ---
else:
    st.title("🎯 AI วิเคราะห์ยี่กี + สถิติ 50 คู่เลขยอดฮิต")
    st.subheader("📋 วางสถิติยี่กีเพื่อวิเคราะห์เชิงลึก")
    raw_input = st.text_area("ก๊อปปี้สถิติรอบที่ผ่านมามาวางที่นี่:", height=200, placeholder="ยี่กีทันใจ รอบที่ 48\nสามตัวบน 593\nสองตัวล่าง 19...")
    target_yeekee = st.radio("📍 เลือกตำแหน่งที่จะเล่นรอบนี้:", ["บน (2 ตัวบน)", "ล่าง (2 ตัวล่าง)"], horizontal=True)
    
    if raw_input:
        tops = re.findall(r"สามตัวบน\s*(\d+)", raw_input)
        bots = re.findall(r"สองตัวล่าง\s*(\d+)", raw_input)
        
        if tops and bots:
            # วิเคราะห์เลขคู่บ่อย ขยายเป็น 50 อันดับ
            top_pairs = [t[-2:] for t in tops]
            bot_pairs = bots
            # ใช้ 50 อันดับตามคำขอ
            top_counts = Counter(top_pairs).most_common(50)
            bot_counts = Counter(bot_pairs).most_common(50)

            last_top, last_bot = tops[-1], bots[-1]
            st.success(f"🔍 ตรวจพบข้อมูลล่าสุด: บน {last_top} / ล่าง {last_bot}")
            
            if st.button("🔮 สั่ง AI คำนวณและวิเคราะห์ 50 คู่ฮิต"):
                # สูตรคำนวณเลขปักหลัก 8 ตัว
                seed = (int(last_top[-1]) + int(last_top[-2])) % 10 if "บน" in target_yeekee else (int(last_bot[-1]) + 1) % 10
                tens = [(seed + i) % 10 for i in range(8)]
                units = [0, 1, 2, 4, 5, 6, 7, 9]
                all_64 = [f"{t}{u}" for t in tens for u in units]
                highlights = [n for n in all_64 if (int(n[0]) + int(n[1])) % 10 in [seed, (seed+2)%10, (seed+4)%10]][:30]
                
                st.subheader(f"🔥 AI คัดเน้น 30 ชุด ({target_yeekee})")
                for i in range(0, len(highlights), 10):
                    st.code("  ".join([f"{n}," for n in highlights[i:i+10]]))
                
                st.subheader(f"📋 ตาราง 64 ชุดเต็ม ({target_yeekee})")
                display_table(all_64, highlights, color="#C8E6C9")

                # --- กล่องวิเคราะห์สถิติ 50 อันดับ (ใต้ตาราง) ---
                st.divider()
                st.subheader("📈 วิเคราะห์ 50 อันดับคู่เลขที่ออกบ่อยที่สุด")
                
                col_left, col_right = st.columns(2)
                
                with col_left:
                    st.markdown("#### ⭐ **Top 50 คู่บน** (บ่อยสุดไปน้อย)")
                    # แสดงผลในกล่องเลื่อนหรือตารางสั้นๆ
                    st.dataframe(pd.DataFrame(top_counts, columns=['เลขคู่บน', 'จำนวนครั้งที่ออก']), use_container_width=True, height=400)
                
                with col_right:
                    st.markdown("#### ⭐ **Top 50 คู่ล่าง** (บ่อยสุดไปน้อย)")
                    st.dataframe(pd.DataFrame(bot_counts, columns=['เลขคู่ล่าง', 'จำนวนครั้งที่ออก']), use_container_width=True, height=400)
                
                st.info("💡 หมายเหตุ: หากเลขในตาราง 64 ชุด ติดอันดับ Top 50 ที่มีความถี่สูง จะมีโอกาสมาในรอบถัดไปมากขึ้น")
        else:
            st.info("💡 กรุณาวางสถิติในช่องด้านบนเพื่อให้ระบบเริ่มวิเคราะห์ 50 อันดับ")
