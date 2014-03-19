from flask import Flask, render_template
from flask.ext.pymongo import PyMongo


app = Flask(__name__)
mongo = PyMongo(app)


@app.route('/')
def home():
	grants = mongo.db.grant_collection.find()
	return render_template('home.html', grants=grants)


@app.route('/amount-by-year/')
def amount_by_year():
	amount_by_year = []
	years = [
		# "2009 and earlier",
		"2010",
		"2011",
		"2012",
		"2013",
		"2014"
	]
	for y in years:
		amount = get_amount_by_year(y)
		amount_by_year.append({
			"year": y,
			"raw_total": amount,
			"formatted_total": format_dollars(amount)
		})
	return render_template('amount_by_year.html', amount_by_year=amount_by_year)


def get_amount_by_year(year_query):
	amount = 0 
	grants_in_year = mongo.db.grant_collection.find({"year": year_query})
	for g in grants_in_year:
		amount += g["amount"]
	return amount


def format_dollars(amount):
	return "${:,.2f}".format(amount)


if __name__ == "__main__":
	app.run(debug=True)