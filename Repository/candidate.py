from utils.database_helper import db_helper
import pandas as pd

class CandidateRepository:
    @staticmethod
    def _add_candidate(candidate_name, candidate_major):
        query = """
            INSERT INTO Candidate (CandidateName, CandidateMajor) 
            VALUES (%s, %s) 
            RETURNING CandidateID
        """
        result, error = db_helper._execute_query(query, (candidate_name, candidate_major))
        if result is not None:
            result = result.to_dict(orient='records')
        return result, error

    @staticmethod
    def _get_matching_jobs(candidate_major): #models directory
        query = "SELECT JobID FROM Job WHERE JobSkills->>0 = %s"
        result, error = db_helper._execute_query(query, (candidate_major,))
        if result is not None:
            result = result.to_dict(orient='records')
        return result, error

    @staticmethod
    def _add_application(job_id, candidate_id):  #models directory
        query = "INSERT INTO Application (JobID, CandidateID) VALUES (%s, %s)"
        return db_helper._execute_update(query, (job_id, candidate_id))
