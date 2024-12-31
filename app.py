from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application
app = Flask(__name__)

# Configure the SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for performance

# Initialize the SQLAlchemy instance
db = SQLAlchemy(app)

# Define the Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Task {self.name}>'

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        task_name = request.form['name']
        task_desc = request.form['description']
        new_task = Task(name=task_name, description=task_desc)
        db.session.add(new_task)
        db.session.commit()
    all_tasks = Task.query.all()
    return render_template('index.html', tasks=all_tasks)

@app.route('/delete/<int:task_id>', methods=['GET'])
def delete_task_func(task_id):
    task_to_delete = Task.query.get_or_404(task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
