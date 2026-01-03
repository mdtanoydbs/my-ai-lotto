import streamlit as st
import yfinance as yf

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="AI Lotto Master Pro", layout="wide")

# เมนูด้านข้าง
st.sidebar.title("🛠 เมนูเลือกโหมด AI")
mode = st.sidebar.radio("ประเภทการลงทุน:", ["📈 วิเคราะห์หุ้น", "🎯 วิเคราะห์ยี่กี"])

# --- ฟังก์ชันแสดงผลตาราง ---
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

# --- โหมดหุ้น (เพิ่มเลือก บน-ล่าง) ---
if mode == "📈 วิเคราะห์หุ้น":
    st.title("🤖 AI วิเคราะห์หุ้น (บน-ล่าง อัตโนมัติ)")
    
    target_stock = st.radio("📍 เลือกตำแหน่งที่ต้องการเล่น:", ["บน (ปิดดัชนี)", "ล่าง (ปิด Change)"], horizontal=True)
    
    market_list = {
        "นิเคอิ (ญี่ปุ่น)": "^N225", 
        "ฮั่งเส็ง (ฮ่องกง)": "^HSI", 
        "หุ้นไทย (SET)": "^SET.BK", 
        "ดาวโจนส์ (USA)": "^DJI",
        "หุ้นจีน (SSE)": "000001.SS"
    }
    choice = st.selectbox("🎯 เลือกตลาดหุ้น:", list(market_list.keys()))
    
    if st.button("🪄 วิเคราะห์ราคาหุ้น"):
        ticker = yf.Ticker(market_list[choice])
        data = ticker.history(period="1d")
        
        if not data.empty:
            price = data['Close'].iloc[-1]
            st.metric(label=f"📊 ราคา {choice} ล่าสุด", value=f"{price:,.2f}")
            
            # สูตร AI หุ้น แยกบน-ล่าง
            price_str = f"{price:.2f}"
            if "บน" in target_stock:
                # บน: ใช้ทศนิยมตัวท้ายของราคาปิด
                seed = int(price_str[-1])
            else:
                # ล่าง: ใช้ทศนิยมตัวแรกของราคาปิด + เลขหลักหน่วย
                seed = (int(price_str[-2]) + int(price_str[-4])) % 10
            
            tens = [(seed + i) % 10 for i in range(8)]
            units = [0, 1, 2, 4, 5, 6, 7, 9]
            all_64 = [f"{t}{u}" for t in tens for u in units]
            
            # คัดเน้น 30 ชุด (สูตร AI คัดจากเลขฐาน)
            highlights = [n for n in all_64 if (int(n[0]) + int(n[1])) % 2 == (seed % 2)][:30]
            
            st.subheader(f"🔥 AI คัดเน้น 30 ชุด (สำหรับหุ้น {target_stock})")
            for i in range(0, len(highlights), 10):
                st.code("  ".join([f"{n}," for n in highlights[i:i+10]]))
            
            st.subheader(f"📋 ตาราง 64 ชุดเต็ม ({target_stock})")
            display_table(all_64, highlights, color="#FFE0B2") # สีส้มสำหรับหุ้น
        else:
            st.error("ไม่สามารถดึงข้อมูลได้ โปรดลองอีกครั้ง")

# --- โหมดหน้ายี่กี ---
else:
    st.title("🎯 AI วิเคราะห์ยี่กี (เจาะลึก บน-ล่าง)")
    target_yeekee = st.radio("📍 เลือกตำแหน่งที่ต้องการเล่น:", ["บน (2 ตัวบน)", "ล่าง (2 ตัวล่าง)"], horizontal=True)
    
    col1, col2 = st.columns(2)
    with col1:
        last_top = st.text_input("3 ตัวบนล่าสุด:", "836")
    with col2:
        last_bot = st.text_input("2 ตัวล่างล่าสุด:", "96")
        
    if st.button("🔮 วิเคราะห์ยี่กีรอบถัดไป"):
        if "บน" in target_yeekee:
            seed = (int(last_top[-1]) + int(last_top[-2])) % 10
        else:
            seed = (int(last_bot[-1]) + 1) % 10
            
        tens = [(seed + i) % 10 for i in range(8)]
        units = [0, 1, 2, 4, 5, 6, 7, 9]
        all_64 = [f"{t}{u}" for t in tens for u in units]
        highlights = [n for n in all_64 if (int(n[0]) + int(n[1])) % 10 in [seed, (seed+2)%10, (seed+4)%10]][:30]
        
        st.subheader(f"🔥 AI คัดเน้น 30 ชุด ({target_yeekee})")
        for i in range(0, len(highlights), 10):
            st.code("  ".join([f"{n}," for n in highlights[i:i+10]]))
            
        st.subheader(f"📋 ตาราง 64 ชุดเต็ม ({target_yeekee})")
        display_table(all_64, highlights, color="#C8E6C9") # สีเขียวสำหรับยี่กี
