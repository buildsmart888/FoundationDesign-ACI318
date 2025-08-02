# Foundation Design - ACI 318M-25 Streamlit Web Application

🏗️ **เว็บแอปพลิเคชันสำหรับการออกแบบฐานรากตามมาตรฐาน ACI 318M-25**

## คุณสมบัติหลัก

### 🎯 การออกแบบฐานราก
- **ออกแบบฐานรากแผ่น (Pad Foundation)** ตาม ACI 318M-25 Chapter 13.1
- **คำนวณโหลดรวม** ด้วย Load Factors มาตรฐาน (1.2D + 1.6L)
- **ตรวจสอบแรงดัด** ตาม Section 7 ด้วย Whitney Stress Block
- **ตรวจสอบแรงเฉือน** ตาม Section 22.5 และ 22.6
- **คำนวณกำลังรับแรงอัด** ของดินอัตโนมัติ

### 📊 ส่วนต่อประสานผู้ใช้
- **อินเทอร์เฟซแบบโต้ตอบ** ง่ายต่อการใช้งาน
- **ผลลัพธ์แบบ Real-time** อัพเดททันทีเมื่อเปลี่ยนค่าพารามิเตอร์
- **แสดงภาพ 3มิติ** ของฐานรากและโครงสร้าง
- **รายงานโดยละเอียด** ตามมาตรฐาน ACI 318M-25
- **ตรวจสอบความปลอดภัย** แบบครบถ้วน

### 📈 การแสดงผลและวิเคราะห์
- **แผนภูมิแสดงอัตราส่วน Demand/Capacity**
- **แผนผังฐานราก** พร้อมตำแหน่งเสาและ Critical Section
- **ตารางสรุปผลการออกแบบ** ครบถ้วนตามมาตรฐาน
- **ส่งออกผลลัพธ์** เป็น PDF หรือ Excel (กำลังพัฒนา)

## วิธีการใช้งาน

### 1. การเริ่มต้นใช้งาน

#### วิธีที่ 1: รันด้วย Batch File (แนะนำ)
```bash
# Double-click ไฟล์ run_streamlit.bat
# หรือเปิด Command Prompt และรันคำสั่ง:
run_streamlit.bat
```

#### วิธีที่ 2: รันด้วย Command Line
```bash
# เปิด Terminal/PowerShell ใน Folder โปรเจกต์
cd "c:\Users\thani\OneDrive - Thaniyagroup\GitHub\FoundationDesign-ACI318"

# รัน Streamlit App
& ".venv\Scripts\streamlit.exe" run streamlit_app.py --server.port 8501
```

#### วิธีที่ 3: รันผ่าน Python Environment
```bash
# Activate virtual environment
.venv\Scripts\activate

# Install dependencies (ถ้ายังไม่ได้ติดตั้ง)
pip install -r requirements_streamlit.txt

# รัน Streamlit
streamlit run streamlit_app.py
```

### 2. การใส่ข้อมูลอินพุต

#### 🏛️ ข้อมูลเสา (Column Properties)
- **ความยาวเสา (mm)**: 200-2000 mm
- **ความกว้างเสา (mm)**: 200-2000 mm

#### ⚖️ โหลด (Loads)
- **Dead Load (kN)**: น้ำหนักคงที่
- **Live Load (kN)**: น้ำหนักจร
- **Wind Load (kN)**: แรงลม (optional)

#### 🏗️ พารามิเตอร์ฐานราก
- **ความหนาฐานราก (mm)**: 200-1500 mm
- **กำลังรับแรงอัดของดิน (kN/m²)**: 50-1000 kN/m²

#### 🧱 คุณสมบัติวัสดุ
- **f'c (MPa)**: กำลังอัดคอนกรีต 17-83 MPa
- **fy (MPa)**: จุดครากของเหล็ก 280-550 MPa

### 3. การวิเคราะห์และผลลัพธ์

#### 📊 แท็บผลลัพธ์
1. **📐 Geometry**: ข้อมูลขนาดฐานรากและวัสดุ
2. **💪 Flexural Design**: การออกแบบแรงดัดตาม Section 7
3. **✂️ Shear Design**: การออกแบบแรงเฉือนตาม Section 22
4. **📋 Summary**: สรุปผลการออกแบบและความปลอดภัย
5. **📊 Visualization**: แสดงภาพฐานรากและกราฟวิเคราะห์

## ข้อมูลทางเทคนิค

