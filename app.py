import streamlit as st
import yfinance as yf
import re
import pandas as pd
from collections import Counter

# 1. ตั้งค่าหน้าเว็บแบบกว้าง
st.set_page_config(page_title="AI Lotto 65-Tail Pro", layout="wide")

# 2. ฟังก์ชันแสดงผลตารางสรุปผล (สไตล์โปรแกรมวิเคราะห์)
def display_analysis_result(final_sets):
    html_code = f'''
    <div style="background-color: #f0f7f0; padding: 20px; border-radius: 10px; border: 1px solid #c8e6c9; margin-top: 20px;">
        <p style="color: #2e7d32; font-weight: bold; font-size: 18px; margin-bottom: 15px;">สรุปผลการวิเคราะห์ จาก 2 สูตร (ถ้าไม่มีสูตรใดผิด)</p>
    '''
    
    sets_list = sorted(list(final_sets))
    # แบ่งแสดงทีละ 10 ชุดต่อบรรทัด
    for i in range(0, len(sets_list), 10):
        row = " - ".join(sets_list[i:i+10])
        html_code += f'<p style="font-family: monospace; font-size: 17px; margin: 8px 0; letter-spacing: 1px; color: #333;">{row}</p>'
    
    html_code += f'''
        <hr style="border: 0.5px solid #c8e6c9; margin: 15px 0;">
        <p style="font-weight: bold; font-size: 16px; color: #2e7d32;">({len(sets_list)} ชุด / รวมทั้งหมด {len(sets_list)} ชุด)</p>
    </div>
    '''
    st.markdown(html_code, unsafe_allow_html=True)

# 3. เมนูหลักด้านข้าง
st.sidebar.title("🚀 AI Lotto Menu")
mode = st.sidebar.radio("เลือกโหมด:", ["🎯 วิเคราะห์ยี่กี (65 ชุด)", "📈 วิเคราะห์หุ้น"])

# --- โหมดที่ 1: วิเคราะห์ยี่กี ---
if mode == "🎯 วิเคราะห์ยี่กี (65 ชุด)":
    st.title("🎯 AI วิเคราะห์ยี่กี สรุปผล 2 สูตรหลัก")
    
    # ระบบ Session State สำหรับปุ่มล้างข้อมูล
    if 'input_text' not in st.session_state:
        st.session_state.input_text = ""

    def clear_text():
        st.session_state.input_text = ""

    # ส่วนบน: ปุ่มล้างและพื้นที่กรอกข้อมูล
    col_btn1, col_btn2 = st.columns([6, 1])
    with col_btn2:
        st.button("🗑️ ล้างสถิติ", on_click=clear_text, use_container_width=True)

    raw_input = st.text_area("วางสถิติยี่กี (แนะนำ 20-40 รอบล่าสุด):", 
                            value=st.session_state.input_text, 
                            height=200, 
                            key="input_text_area",
                            on_change=lambda: st.session_state.update(input_text=st.session_state.input_text_area))
    
    target = st.radio("📍 ตำแหน่งที่เล่น:", ["บน (2 ตัวบน)", "ล่าง (2 ตัวล่าง)"], horizontal=True)

    if raw_input:
        # ดึงเลขจากข้อความ (รองรับคำว่า สามตัวบน / สองตัวล่าง / บน / ล่าง)
        tops = re.findall(r"บน\s*(\d+)", raw_input.replace("สามตัวบน", "บน"))
        bots = re.findall(r"ล่าง\s*(\d+)", raw_input.replace("สองตัวล่าง", "ล่าง"))
        
        if tops and bots:
            pairs = [t[-2:] for t in tops if len(t)>=2] if "บน" in target else bots
            
            # --- ประมวลผลสูตร ---
            # 1. เลขมาครบ 9 ตัว (TF (2))
            all_digits = "".join(pairs)
            hot_9_digits = [i[0] for i in Counter(all_digits).most_common(9)]
            hot_9_digits.sort()
            
            # 2. แต้มสิบหน่วย (TF Total) 8 แต้ม
            sums = [(int(p[0]) + int(p[1])) % 10 for p in pairs]
            hot_8_sums = [i[0] for i in Counter(sums).most_common(8)]
            hot_8_sums.sort()

            # --- ส่วนการแสดงผลรายละเอียดสูตรและปุ่มกด (จัดให้อยู่ใกล้กัน) ---
            st.markdown("---")
            st.write("### 📝 รายละเอียดสูตรที่ใช้")
            
            # จัดวาง Checkbox และ ปุ่มกดในแถวเดียวกัน
            c1, c2, c3 = st.columns([3, 3, 2])
            with c1:
                st.checkbox(f"แต้มสิบหน่วย (TF Total) : {''.join(map(str, hot_8_sums))}", value=True, disabled=True)
            with c2:
                st.checkbox(f"เลขมาครบสิบหน่วย (TF (2)) : {''.join(hot_9_digits)}", value=True, disabled=True)
            with c3:
                # ปุ่มเริ่มวิเคราะห์อยู่ท้ายแถว
                analyze_btn = st.button("🔍 เริ่มวิเคราะห์สรุปผล", use_container_width=True, type="primary")

            if analyze_btn:
                # ตรรกะ: วินเลขมาครบ 9x9 แล้วตัดด้วยแต้ม
                win_sets = [f"{a}{b}" for a in hot_9_digits for b in hot_9_digits]
                final_sets = [p for p in win_sets if (int(p[0]) + int(p[1])) % 10 in hot_8_sums]

                # แสดงผลชุดเลข 65 ชุดโดยประมาณ
                display_analysis_result(final_sets)
                
                # ตารางสถิติย้อนหลัง
                st.divider()
                st.subheader("📈 อันดับคู่เลขที่ออกจริงจากสถิติ")
                df = pd.DataFrame(Counter(pairs).most_common(50), columns=['เลขคู่', 'ความถี่'])
                st.table(df)
        else:
            st.error("⚠️ ข้อมูลไม่เพียงพอ กรุณาวางสถิติที่มีทั้งผลบนและล่าง")

# --- โหมดที่ 2: วิเคราะห์หุ้น ---
else:
    st.title("📈 AI วิเคราะห์หุ้น")
    st.info("ใช้ข้อมูลราคาปิดล่าสุดเพื่อคำนวณแนวโน้ม")
    # ส่วนนี้ใช้โค้ดเดิมที่คุณมีอยู่แล้วได้เลย
