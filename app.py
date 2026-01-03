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
    
    # --- ระบบ Session State สำหรับจัดการการล้างข้อมูลทั้งหมด ---
    if 'input_text' not in st.session_state:
        st.session_state.input_text = ""
    if 'analyzed' not in st.session_state:
        st.session_state.analyzed = False

    def clear_all_data():
        # ล้างค่าสถิติใน text area
        st.session_state.input_text = ""
        # รีเซ็ตสถานะการวิเคราะห์ (ทำให้เลขที่เจนไว้หายไป)
        st.session_state.analyzed = False
        # ล้างค่าใน widget โดยตรงผ่าน key
        if 'input_text_area' in st.session_state:
            st.session_state.input_text_area = ""

    # ส่วนบน: ปุ่มล้างสถิติ
    col_empty, col_btn = st.columns([6, 1])
    with col_btn:
        st.button("🗑️ ล้างสถิติ", on_click=clear_all_data, use_container_width=True)

    # ช่องวางสถิติ
    raw_input = st.text_area("วางสถิติยี่กี (แนะนำ 20-40 รอบล่าสุด):", 
                            value=st.session_state.input_text, 
                            height=200, 
                            key="input_text_area",
                            placeholder="วางข้อความสถิติที่นี่...")
    
    # อัปเดตค่าใน session_state เมื่อมีการพิมพ์
    st.session_state.input_text = raw_input

    target = st.radio("📍 ตำแหน่งที่เล่น:", ["บน (2 ตัวบน)", "ล่าง (2 ตัวล่าง)"], horizontal=True)

    if st.session_state.input_text:
        # ดึงเลขจากข้อความ
        tops = re.findall(r"บน\s*(\d+)", st.session_state.input_text.replace("สามตัวบน", "บน"))
        bots = re.findall(r"ล่าง\s*(\d+)", st.session_state.input_text.replace("สองตัวล่าง", "ล่าง"))
        
        if tops and bots:
            pairs = [t[-2:] for t in tops if len(t)>=2] if "บน" in target else bots
            
            # --- ประมวลผลสูตร ---
            all_digits = "".join(pairs)
            hot_9_digits = [i[0] for i in Counter(all_digits).most_common(9)]
            hot_9_digits.sort()
            
            sums = [(int(p[0]) + int(p[1])) % 10 for p in pairs]
            hot_8_sums = [i[0] for i in Counter(sums).most_common(8)]
            hot_8_sums.sort()

            st.markdown("---")
            st.write("### 📝 รายละเอียดสูตรที่ใช้")
            
            c1, c2, c3 = st.columns([3, 3, 2])
            with c1:
                st.checkbox(f"แต้มสิบหน่วย (TF Total) : {''.join(map(str, hot_8_sums))}", value=True, disabled=True, key="chk_sum")
            with c2:
                st.checkbox(f"เลขมาครบสิบหน่วย (TF (2)) : {''.join(hot_9_digits)}", value=True, disabled=True, key="chk_win")
            with c3:
                if st.button("🔍 เริ่มวิเคราะห์สรุปผล", use_container_width=True, type="primary"):
                    st.session_state.analyzed = True

            # แสดงผลเมื่อมีการกดปุ่มวิเคราะห์เท่านั้น
            if st.session_state.analyzed:
                win_sets = [f"{a}{b}" for a in hot_9_digits for b in hot_9_digits]
                final_sets = [p for p in win_sets if (int(p[0]) + int(p[1])) % 10 in hot_8_sums]

                display_analysis_result(final_sets)
                
                st.divider()
                st.subheader("📈 อันดับคู่เลขที่ออกจริงจากสถิติ")
                df = pd.DataFrame(Counter(pairs).most_common(50), columns=['เลขคู่', 'ความถี่'])
                st.table(df)
        else:
            st.error("⚠️ ข้อมูลไม่เพียงพอ กรุณาวางสถิติที่มีทั้งผลบนและล่าง")
    else:
        # ถ้าไม่มีข้อมูล (เช่น หลังกดปุ่มล้าง) ให้แสดงคำแนะนำ
        st.info("กรุณาวางสถิติเพื่อเริ่มการวิเคราะห์")

# --- โหมดที่ 2: วิเคราะห์หุ้น ---
else:
    st.title("📈 AI วิเคราะห์หุ้น")
    st.info("ใช้ข้อมูลราคาปิดล่าสุดเพื่อคำนวณแนวโน้ม")
