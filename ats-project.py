from flask import Flask, request, jsonify, render_template
from Repository.job import JobRepository
from Repository.candidate import CandidateRepository
from Repository.application import ApplicationRepository

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/job', methods=['POST'])
def _add_job():
    data = request.get_json()

    if not data or 'job_skills' not in data or 'job_requirements' not in data:
        return jsonify({'error': 'Invalid input data'}), 400

    job_skills = data['job_skills']
    job_requirements = data['job_requirements']

    result, error = JobRepository._add_job(job_skills, job_requirements)

    if error:
        return jsonify({'error': 'Failed to add job', 'details': error}), 500
    else:
        job_id = result[0]['jobid']
        return jsonify({'message': 'Job added successfully', 'job_id': job_id}), 201

@app.route('/job/<int:job_id>', methods=['DELETE'])
def _delete_job(job_id):
    error = JobRepository._delete_job(job_id)

    if error:
        return jsonify({'error': 'Failed to delete job', 'details': error}), 500
    else:
        return jsonify({'message': 'Job deleted successfully'}), 200

@app.route('/job', methods=['GET'])
def _show_jobs():
    result, error = JobRepository._get_all_jobs()

    if error:
        return jsonify({'error': 'Failed to fetch jobs', 'details': error}), 500
    else:
        return jsonify(result), 200

@app.route('/candidate', methods=['POST'])
def _add_candidate():
    data = request.get_json()

    if not data or 'candidate_name' not in data or 'candidate_major' not in data:
        return jsonify({'error': 'Invalid input data'}), 400

    candidate_name = data['candidate_name']
    candidate_major = data['candidate_major']

    try:
        result, error = CandidateRepository._add_candidate(candidate_name, candidate_major)

        if error:
            raise Exception(error)

        candidate_id = result[0]['candidateid']

        result, error = CandidateRepository._get_matching_jobs(candidate_major)

        if error:
            raise Exception(error)

        job_ids = [job['jobid'] for job in result]

        for job_id in job_ids:
            error = CandidateRepository._add_application(job_id, candidate_id)

            if error:
                raise Exception(error)

        return jsonify({'message': 'Candidate added successfully', 'candidate_id': candidate_id}), 201

    except Exception as e:
        return jsonify({'error': 'Failed to add candidate', 'details': str(e)}), 500

@app.route('/application', methods=['GET'])
def _show_applications():
    result, error = ApplicationRepository._get_all_applications()

    if error:
        return jsonify({'error': 'Failed to fetch applications', 'details': error}), 500
    else:
        return jsonify(result), 200

@app.route('/application', methods=['POST'])
def _add_application():
    data = request.get_json()

    if not data or 'candidate_id' not in data or 'job_id' not in data:
        return jsonify({'error': 'Invalid input data'}), 400

    job_id = data['job_id']
    candidate_id = data['candidate_id']

    result, error = ApplicationRepository._add_application(job_id, candidate_id)

    if error:
        return jsonify({'error': 'Failed to add application', 'details': error}), 500
    else:
        application_id = result[0]['applicationid']
        return jsonify({'message': 'Application added successfully', 'application_id': application_id}), 201


if __name__ == '__main__':
    app.run(debug=True, port=5001)
