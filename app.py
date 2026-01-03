import streamlit as st
import yfinance as yf
import re
import pandas as pd
from collections import Counter

st.set_page_config(page_title="AI Lotto Analytics Pro", layout="wide")

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

st.sidebar.title("🚀 AI Lotto Menu")
mode = st.sidebar.radio("เลือกประเภทการลงทุน:", ["📈 วิเคราะห์หุ้น", "🎯 วิเคราะห์ยี่กี"])

if mode == "📈 วิเคราะห์หุ้น":
    st.title("🤖 AI วิเคราะห์หุ้น")
    # ... (ส่วนหุ้นคงเดิม)
else:
    st.title("🎯 AI วิเคราะห์ยี่กี (ระบบแม่นยำสูง)")
    raw_input = st.text_area("วางสถิติที่นี่ (เน้น 20-30 รอบล่าสุด):", height=200)
    target_yeekee = st.radio("📍 เลือกตำแหน่ง:", ["บน", "ล่าง"], horizontal=True)
    
    if raw_input:
        # ดึงข้อมูลด้วยระบบตรวจสอบคำผิดเบื้องต้น
        tops = re.findall(r"บน\s*(\d+)", raw_input.replace("สามตัวบน", "บน"))
        bots = re.findall(r"ล่าง\s*(\d+)", raw_input.replace("สองตัวล่าง", "ล่าง"))
        
        if tops and bots:
            st.info(f"📊 ตรวจพบสถิติทั้งหมด: {len(tops)} รอบ (AI จะใช้ข้อมูลนี้วิเคราะห์)")
            
            # แยกหลักสิบ-หน่วย
            if "บน" in target_yeekee:
                tens = [t[-2] for t in tops if len(t)>=2]
                units = [t[-1] for t in tops]
                pairs = [t[-2:] for t in tops if len(t)>=2]
            else:
                tens = [b[0] for b in bots if len(b)>=2]
                units = [b[1] for b in bots]
                pairs = bots

            # 8 หลักยอดฮิต
            hot_tens = [i[0] for i in Counter(tens).most_common(8)]
            hot_units = [i[0] for i in Counter(units).most_common(8)]
            
            if st.button("🔮 คำนวณเลขรอบถัดไป"):
                st.subheader(f"🔢 สรุปเลข 8 หลักมหาลาภ ({target_yeekee})")
                st.success(f"หลักสิบ: {' - '.join(hot_tens)} | หลักหน่วย: {' - '.join(hot_units)}")
                
                res_64 = [f"{t}{u}" for t in hot_tens for u in hot_units]
                # คัดเน้น 30 ชุดจากสถิติจริง
                highlights = [i[0] for i in Counter(pairs).most_common(30)]
                
                display_table(res_64, highlights, color="#C8E6C9")
                
                st.divider()
                st.subheader(f"📈 ตารางอันดับคู่เลข {target_yeekee} ที่ออกบ่อยที่สุด (Top 64)")
                df = pd.DataFrame(Counter(pairs).most_common(64), columns=['เลขชุด', 'จำนวนครั้ง'])
                st.dataframe(df, use_container_width=True)
        else:
            st.error("⚠️ AI ไม่พบตัวเลขในข้อความที่คุณวาง กรุณาตรวจสอบว่ามีเลข 'บน' หรือ 'ล่าง' หรือไม่")
