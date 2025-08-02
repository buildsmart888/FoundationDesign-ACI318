# 🏗️ Foundation Design - ACI 318M-25 Streamlit App

## 🚀 การเริ่มต้นใช้งาน

### วิธีการรัน:
```bash
# วิธีที่ 1: ใช้ Batch File
run_streamlit.bat

# วิธีที่ 2: Command Line
streamlit run streamlit_app.py --server.port 8501
```

### 🌐 URL แอปพลิเคชัน:
**http://localhost:8501**

---

## 📋 วิธีการใช้งาน

### 1. กรอกข้อมูลใน Sidebar:

#### 🏛️ Column Properties:
- **Column Length** (mm): 200-2000
- **Column Width** (mm): 200-2000

#### ⚖️ Loads:
- **Dead Load** (kN): น้ำหนักคงที่
- **Live Load** (kN): น้ำหนักจร  
- **Wind Load** (kN): แรงลม (optional)

#### 🏗️ Foundation Parameters:
- **Foundation Thickness** (mm): 200-1500
- **Allowable Bearing Capacity** (kN/m²): 50-1000

#### 🧱 Material Properties:
- **f'c** (MPa): กำลังอัดคอนกรีต 17-83
- **fy** (MPa): จุดครากเหล็ก 280-550

### 2. คลิกปุ่ม "🔄 Run Foundation Analysis"

### 3. ดูผลลัพธ์ใน 5 แท็บ:
- **📐 Geometry**: ขนาดฐานรากและวัสดุ
- **💪 Flexural Design**: การออกแบบแรงดัด
- **✂️ Shear Design**: การออกแบบแรงเฉือน
- **📋 Summary**: สรุปการออกแบบ
- **📊 Visualization**: แสดงภาพและกราฟ

---

## ✅ มาตรฐานการออกแบบ

### ACI 318M-25 Compliance:
- **Chapter 13.1**: Foundations
- **Section 5.3**: Load combinations (1.2D + 1.6L)
- **Section 7**: Flexural design (Whitney stress block)
- **Section 22**: Shear design (punching & one-way)

### Load Factors:
- Dead Load: **1.2**
- Live Load: **1.6**
- Wind Load: **1.0**

### Strength Reduction Factors (φ):
- Flexure: **0.9**
- Shear: **0.75**

---

## 📊 ตัวอย่างการใช้งาน

### Example 1: อาคารสำนักงาน
```
Input:
- Dead Load: 800 kN
- Live Load: 300 kN
- Column: 400×400 mm
- f'c: 30 MPa, fy: 420 MPa
- Soil: 200 kN/m²

Expected Output:
- Foundation: ~2500×2500×400 mm
- Reinforcement: 16mm @ 150mm c/c
- Status: ✅ PASS
```

### Example 2: โรงงาน
```
Input:
- Dead Load: 1200 kN
- Live Load: 600 kN
- Column: 500×500 mm
- f'c: 35 MPa, fy: 420 MPa
- Soil: 150 kN/m²

Expected Output:
- Foundation: ~3000×3000×500 mm
- Reinforcement: 20mm @ 125mm c/c
- Status: ✅ PASS
```

---

## 🛠️ การแก้ไขปัญหา

### ❌ Import Error:
```bash
pip install -r requirements_streamlit.txt
```

### ❌ Port Already in Use:
```bash
streamlit run streamlit_app.py --server.port 8502
```

### ❌ Material Properties Invalid:
- ตรวจสอบ f'c: 17-83 MPa
- ตรวจสอบ fy: 280-550 MPa

### ❌ Foundation Design Failed:
- เพิ่มขนาดฐานราก
- เพิ่มความหนาฐานราก
- ลดโหลด
- เพิ่มกำลังรับแรงอัดดิน

---

## 🎯 Features

✅ **ACI 318M-25 Compliant**  
✅ **Real-time Calculation**  
✅ **Interactive Visualization**  
✅ **Comprehensive Reports**  
✅ **Material Validation**  
✅ **Multiple Design Checks**  

---

## 📞 สนับสนุน

- 📧 Email: support@foundationdesign.com
- 🌐 GitHub: FoundationDesign-ACI318
- 📚 Documentation: [Link to docs]

---

**Foundation Design - ACI 318M-25**  
*Building Code Requirements for Structural Concrete (Metric)*
