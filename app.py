import streamlit as st
import yfinance as yf
import re
import pandas as pd
from collections import Counter

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="AI Lotto Analytics Pro", layout="wide")

# 2. ฟังก์ชันแสดงผลตารางเลขชุดแบบตารางหมากรุก
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

# 3. เมนูเลือกโหมด
st.sidebar.title("🚀 AI Lotto Menu")
mode = st.sidebar.radio("เลือกประเภทการลงทุน:", ["📈 วิเคราะห์หุ้น", "🎯 วิเคราะห์ยี่กี"])

# --- โหมดวิเคราะห์หุ้น ---
if mode == "📈 วิเคราะห์หุ้น":
    st.title("🤖 AI วิเคราะห์หุ้น (บน-ล่าง อัตโนมัติ)")
    target_stock = st.radio("📍 เลือกตำแหน่ง:", ["บน (ปิดดัชนี)", "ล่าง (ปิด Change)"], horizontal=True)
    market_list = {"นิเคอิ": "^N225", "ฮั่งเส็ง": "^HSI", "หุ้นไทย": "^SET.BK", "ดาวโจนส์": "^DJI"}
    choice = st.selectbox("🎯 เลือกตลาดหุ้น:", list(market_list.keys()))
    
    if st.button("🪄 สั่ง AI วิเคราะห์ราคาหุ้น"):
        try:
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
        except:
            st.error("ไม่สามารถดึงข้อมูลหุ้นได้")

# --- โหมดวิเคราะห์ยี่กี (เน้นระบบวิเคราะห์ 64 ชุดจากสถิติ) ---
else:
    st.title("🎯 AI วิเคราะห์ยี่กี + วิเคราะห์เลข 8 หลัก (สิบ-หน่วย)")
    st.subheader("📋 วางสถิติยี่กีเพื่อวิเคราะห์เชิงลึก")
    raw_input = st.text_area("ก๊อปปี้สถิติมาวางที่นี่:", height=200, placeholder="ยี่กีทันใจ รอบที่ 48\nสามตัวบน 593\nสองตัวล่าง 19...")
    target_yeekee = st.radio("📍 เลือกตำแหน่งที่จะเล่นรอบนี้:", ["บน (2 ตัวบน)", "ล่าง (2 ตัวล่าง)"], horizontal=True)
    
    if raw_input:
        tops = re.findall(r"สามตัวบน\s*(\d+)", raw_input)
        bots = re.findall(r"สองตัวล่าง\s*(\d+)", raw_input)
        
        if tops and bots:
            # วิเคราะห์หลักสิบและหลักหน่วยเพื่อหา 8 หลักที่ออกบ่อย
            if "บน" in target_yeekee:
                tens_list = [t[-2] for t in tops]
                units_list = [t[-1] for t in tops]
                current_pairs = [t[-2:] for t in tops]
            else:
                tens_list = [b[0] for b in bots]
                units_list = [b[1] for b in bots]
                current_pairs = bots

            # หาเลข 8 หลักที่ออกบ่อยที่สุดในหลักสิบและหน่วย
            hot_tens = [item[0] for item in Counter(tens_list).most_common(8)]
            hot_units = [item[0] for item in Counter(units_list).most_common(8)]
            
            # เลขที่ยังไม่มา
            all_digits = set("0123456789")
            miss_tens = sorted(list(all_digits - set(hot_tens)))
            miss_units = sorted(list(all_digits - set(hot_units)))

            last_top, last_bot = tops[-1], bots[-1]
            st.success(f"🔍 ข้อมูลล่าสุด: บน {last_top} / ล่าง {last_bot}")
            
            if st.button("🔮 สั่ง AI วิเคราะห์ Top 64 ชุด"):
                # สรุปสถิติ 8 หลัก
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"🔢 หลักสิบ 8 ตัวฮิต: {', '.join(hot_tens)}\n\n(ยังไม่มา: {', '.join(miss_tens)})")
                with col2:
                    st.info(f"🔢 หลักหน่วย 8 ตัวฮิต: {', '.join(hot_units)}\n\n(ยังไม่มา: {', '.join(miss_units)})")

                # สร้างชุดเลข 64 ชุดจากการจับคู่เลข 8 หลักที่ออกบ่อยที่สุด
                res_64 = [f"{t}{u}" for t in hot_tens for u in hot_units]
                
                # คัดเน้น 30 ชุด (จากเลขที่ออกบ่อยที่สุดในสถิติจริง)
                hot_hits_all = Counter(current_pairs).most_common(30)
                highlights = [item[0] for item in hot_hits_all]

                st.subheader(f"🔥 AI คัดเน้น 30 ชุด (จากสถิติที่วาง)")
                st.code("  ".join([f"{n}," for n in highlights]))

                st.subheader(f"📋 กล่อง Top 64 ชุด (จับคู่จากเลข 8 หลัก สิบ-หน่วย)")
                display_table(res_64, highlights, color="#C8E6C9")

                # --- ตารางสถิติ Top 64 อันดับตามคำขอ ---
                st.divider()
                st.subheader(f"📈 อันดับคู่เลข {target_yeekee} ที่ออกบ่อยที่สุด (Top 64)")
                
                pair_counts = Counter(current_pairs).most_common(64)
                df_pairs = pd.DataFrame(pair_counts, columns=['เลขคู่', 'จำนวนครั้งที่ออก'])
                st.dataframe(df_pairs, use_container_width=True, height=500)
        else:
            st.info("💡 กรุณาวางสถิติในรูปแบบที่ถูกต้อง (มีคำว่า สามตัวบน / สองตัวล่าง)")
