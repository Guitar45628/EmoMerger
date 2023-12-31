# รายละเอียดโปรแกรม "EmoMerger"

![image](https://github.com/Guitar45628/EmoMerger/assets/66988309/76a01d78-c4a3-4cb2-8a7a-ecd28124f26f)


โปรแกรมนี้เป็นโปรแกรม GUI ด้วย tkinter ใน Python ที่ชื่อ "EmoMerger" ที่อนุญาตให้คุณลากและวางไฟล์ CSV เข้าสู่แอปพลิเคชันเพื่อรวมข้อมูลจากไฟล์ CSV หลาย ๆ ไฟล์ในรายการเข้าไปในไฟล์ CSV เดียว โดยเลือกเฉพาะคอลัมน์ที่คุณสนใจ (โดยเลือกจากรายการของส่วนท้ายของชื่อคอลัมน์ที่ยอมรับที่กำหนดไว้ใน `accepted_endings`) และรวมข้อมูลทั้งหมดในแถวที่มี "LocalTimestamp" เหมือนกัน ลงในไฟล์ผลลัพธ์ CSV โดยให้ผู้ใช้สามารถเลือกชื่อไฟล์ผลลัพธ์เมื่อรวมเสร็จสิ้น.

## ฟีเจอร์หลัก

1. **ลากและวางไฟล์ CSV**: คุณสามารถลากไฟล์ CSV จากเครื่องคอมพิวเตอร์ของคุณและวางลงในช่องข้อความที่ว่างเปล่าที่อยู่ด้านบนของหน้าต่างโปรแกรม.

2. **เลือกส่วนท้ายของไฟล์**: คุณสามารถเลือกส่วนท้ายของชื่อคอลัมน์ที่คุณต้องการให้รวมเข้าด้วยกัน โดยใช้ Checkboxes ที่อยู่ด้านขวาของหน้าต่าง.

3. **แสดงรายการไฟล์**: รายการไฟล์ CSV ที่ถูกลากและวางจะแสดงในตารางที่ตั้งชื่อ "No." และ "ชื่อไฟล์" ซึ่งคุณสามารถเห็นชื่อไฟล์ที่ถูกลากมา.

4. **รวมไฟล์**: เมื่อคุณเลือกและรวมไฟล์ที่คุณต้องการ, คุณสามารถคลิกที่ปุ่ม "รวมไฟล์" เพื่อเลือกตำแหน่งและป้อนชื่อไฟล์ผลลัพธ์. โปรแกรมจะรวมข้อมูลจากไฟล์ CSV และบันทึกไฟล์ผลลัพธ์ที่คุณเลือก.

5. **ลบรายการที่เลือก**: หากคุณต้องการลบไฟล์ CSV ที่เลือก, คุณสามารถเลือกไฟล์ในรายการและคลิกที่ปุ่ม "ลบรายการที่เลือก" เพื่อลบไฟล์เหล่านั้นออกจากรายการ.

## ความสามารถเพิ่มเติม

โปรแกรมนี้อนุญาตให้คุณดำเนินการรวมไฟล์ CSV จากหลาย ๆ ไฟล์ที่มีรูปแบบและโครงสร้างคอลัมน์ที่แตกต่างกันเข้าสู่ไฟล์ CSV เดียว โดยการเลือกคอลัมน์ที่คุณต้องการเพียงอย่างเดียว และบันทึกไฟล์ผลลัพธ์ไว้ในตำแหน่งที่คุณต้องการ.

ความสามารถในการลากและวางไฟล์ได้ถูกเพิ่มเข้ามาด้วยการใช้ `TkinterDnD` library ซึ่งช่วยในการจัดการกับการลากและวางไฟล์ใน tkinter โดยไม่จำเป็นต้องเพิ่มเติมโมดูลนอกจาก `tkinter` และ `pandas` สำหรับการทำงานรวมข้อมูล.
