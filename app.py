from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# ฟังก์ชันเชื่อมต่อฐานข้อมูล
def get_db_connection():
    return mysql.connector.connect(
        host='db',            # ถ้าใช้ Docker Compose ชื่อ service คือ 'db'
        user='root',
        password='pass123',
        database='finalexam'
    )

# หน้า Landing Page
@app.route('/')
def index():
    return render_template('index.html')

# หน้าเกี่ยวกับฉัน
@app.route('/about')
def about():
    return render_template('about.html')

# หน้าข้อมูลวิจัย + แสดงอ้างอิงจาก DB
@app.route('/myresearch')
def myresearch():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM reference")
    references = cursor.fetchall()
    conn.close()
    return render_template('myresearch.html', references=references)

# หน้าแสดง/จัดการอ้างอิง (Add/Delete)
@app.route('/reference')
def reference():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM reference")
    references = cursor.fetchall()
    conn.close()
    return render_template('reference.html', references=references)

# เพิ่มข้อมูลอ้างอิง
@app.route('/reference/add', methods=['POST'])
def add_reference():
    title = request.form['title']
    pdf_url = request.form['pdf_url']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reference (title, pdf_url) VALUES (%s, %s)", (title, pdf_url))
    conn.commit()
    conn.close()
    return redirect('/reference')

# ลบข้อมูลอ้างอิง
@app.route('/reference/delete/<int:id>', methods=['POST'])
def delete_reference(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reference WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect('/reference')

# เริ่มต้นแอป
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)