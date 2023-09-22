import flask
from flask import jsonify
import psycopg2
import os

host = "0.0.0.0"
port = 5000

try:
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        database=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD')
    )
    print("Conexão bem-sucedida!")

except psycopg2.Error as e:
    print(f"Erro ao conectar-se ao PostgreSQL: {e}")

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "<h1>API is working</h1>"
    
# @app.route('/products', methods=['GET'])
# def products():
#     try:
#         cur = conn.cursor()
#         cur.execute("SELECT * FROM products")
#         rows = cur.fetchall()
#         cur.close()
#         return jsonify(rows)
#     except psycopg2.Error as e:
#         return f"Erro ao consultar o banco de dados: {e}"

@app.route('/products', methods=['GET'])
def products():
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, name, description, price, stock_quantity FROM products")
        rows = cur.fetchall()
        cur.close()

        products_list = []
        for row in rows:
            product = {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "price": float(row[3]),
                "stock_quantity": row[4]
            }
            products_list.append(product)

        return jsonify(products_list)
    except psycopg2.Error as e:
        return f"Erro ao consultar o banco de dados: {e}"

    
@app.route('/products/<int:id>', methods=['GET'])
def product(id):
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM products WHERE id = {id}")
        row = cur.fetchone()
        cur.close()
        product = {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "price": float(row[3]),
                "stock_quantity": row[4]
            }
        return jsonify(product)
    except psycopg2.Error as e:
        return f"Erro ao consultar o banco de dados: {e}"
    
@app.route('/products', methods=['POST'])
def create_product():
    request_data = flask.request.get_json()
    name = request_data['name']
    price = request_data['price']
    description = request_data['description']
    stock_quantity = request_data['stock_quantity']
    try:
        cur = conn.cursor()
        cur.execute(f"INSERT INTO products (name, price, description, stock_quantity) VALUES ('{name}', {price}, '{description}', {stock_quantity})")
        conn.commit()
        cur.close()
        return jsonify(request_data)
    except psycopg2.Error as e:
        return f"Erro ao inserir dados no banco dwee dados: {e}"

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    try:
        cur = conn.cursor()
        cur.execute(f"DELETE FROM products WHERE id = {id}")
        conn.commit()
        cur.close()
        return jsonify({"message": "Produto deletado com sucesso!"})
    except psycopg2.Error as e:
        return f"Erro ao deletar produto: {e}"

@app.route('/products/<int:id>', methods=['PATCH'])
def update_product(id):
    request_data = flask.request.get_json()
    name = request_data['name']
    price = request_data['price']
    description = request_data['description']
    stock_quantity = request_data['stock_quantity']
    try:
        cur = conn.cursor()
        cur.execute(f"UPDATE products SET name = '{name}', price = {price}, description = '{description}', stock_quantity = {stock_quantity} WHERE id = {id}")
        conn.commit()
        cur.close()
        return jsonify(request_data)
    except psycopg2.Error as e:
        return f"Erro ao atualizar produto: {e}"
    
if __name__ == '__main__':
    app.run(host=host, port=port, debug=True)
