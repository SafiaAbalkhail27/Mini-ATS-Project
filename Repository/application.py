from utils.database_helper import db_helper
import pandas as pd

class ApplicationRepository:
    @staticmethod
    def _get_all_applications():
        query = "SELECT ApplicationID, JobID, CandidateID FROM Application"
        result, error = db_helper._execute_query(query)
        if result is not None:
            result = result.to_dict(orient='records')
        return result, error

    @staticmethod
    def _add_application(job_id, candidate_id):
        query = "INSERT INTO Application (JobID, CandidateID) VALUES (%s, %s) RETURNING ApplicationID"
        result, error = db_helper._execute_query(query, (job_id, candidate_id))
        if result is not None:
            result = pd.DataFrame(result).to_dict(orient='records')
        return result, error