from algorithms.recommendation import pipeline
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

_path_cur = Path(__file__).resolve().absolute().parent
_path_temp = _path_cur / 'temp'
if not _path_temp.is_dir():
    raise FileNotFoundError(f'Temp folder not exist: "{_path_temp}"')


@app.route('/')
def index():
    return 'hello'


def get_job_recommends(pdf_path):
    cv_text = pipeline.cv_from_pdf(pdf_path)
    return pipeline.get_job_recommendations(cv_text)


@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        save_path = str(_path_temp / uploaded_file.filename)
        uploaded_file.save(save_path)
        print(f'uploaded file saved to "{save_path}"')
        results = get_job_recommends(save_path)
        print(f'returned {len(results)} jobs')
        return jsonify(results)

    return jsonify({'error': 'unknown'})


if __name__ == '__main__':
    app.run()