### มาตรฐานการออกแบบ
- **ACI 318M-25**: Building Code Requirements for Structural Concrete (Metric)
- **Chapter 13.1**: Foundations
- **Section 5.3**: Load combinations and strength reduction factors
- **Section 7**: Flexural design using Whitney stress block
- **Section 22**: Shear and torsion design

### Load Factors ตาม ACI 318M-25
- **Dead Load Factor**: 1.2
- **Live Load Factor**: 1.6
- **Wind Load Factor**: 1.0

### Strength Reduction Factors (φ)
- **φ Flexure**: 0.9 (Section 5.4.2.1)
- **φ Shear**: 0.75 (Section 5.4.2.3)

### การตรวจสอบความปลอดภัย
1. **Bearing Pressure Check**: ตรวจสอบแรงกดดิน ≤ Allowable
2. **Flexural Strength**: ตรวจสอบกำลังรับแรงดัด
3. **One-way Shear**: ตรวจสอบแรงเฉือนทางเดียว
4. **Punching Shear**: ตรวจสอบแรงเฉือนทะลุ (Two-way shear)

## ตัวอย่างการใช้งาน

### ตัวอย่างที่ 1: อาคารสำนักงานทั่วไป
```
📋 Input Parameters:
- Dead Load: 800 kN
- Live Load: 300 kN  
- Column: 400×400 mm
- f'c: 30 MPa, fy: 420 MPa
- Soil Capacity: 200 kN/m²

✅ Expected Results:
- Foundation: ~2500×2500×400 mm
- Reinforcement: 16mm @ 150mm c/c
- All checks: PASS
```

### ตัวอย่างที่ 2: โรงงานอุตสาหกรรม
```
📋 Input Parameters:
- Dead Load: 1200 kN
- Live Load: 600 kN
- Column: 500×500 mm  
- f'c: 35 MPa, fy: 420 MPa
- Soil Capacity: 150 kN/m²

✅ Expected Results:
- Foundation: ~3000×3000×500 mm
- Reinforcement: 20mm @ 125mm c/c
- All checks: PASS
```

## การแก้ไขปัญหาทั่วไป

### ❌ ปัญหา: Import Error
```
Solution: ตรวจสอบว่าได้ติดตั้ง dependencies ครบแล้ว
pip install -r requirements_streamlit.txt
```

### ❌ ปัญหา: Port Already in Use
```
Solution: เปลี่ยน port ในการรัน
streamlit run streamlit_app.py --server.port 8502
```

### ❌ ปัญหา: Material Properties Invalid
```
Solution: ตรวจสอบค่าความแข็งแรงวัสดุให้อยู่ในช่วงที่ ACI 318M-25 กำหนด
- f'c: 17-83 MPa
- fy: 280-550 MPa
```

### ❌ ปัญหา: Foundation Design Failed
```
Solution: ปรับเปลี่ยนพารามิเตอร์ดังนี้
- เพิ่มขนาดฐานราก
- เพิ่มความหนาฐานราก
- ลดโหลดที่กระทำ
- เพิ่มกำลังรับแรงอัดของดิน
```

## การพัฒนาเพิ่มเติม

### 🚀 Features ในอนาคต
- [ ] **Export to PDF/Excel**: ส่งออกรายงานการออกแบบ
- [ ] **3D Visualization**: แสดงภาพ 3 มิติของฐานราก
- [ ] **Multiple Foundation Types**: ฐานรากหลายประเภท
- [ ] **Seismic Design**: การออกแบบต้านทานแผ่นดินไหว
- [ ] **Cost Estimation**: ประมาณการต้นทุน
- [ ] **User Templates**: เทมเพลตสำหรับใช้งานบ่อย

### 🔧 การปรับปรุงเทคนิค
- [ ] **Database Integration**: เชื่อมต่อฐานข้อมูล
- [ ] **API Development**: สร้าง REST API
- [ ] **Mobile Responsive**: รองรับการใช้งานบนมือถือ
- [ ] **Multi-language Support**: รองรับหลายภาษา

## การสนับสนุนและติดต่อ

### 📚 เอกสารอ้างอิง
- [ACI 318M-25 Standard](https://www.concrete.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Python Foundation Design](https://github.com/buildsmart888/FoundationDesign-ACI318)

### 🐛 รายงานปัญหา
หากพบปัญหาการใช้งาน กรุณารายงานผ่าน:
- GitHub Issues
- Email: technical.support@example.com

### 📝 License
โปรเจกต์นี้ใช้ลิขสิทธิ์ตาม MIT License

---

**Foundation Design - ACI 318M-25 Streamlit App**  
*Building Code Requirements for Structural Concrete (Metric)*  
*Chapter 13.1 Foundations*
