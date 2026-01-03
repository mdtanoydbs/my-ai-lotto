import streamlit as st
import yfinance as yf

st.set_page_config(page_title="AI Lotto Analytics", layout="wide")

st.title("🤖 AI วิเคราะห์หุ้นปักหลัก 8 ตัว")
st.write("ดึงราคา Real-time เพื่อคำนวณเลข 64 ชุด")

market_list = {
    "นิเคอิ (ญี่ปุ่น)": "^N225", 
    "ฮั่งเส็ง (ฮ่องกง)": "^HSI", 
    "หุ้นไทย (SET)": "^SET.BK", 
    "ดาวโจนส์ (USA)": "^DJI",
    "หุ้นจีน (SSE)": "000001.SS",
    "สิงคโปร์ (STI)": "^STI",
    "อังกฤษ (FTSE)": "^FTSE",
    "เยอรมัน (DAX)": "^GDAXI"
}
choice = st.selectbox("🎯 เลือกตลาดหุ้น:", list(market_list.keys()))

st.subheader("⚙️ ตั้งค่าเลขปักหลัก")
col1, col2 = st.columns(2)
with col1:
    s_tens = st.text_input("หลักสิบ (8 ตัว):", "0,1,2,3,4,5,7,9")
with col2:
    s_units = st.text_input("หลักหน่วย (8 ตัว):", "0,1,2,4,5,6,7,9")

if st.button("🚀 เริ่มคำนวณเลขเด่น"):
    try:
        ticker = yf.Ticker(market_list[choice])
        price_data = ticker.history(period="1d")
        if not price_data.empty:
            price = price_data['Close'].iloc[-1]
            st.metric(label=f"📊 ราคา {choice} ล่าสุด", value=f"{price:,.2f}")

        tens = [t.strip() for t in s_tens.split(",")]
        units = [u.strip() for u in s_units.split(",")]
        res = [f"{t}{u}" for t in tens for u in units]
        
        st.success(f"✅ วิเคราะห์เสร็จสิ้น! ได้เลขทั้งหมด {len(res)} ชุด")
        st.write("📋 **ชุดเลข 64 หาง (เรียงแถวละ 8 ชุด):**")

        # บังคับแสดงผลเป็นแถวละ 8 ตัวด้วย HTML Table
        html_code = '<table style="width:100%; border-collapse: collapse;">'
        for i in range(0, len(res), 8):
            row_items = res[i:i+8]
            html_code += '<tr>'
            for item in row_items:
                html_code += f'<td style="border: 1px solid #ddd; padding: 8px; text-align: center; font-family: monospace; font-size: 18px;">{item},</td>'
            html_code += '</tr>'
        html_code += '</table>'
        
        st.markdown(html_code, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาด: {e}")
