from datetime import datetime
from unittest.mock import Mock
from dataactcore.models.jobModels import Submission, Job, FileGenerationTask
from dataactcore.models.baseInterface import BaseInterface
from dataactcore.interfaces.interfaceHolder import InterfaceHolder
from dataactcore.scripts.setupAllDB import setupAllDB
from dataactbroker.handlers.fileHandler import FileHandler

def test_start_generation_job(database):
    print("start generation test called")
    interfaces = InterfaceHolder()
    print("DB name is {}".format(BaseInterface.dbName))
    # Set up DBs
    setupAllDB()
    fileHandler = FileHandler(None,interfaces,True)
    # Mock D file API
    fileHandler.call_d_file_api = Mock(return_value=True)
    # Mock request object
    fileHandler.request = MockRequest()
    file_type = "D2"
    file_type_name = "award"
    sub, uploadJob, validationJob = setupSubmission(interfaces, file_type_name)
    print("Submission {}".format(sub.submission_id))
    submissions = interfaces.jobDb.session.query(Submission).all()
    print(str([sub.submission_id for sub in submissions]))
    success, errorResponse = fileHandler.startGenerationJob(sub.submission_id, file_type)
    assert(success)
    # Get file generation task created
    task = interfaces.jobDb.query(FileGenerationTask).filter(FileGenerationTask.submission_id == sub.submission_id).filter(FileGenerationTask.file_type_id == interfaces.jobDb.getFileTypeId(file_type_name)).one()
    assert(task.job_id == uploadJob.job_id)
    assert(uploadJob.job_status_id == interfaces.jobDb.getJobStatusId("running"))

    # Mock an empty response
    fileHandler.call_d_file_api = Mock(return_value=True)
    sub, uploadJob, validationJob = setupSubmission(interfaces, file_type_name)
    success, errorResponse = fileHandler.startGenerationJob(sub.submission_id, file_type)
    assert(success)
    task = interfaces.jobDb.query(FileGenerationTask).filter(FileGenerationTask.submission_id == sub.submission_id).filter(FileGenerationTask.file_type_id == interfaces.jobDb.getFileTypeId(file_type_name)).one()
    assert(task.job_id == uploadJob.job_id)
    assert(uploadJob.filename == "#")
    assert(uploadJob.job_status_id == interfaces.jobDb.getJobStatusId("finished"))

def setupSubmission(interfaces, file_type_name):
    """ Create a submission with jobs for specified file type """
    # Create test submission
    sub = Submission(datetime_utc=datetime.utcnow(), user_id=1, cgac_code = "SYS", reporting_start_date = "01/01/2016", reporting_end_date = "01/31/2016")
    interfaces.jobDb.session.commit()
    # Add jobs
    uploadJob = Job(job_status_id = interfaces.jobDb.getJobStatusId("ready"), job_type_id = interfaces.jobDb.getJobTypeId("file_upload"),
                    submission_id = sub.submission_id, file_type_id = interfaces.jobDb.getFileTypeId(file_type_name))
    validationJob =  Job(job_status_id = interfaces.jobDb.getJobStatusId("ready"), job_type_id = interfaces.jobDb.getJobTypeId("csv_record_validation"),
                    submission_id = sub.submission_id, file_type_id = interfaces.jobDb.getFileTypeId(file_type_name))
    interfaces.jobDb.session.add(uploadJob)
    interfaces.jobDb.session.add(validationJob)
    interfaces.jobDb.session.commit()
    return sub, uploadJob, validationJob

class MockRequest:

    def __init__(self):
        self.headers = {"Content-Type": "application/x-www-form-urlencoded"}
        self.form = {"start": "10/1/2016", "end": "12/31/2016"}
