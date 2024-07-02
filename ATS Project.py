from flask import Flask, request, jsonify, render_template
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import OperationalError
import json

def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="Ss1234567",
            host="localhost",
            port="5432"
        )
        print("Connection successful")
        return conn
    except OperationalError as e:
        print(f"The error '{e}' occurred")
        return None

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Job endpoints
@app.route('/job', methods=['POST'])
def add_job():
    data = request.get_json()
    job_skills = data['job_skills']
    job_requirements = data['job_requirements']

    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to the database'}), 500

    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO Job (JobSkills, JobRequirements) VALUES (%s, %s) RETURNING JobID",
                    (json.dumps(job_skills), json.dumps(job_requirements)))
        job_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'Job added successfully', 'job_id': job_id}), 201
    except Exception as e:
        print(f"The error '{e}' occurred while adding a job")
        return jsonify({'error': 'Failed to add job', 'details': str(e)}), 500

@app.route('/job/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to the database'}), 500

    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM Job WHERE JobID = %s", (job_id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'Job deleted successfully'}), 200
    except Exception as e:
        print(f"The error '{e}' occurred while deleting a job")
        return jsonify({'error': 'Failed to delete job', 'details': str(e)}), 500

@app.route('/job', methods=['GET'])
def show_jobs():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to the database'}), 500

    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM Job")
        jobs = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(jobs), 200
    except Exception as e:
        print(f"The error '{e}' occurred while fetching jobs")
        return jsonify({'error': 'Failed to fetch jobs', 'details': str(e)}), 500

# Candidate endpoints
@app.route('/candidate', methods=['POST'])
def add_candidate():
    data = request.get_json()
    candidate_name = data['candidate_name']
    candidate_major = data['candidate_major']
    job_ids = data.get('job_ids', [])  # Assuming job_ids are provided in the POST request

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # Insert the candidate into the Candidate table
        cur.execute("INSERT INTO Candidate (CandidateName, CandidateMajor) VALUES (%s, %s) RETURNING CandidateID",
                    (candidate_name, candidate_major))
        candidate_id = cur.fetchone()[0]

         # Check for jobs where the first skill matches the candidate's major
        cur.execute("SELECT JobID FROM Job WHERE JobSkills->>0 = %s", (candidate_major,))
       # job_ids = cur.fetchall()
        job_ids = [job_id[0] for job_id in cur.fetchall()]

        # Insert entries into Application table for matched jobs
        for job_id in job_ids:
            cur.execute("INSERT INTO Application (JobID, CandidateID) VALUES (%s, %s)", (job_id, candidate_id))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'message': 'Candidate added successfully', 'candidate_id': candidate_id}), 201

    except Exception as e:
        print(f"Error adding candidate: {e}")
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({'error': 'Failed to add candidate'}), 500


# Application endpoints
@app.route('/application', methods=['GET'])
def show_applications():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to the database'}), 500

    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM Application")
        applications = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(applications), 200
    except Exception as e:
        print(f"The error '{e}' occurred while fetching applications")
        return jsonify({'error': 'Failed to fetch applications', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True,port=5001)
