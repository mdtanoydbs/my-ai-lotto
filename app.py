import streamlit as st
import yfinance as yf
import re
import pandas as pd
from collections import Counter

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="AI Lotto 65-Tail Pro", layout="wide")

# 2. ฟังก์ชันแสดงผลตารางสรุปผล
def display_analysis_result(final_sets):
    html_code = f'''
    <div style="background-color: #f0f7f0; padding: 20px; border-radius: 10px; border: 1px solid #c8e6c9; margin-top: 20px;">
        <p style="color: #2e7d32; font-weight: bold; font-size: 18px; margin-bottom: 15px;">สรุปผลการวิเคราะห์ จาก 2 สูตร (ถ้าไม่มีสูตรใดผิด)</p>
    '''
    
    sets_list = sorted(list(final_sets))
    # แบ่งแสดงทีละ 10 ชุด
    for i in range(0, len(sets_list), 10):
        row = " - ".join(sets_list[i:i+10])
        html_code += f'<p style="font-family: "Courier New", Courier, monospace; font-size: 17px; margin: 8px 0; letter-spacing: 1px; color: #333;">{row}</p>'
    
    html_code += f'''
        <hr style="border: 0.5px solid #c8e6c9; margin: 15px 0;">
        <p style="font-weight: bold; font-size: 16px; color: #2e7d32;">({len(sets_list)} ชุด / รวมทั้งหมด {len(sets_list)} ชุด)</p>
    </div>
    '''
    st.markdown(html_code, unsafe_allow_html=True)

# 3. เมนูหลัก
st.sidebar.title("🚀 AI Lotto Menu")
mode = st.sidebar.radio("เลือกโหมด:", ["🎯 วิเคราะห์ยี่กี (65 ชุด)", "📈 วิเคราะห์หุ้น"])

if mode == "🎯 วิเคราะห์ยี่กี (65 ชุด)":
    st.title("🎯 AI วิเคราะห์ยี่กี สรุปผล 2 สูตรหลัก")
    
    # ระบบปุ่มล้างข้อมูล (ใช้ Session State)
    if 'input_text' not in st.session_state:
        st.session_state.input_text = ""

    def clear_text():
        st.session_state.input_text = ""

    col_btn1, col_btn2 = st.columns([6, 1])
    with col_btn2:
        st.button("🗑️ ล้างสถิติ", on_click=clear_text)

    raw_input = st.text_area("วางสถิติยี่กี (แนะนำ 20-40 รอบล่าสุด):", 
                            value=st.session_state.input_text, 
                            height=200, 
                            key="input_text_area",
                            on_change=lambda: st.session_state.update(input_text=st.session_state.input_text_area))
    
    target = st.radio("📍 ตำแหน่งที่เล่น:", ["บน (2 ตัวบน)", "ล่าง (2 ตัวล่าง)"], horizontal=True)

    if raw_input:
        # ดึงเลขจากข้อความให้แม่นยำขึ้น
        tops = re.findall(r"บน\s*(\d+)", raw_input.replace("สามตัวบน", "บน"))
        bots = re.findall(r"ล่าง\s*(\d+)", raw_input.replace("สองตัวล่าง", "ล่าง"))
        
        if tops and bots:
            pairs = [t[-2:] for t in tops if len(t)>=2] if "บน" in target else bots
            
            # สูตรที่ 1: เลขมาครบ 9 ตัว (TF (2))
            all_digits = "".join(pairs)
            hot_9_digits = [i[0] for i in Counter(all_digits).most_common(9)]
            hot_9_digits.sort()
            
            # สูตรที่ 2: แต้มสิบหน่วย (TF Total)
            sums = [(int(p[0]) + int(p[1])) % 10 for p in pairs]
            hot_8_sums = [i[0] for i in Counter(sums).most_common(8)]
            hot_8_sums.sort()

            # แสดงรายละเอียดสูตรพร้อม Checkbox (ตามภาพ)
            st.write("### 📝 รายละเอียดสูตรที่ใช้")
            c1, c2 = st.columns(2)
            with c1:
                st.checkbox(f"แต้มสิบหน่วย (TF Total) : {''.join(map(str, hot_8_sums))}", value=True, disabled=True)
            with c2:
                st.checkbox(f"เลขมาครบสิบหน่วย (TF (2)) : {''.join(hot_9_digits)}", value=True, disabled=True)

            if st.button("🔍 เริ่มวิเคราะห์สรุปผล"):
                # จับคู่วินเลขมาครบ 9x9 = 81 ชุด
                win_sets = [f"{a}{b}" for a in hot_9_digits for b in hot_9_digits]
                # ตัดด้วยแต้ม 8 ตัว
                final_sets = [p for p in win_sets if (int(p[0]) + int(p[1])) % 10 in hot_8_sums]

                # แสดงผลชุดเลข
                display_analysis_result(final_sets)
                
                # ตารางสถิติ Top 50
                st.divider()
                st.subheader("📈 อันดับคู่เลขที่ออกจริงจากสถิติ")
                df = pd.DataFrame(Counter(pairs).most_common(50), columns=['เลขคู่', 'ความถี่'])
                st.table(df) # ใช้ st.table เพื่อให้ดูนิ่งและเป็นระเบียบแบบโปรแกรม
        else:
            st.error("⚠️ ไม่พบข้อมูลสถิติ กรุณาวางสถิติที่มีคำว่า 'บน' และ 'ล่าง'")
else:
    st.title("📈 วิเคราะห์หุ้น")
    st.info("ระบบดึงราคา Real-time จากตลาดโลก")
