from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:123369Ugwueze@cis2368db.c6s8i3sqjaj6.us-east-1.rds.amazonaws.com/StockBrokerage'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Investor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    
    stock_transactions = db.relationship('StockTransaction', backref='investor', cascade='all, delete-orphan')
    bond_transactions = db.relationship('BondTransaction', backref='investor', cascade='all, delete-orphan')

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stockname = db.Column(db.String(100), nullable=False)
    abbreviation = db.Column(db.String(10), nullable=False)
    currentprice = db.Column(db.Float, nullable=False)
    
    stock_transactions = db.relationship('StockTransaction', backref='stock', cascade='all, delete-orphan')

class Bond(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bondname = db.Column(db.String(100), nullable=False)
    abbreviation = db.Column(db.String(10), nullable=False)
    currentprice = db.Column(db.Float, nullable=False)
    
    bond_transactions = db.relationship('BondTransaction', backref='bond', cascade='all, delete-orphan')

class StockTransaction(db.Model):
    __tablename__ = 'stocktransaction'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())
    investorid = db.Column(db.Integer, db.ForeignKey('investor.id'), nullable=False)
    stockid = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class BondTransaction(db.Model):
    __tablename__ = 'bondtransaction'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())
    investorid = db.Column(db.Integer, db.ForeignKey('investor.id'), nullable=False)
    bondid = db.Column(db.Integer, db.ForeignKey('bond.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


# Create an investor
@app.route('/investor', methods=['POST'])
def create_investor():
    data = request.json
    new_investor = Investor(firstname=data['firstname'], lastname=data['lastname'])
    db.session.add(new_investor)
    db.session.commit()
    return jsonify({"message": "Investor created successfully."})

# Read all investors
@app.route('/investor', methods=['GET'])
def get_investors():
    investors = Investor.query.all()
    return jsonify([{"id": inv.id, "firstname": inv.firstname, "lastname": inv.lastname} for inv in investors])

# Update an investor
@app.route('/investor/<int:id>', methods=['PUT'])
def update_investor(id):
    data = request.json
    investor = Investor.query.get(id)
    if not investor:
        return jsonify({"message": "Investor not found."})
    
    investor.firstname = data['firstname']
    investor.lastname = data['lastname']
    db.session.commit()
    return jsonify({"message": "Investor updated successfully."})

# Delete an investor
@app.route('/investor/<int:id>', methods=['DELETE'])
def delete_investor(id):
    investor = Investor.query.get(id)
    if not investor:
        return jsonify({"message": "Investor not found."})
    
    db.session.delete(investor)
    db.session.commit()
    return jsonify({"message": "Investor deleted successfully."})

# Create a stock
@app.route('/stock', methods=['POST'])
def create_stock():
    data = request.json
    new_stock = Stock(stockname=data['stockname'], abbreviation=data['abbreviation'], currentprice=data['currentprice'])
    db.session.add(new_stock)
    db.session.commit()
    return jsonify({"message": "Stock created successfully."})

# Update a stock
@app.route('/stock/<int:id>', methods=['PUT'])
def update_stock(id):
    data = request.json
    stock = Stock.query.get(id)
    if not stock:
        return jsonify({"message": "Stock not found."})
    
    stock.stockname = data['stockname']
    stock.abbreviation = data['abbreviation']
    stock.currentprice = data['currentprice']
    db.session.commit()
    return jsonify({"message": "Stock updated successfully."})

# Delete a stock
@app.route('/stock/<int:id>', methods=['DELETE'])
def delete_stock(id):
    stock = Stock.query.get(id)
    if not stock:
        return jsonify({"message": "Stock not found."})
    
    db.session.delete(stock)
    db.session.commit()
    return jsonify({"message": "Stock deleted successfully."})

# Create a bond
@app.route('/bond', methods=['POST'])
def create_bond():
    data = request.json
    new_bond = Bond(bondname=data['bondname'], abbreviation=data['abbreviation'], currentprice=data['currentprice'])
    db.session.add(new_bond)
    db.session.commit()
    return jsonify({"message": "Bond created successfully."})

# Update a bond
@app.route('/bond/<int:id>', methods=['PUT'])
def update_bond(id):
    data = request.json
    bond = Bond.query.get(id)
    if not bond:
        return jsonify({"message": "Bond not found."})
    
    bond.bondname = data['bondname']
    bond.abbreviation = data['abbreviation']
    bond.currentprice = data['currentprice']
    db.session.commit()
    return jsonify({"message": "Bond updated successfully."})

# Delete a bond
@app.route('/bond/<int:id>', methods=['DELETE'])
def delete_bond(id):
    bond = Bond.query.get(id)
    if not bond:
        return jsonify({"message": "Bond not found."})
    
    db.session.delete(bond)
    db.session.commit()
    return jsonify({"message": "Bond deleted successfully."})

# Get an investor's portfolio (stocks and bonds)
@app.route('/investor/<int:id>/portfolio', methods=['GET'])
def get_portfolio(id):
    investor = Investor.query.get(id)
    if not investor:
        return jsonify({"message": "Investor not found."})
    
    stocks = StockTransaction.query.filter_by(investorid=id).all()
    bonds = BondTransaction.query.filter_by(investorid=id).all()

    stock_portfolio = [{"stockname": s.stock.stockname, "quantity": s.quantity} for s in stocks]
    bond_portfolio = [{"bondname": b.bond.bondname, "quantity": b.quantity} for b in bonds]

    return jsonify({"stocks": stock_portfolio, "bonds": bond_portfolio})

# Create a stock transaction
@app.route('/transaction/stock', methods=['POST'])
def create_stock_transaction():
    data = request.json
    new_transaction = StockTransaction(investorid=data['investorid'], stockid=data['stockid'], quantity=data['quantity'])
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({"message": "Stock transaction created successfully."})

# Delete a stock transaction
@app.route('/transaction/stock/<int:id>', methods=['DELETE'])
def delete_stock_transaction(id):
    transaction = StockTransaction.query.get(id)
    if not transaction:
        return jsonify({"message": "Transaction not found."})
    
    db.session.delete(transaction)
    db.session.commit()
    return jsonify({"message": "Stock transaction deleted successfully."})

# Create a bond transaction
@app.route('/transaction/bond', methods=['POST'])
def create_bond_transaction():
    data = request.json
    new_transaction = BondTransaction(investorid=data['investorid'], bondid=data['bondid'], quantity=data['quantity'])
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({"message": "Bond transaction created successfully."})

# Delete a bond transaction
@app.route('/transaction/bond/<int:id>', methods=['DELETE'])
def delete_bond_transaction(id):
    transaction = BondTransaction.query.get(id)
    if not transaction:
        return jsonify({"message": "Transaction not found."})
    
    db.session.delete(transaction)
    db.session.commit()
    return jsonify({"message": "Bond transaction deleted successfully."})

if __name__ == '__main__':
    app.run(debug=True)
