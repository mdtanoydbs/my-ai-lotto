import streamlit as st
import yfinance as yf
import re
import pandas as pd
from collections import Counter

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="AI Lotto 65-Tail Analysis", layout="wide")

# 2. ฟังก์ชันแสดงผลตารางสรุปผล
def display_analysis_result(final_sets):
    html_code = f'<div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; border: 1px solid #ddd;">'
    html_code += f'<p style="color: #2e7d32; font-weight: bold; font-size: 18px;">สรุปผลการวิเคราะห์ จาก 2 สูตร (ถ้าไม่มีสูตรใดผิด)</p>'
    
    # แบ่งแสดงทีละ 10 ชุดเพื่อความสวยงาม
    sets_list = sorted(list(final_sets))
    for i in range(0, len(sets_list), 10):
        row = " - ".join(sets_list[i:i+10])
        html_code += f'<p style="font-family: monospace; font-size: 16px; margin: 5px 0;">{row}</p>'
    
    html_code += f'<hr><p style="font-weight: bold;">({len(sets_list)} ชุด / รวมทั้งหมด {len(sets_list)} ชุด)</p>'
    html_code += '</div>'
    st.markdown(html_code, unsafe_allow_html=True)

# 3. เมนูหลัก
st.sidebar.title("🚀 AI Lotto Menu")
mode = st.sidebar.radio("เลือกโหมด:", ["🎯 วิเคราะห์ยี่กี (65 ชุด)", "📈 วิเคราะห์หุ้น"])

if mode == "🎯 วิเคราะห์ยี่กี (65 ชุด)":
    st.title("🎯 AI วิเคราะห์ยี่กี สรุปผล 2 สูตรหลัก")
    
    raw_input = st.text_area("วางสถิติยี่กี (แนะนำ 20-40 รอบล่าสุด):", height=200)
    target = st.radio("📍 ตำแหน่งที่เล่น:", ["บน (2 ตัวบน)", "ล่าง (2 ตัวล่าง)"], horizontal=True)

    if raw_input:
        # ดึงเลขจากข้อความ
        tops = re.findall(r"บน\s*(\d+)", raw_input.replace("สามตัวบน", "บน"))
        bots = re.findall(r"ล่าง\s*(\d+)", raw_input.replace("สองตัวล่าง", "ล่าง"))
        
        if tops and bots:
            pairs = [t[-2:] for t in tops if len(t)>=2] if "บน" in target else bots
            
            # --- เริ่มกระบวนการวิเคราะห์ 2 สูตร ---
            
            # สูตรที่ 1: เลขมาครบ 9 ตัว (TF 2 ตัว) - ดึงเลขที่ออกบ่อยที่สุด 9 ตัว
            all_digits = "".join(pairs)
            hot_9_digits = [i[0] for i in Counter(all_digits).most_common(9)]
            hot_9_digits.sort()
            
            # สูตรที่ 2: แต้มรวม 8 แต้ม (TF Total) - ดึงแต้มที่ออกบ่อยที่สุด 8 แต้ม
            sums = [(int(p[0]) + int(p[1])) % 10 for p in pairs]
            hot_8_sums = [i[0] for i in Counter(sums).most_common(8)]
            hot_8_sums.sort()

            if st.button("🔍 เริ่มวิเคราะห์สรุปผล"):
                st.subheader("📝 รายละเอียดสูตรที่ใช้")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"✅ **แต้มสิบหน่วย (TF Total) :** { ''.join(map(str, hot_8_sums)) }")
                with col2:
                    st.write(f"✅ **เลขมาครบสิบหน่วย (TF (2)) :** { ''.join(hot_9_digits) }")

                # --- คำนวณสรุปผล ---
                # 1. วินเลขมาครบ 9 ตัว (จะได้ 81 ชุดรวมเบิ้ล)
                win_sets = [f"{a}{b}" for a in hot_9_digits for b in hot_9_digits]
                
                # 2. ตัดด้วยแต้มรวม 8 แต้ม
                final_sets = [p for p in win_sets if (int(p[0]) + int(p[1])) % 10 in hot_8_sums]

                # แสดงผลลัพธ์
                st.write("")
                display_analysis_result(final_sets)
                
                # ตารางสถิติประกอบการตัดสินใจ
                st.divider()
                st.subheader("📈 อันดับคู่เลขที่ออกจริง (จากสถิติที่วาง)")
                df = pd.DataFrame(Counter(pairs).most_common(50), columns=['เลขคู่', 'ความถี่'])
                st.dataframe(df, use_container_width=True)
        else:
            st.warning("⚠️ กรุณาวางสถิติให้ถูกต้อง")
else:
    st.title("📈 วิเคราะห์หุ้น")
    st.info("ระบบคำนวณจากราคาปิด Real-time")
