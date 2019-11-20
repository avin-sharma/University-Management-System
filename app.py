import os
from university import University
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/instructors')
def get_db_instructor_table():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        stevens = University(current_dir, ('\t', True), ('\t', True), ('\t', True), ('\t', True), os.path.join(current_dir, 'database.db'))
        print(stevens)
        return render_template('instructors.html', title = 'Instructors Table', instructors = stevens.get_instructors_table_dicts())
    except (KeyError, ValueError) as e:
        print("Bad data encountered.\n" + str(e))
    except FileNotFoundError as e:
        print('Wrong folder path or missing files.\n' + str(e))


app.run(debug = True)