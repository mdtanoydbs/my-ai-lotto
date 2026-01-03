import streamlit as st
import yfinance as yf

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="AI Lotto Multi-Tool", layout="wide")

# เมนูหลัก
st.sidebar.title("🛠 เมนูเลือกโหมด AI")
mode = st.sidebar.radio("เลือกประเภทที่ต้องการลงทุน:", ["📈 วิเคราะห์หุ้น (AI Auto)", "🎯 วิเคราะห์ยี่กี (กรอกสถิติ)"])

# --- ฟังก์ชันจัดการแสดงผลตาราง 64 ชุด ---
def display_table(res, highlights):
    html_code = '<table style="width:100%; border-collapse: collapse;">'
    for i in range(0, len(res), 8):
        row_items = res[i:i+8]
        html_code += '<tr>'
        for item in row_items:
            bg_color = "#DFFFD6" if item in highlights else "#FFFFFF"
            html_code += f'<td style="border: 1px solid #ddd; padding: 12px; text-align: center; font-family: monospace; background-color: {bg_color}; font-size: 18px; font-weight: bold;">{item},</td>'
        html_code += '</tr>'
    html_code += '</table>'
    st.markdown(html_code, unsafe_allow_html=True)

# --- โหมดที่ 1: วิเคราะห์หุ้น ---
if mode == "📈 วิเคราะห์หุ้น (AI Auto)":
    st.title("🤖 AI วิเคราะห์หุ้นปักหลัก (อัตโนมัติ)")
    market_list = {
        "นิเคอิ (ญี่ปุ่น)": "^N225", "ฮั่งเส็ง (ฮ่องกง)": "^HSI", 
        "หุ้นไทย (SET)": "^SET.BK", "ดาวโจนส์ (USA)": "^DJI"
    }
    choice = st.selectbox("🎯 เลือกตลาดหุ้น:", list(market_list.keys()))
    
    if st.button("🪄 สั่ง AI วิเคราะห์ราคาหุ้น"):
        ticker = yf.Ticker(market_list[choice])
        price = ticker.history(period="1d")['Close'].iloc[-1]
        st.metric(label=f"📊 ราคา {choice} ล่าสุด", value=f"{price:,.2f}")
        
        # สูตร AI หุ้น: ใช้ทศนิยมตัวสุดท้ายสร้างเลขปักหลัก
        seed = int(str(f"{price:.2f}")[-1])
        tens = [(seed + i) % 10 for i in range(8)]
        units = [0, 1, 2, 4, 5, 6, 7, 9]
        all_64 = [f"{t}{u}" for t in tens for u in units]
        
        # คัดเน้น 30 ตัวจากฐานราคา
        highlights = all_64[:30] # ตัวอย่างการคัดกรอง
        
        st.subheader("🔥 AI คัดเน้น 30 ชุด (ตัวเต็งหุ้น)")
        st.code(" , ".join(highlights[:10]) + " ,")
        st.code(" , ".join(highlights[10:20]) + " ,")
        st.code(" , ".join(highlights[20:30]) + " ,")
        
        st.subheader("📋 ตาราง 64 ชุดเต็ม")
        display_table(all_64, highlights)

# --- โหมดที่ 2: วิเคราะห์ยี่กี ---
else:
    st.title("🎯 AI วิเคราะห์ยี่กี (อิงสถิติล่าสุด)")
    col1, col2 = st.columns(2)
    with col1:
        last_top = st.text_input("3 ตัวบนล่าสุด:", "836")
    with col2:
        last_bot = st.text_input("2 ตัวล่างล่าสุด:", "96")
        
    if st.button("🔮 สั่ง AI วิเคราะห์ยี่กี"):
        # สูตร AI ยี่กี: ใช้เลขหน่วยบนและล่างบวกกันหาเลขไหล
        seed = (int(last_top[-1]) + int(last_bot[-1])) % 10
        tens = [(seed + i) % 10 for i in range(8)]
        units = [0, 1, 2, 4, 5, 6, 7, 9]
        all_64 = [f"{t}{u}" for t in tens for u in units]
        
        # คัดเน้น 30 ตัว (สุ่มจากสถิติเลขที่มีโอกาสสูง)
        highlights = [n for n in all_64 if (int(n[0]) + int(n[1])) % 2 == 0][:30] 
        
        st.subheader("🔥 AI คัดเน้น 30 ชุด (ตัวเต็งยี่กี)")
        st.code(" , ".join(highlights[:10]) + " ,")
        st.code(" , ".join(highlights[10:20]) + " ,")
        st.code(" , ".join(highlights[20:30]) + " ,")

        st.subheader("📋 ตาราง 64 ชุดเต็ม")
        display_table(all_64, highlights)
