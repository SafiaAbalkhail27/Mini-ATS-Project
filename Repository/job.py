from utils.database_helper import db_helper
import pandas as pd
import json

class JobRepository:
    @staticmethod
    def _add_job(job_skills, job_requirements):
        query = """
            INSERT INTO Job (JobSkills, JobRequirements) 
            VALUES (%s, %s) 
            RETURNING JobID
        """
        result, error = db_helper._execute_query(query, (job_skills, job_requirements))
        #result, error = db_helper.execute_query(query, (json.dumps(job_skills), json.dumps(job_requirements)))

        if result is not None:
            result = result.to_dict(orient='records')
        return result, error

    @staticmethod
    def _delete_job(job_id):
        query = "DELETE FROM Job WHERE JobID = %s"
        return db_helper._execute_update(query, (job_id,))

    @staticmethod
    def _get_all_jobs():
        query = "SELECT JobID, JobSkills,JobRequirements FROM Job"
        result, error = db_helper._execute_query(query)
        if result is not None:
            result = result.to_dict(orient='records')
        return result, error
