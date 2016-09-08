from datetime import datetime
from unittest.mock import Mock
from dataactcore.models.jobModels import Submission, Job, FileGenerationTask
from dataactbroker.handlers.fileHandler import FileHandler

def test_start_generation_job(database, brokerDb):
    fileHandler = FileHandler(None,brokerDb,True)
    # Mock D file API
    fileHandler.call_d_file_api = Mock(return_value=True)
    file_type = "D2"
    file_type_name = "award"
    sub, uploadJob, validationJob = setupSubmission(brokerDb, file_type_name)
    success, errorResponse = fileHandler.startGenerationJob(sub.submission_id, file_type)
    assert(success)
    # Get file generation task created
    task = brokerDb.jobDb.query(FileGenerationTask).filter(FileGenerationTask.submission_id == sub.submission_id).filter(FileGenerationTask.file_type_id == brokerDb.jobDb.getFileTypeId(file_type_name)).one()
    assert(task.job_id == uploadJob.job_id)
    assert(uploadJob.job_status_id == brokerDb.jobDb.getJobStatusId("running"))

    # Mock an empty response
    fileHandler.call_d_file_api = Mock(return_value=True)
    sub, uploadJob, validationJob = setupSubmission(brokerDb, file_type_name)
    success, errorResponse = fileHandler.startGenerationJob(sub.submission_id, file_type)
    assert(success)
    task = brokerDb.jobDb.query(FileGenerationTask).filter(FileGenerationTask.submission_id == sub.submission_id).filter(FileGenerationTask.file_type_id == brokerDb.jobDb.getFileTypeId(file_type_name)).one()
    assert(task.job_id == uploadJob.job_id)
    assert(uploadJob.filename == "#")
    assert(uploadJob.job_status_id == brokerDb.jobDb.getJobStatusId("finished"))

def setupSubmission(brokerDb, file_type_name):
    """ Create a submission with jobs for specified file type """
    # Create test submission
    sub = Submission(datetime_utc=datetime.utcnow(), user_id=1, cgac_code = "SYS", reporting_start_date = "01/01/2016", reporting_end_date = "01/31/2016")
    brokerDb.jobDb.session.commit()
    # Add jobs
    uploadJob = Job(job_status_id = brokerDb.jobDb.getJobStatusId("ready"), job_type_id = brokerDb.jobDb.getJobTypeId("file_upload"),
                    submission_id = sub.submission_id, file_type_id = brokerDb.jobDb.getFileTypeId(file_type_name))
    validationJob =  Job(job_status_id = brokerDb.jobDb.getJobStatusId("ready"), job_type_id = brokerDb.jobDb.getJobTypeId("csv_record_validation"),
                    submission_id = sub.submission_id, file_type_id = brokerDb.jobDb.getFileTypeId(file_type_name))
    brokerDb.jobDb.session.add(uploadJob)
    brokerDb.jobDb.session.add(validationJob)
    brokerDb.jobDb.session.commit()
    return sub, uploadJob, validationJob
