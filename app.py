# app.py
from flask import Flask, request, render_template, jsonify
from utils import *
import threading
import os
PORT = os.environ.get('PORT', 5000)
app = Flask(__name__)

# Global variable to store progress percentage
progress = {"value": 0}

def update_progress(current, total):
    """Helper function to update the progress percentage."""
    progress["value"] = int((current / total) * 100)

@app.route('/', methods=['GET', 'POST'])
def search():
    results = []
    progress["value"] = 0  # Reset progress before starting a new search
    
    if request.method == 'POST':
        name = request.form.get('name', '')
        door = request.form.get('door', '')
        total_circles = len(circles.keys())

        for index, circle in enumerate(circles.keys()):
            try:
                print('processing:', index)
                soup = get_details(circle, name, door)
                table_data = filter_results(soup)
                if table_data:
                    organized_data = print_table(table_data)
                    results.append((circles[circle], organized_data))

                # Update progress after processing each circle
                update_progress(index + 1, total_circles)

            except Exception as e:
                results.append((f"Error processing circle: {circle}", str(e)))
    
    return render_template('index.html', results=results)

@app.route('/api/get-progress', methods=['GET'])
def get_progress():
    """Endpoint to get the current progress percentage."""
    return jsonify(progress)
    
if __name__ == '__main__':
    print('starting web app...')
    app.run(host='0.0.0.0', port=PORT)
