from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        dbname="protip",
        user="postgres",
        password="amit",
        host="localhost"
    )
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT * FROM protip;')
    stocks = cur.fetchall()

    cur.execute('SELECT SUM(invested_amount) FROM protip;')
    total_invested = round(cur.fetchone()[0] or 0, 2)

    cur.execute('SELECT SUM(present_value) FROM protip;')
    total_value = round(cur.fetchone()[0] or 0, 2)

    total_profit_loss = round(total_value - total_invested, 2)
    profit_loss_percent = round((total_profit_loss / total_invested) * 100 if total_invested else 0, 2)

    cur.close()
    conn.close()

    return render_template('index.html', stocks=stocks, total_invested=total_invested,
                            total_value=total_value, total_profit_loss=total_profit_loss,
                            profit_loss_percent=profit_loss_percent)

@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        company_name = request.form['company_name']
        symbol = request.form['symbol']
        bought_price = request.form['bought_price']
        current_price = request.form['current_price']
        units = request.form['units']
        invested_date = request.form['invested_date']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''INSERT INTO protip (company_name, symbol, bought_price, current_price, units, invested_date) 
                        VALUES (%s, %s, %s, %s, %s, %s)''',
                    (company_name, symbol, bought_price, current_price, units, invested_date))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM protip WHERE s_no = %s', (id,))
    stock = cur.fetchone()

    if request.method == 'POST':
        company_name = request.form['company_name']
        symbol = request.form['symbol']
        bought_price = request.form['bought_price']
        current_price = request.form['current_price']
        units = request.form['units']
        invested_date = request.form['invested_date']

        cur.execute('''UPDATE protip 
                        SET company_name = %s, symbol = %s, bought_price = %s, 
                            current_price = %s, units = %s, invested_date = %s 
                        WHERE s_no = %s''',
                    (company_name, symbol, bought_price, current_price, units, invested_date, id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))

    cur.close()
    conn.close()
    return render_template('edit.html', stock=stock)

@app.route('/delete/<int:id>', methods=('POST',))
def delete(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM protip WHERE s_no = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
