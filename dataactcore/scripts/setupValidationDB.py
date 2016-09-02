from dataactcore.models.baseInterface import databaseSession
from dataactcore.models.validationModels import FileTypeValidation, FieldType, RuleSeverity

def setupValidationDB():
    """Create validation tables from model metadata and do initial inserts."""
    insertCodes()

def insertCodes():
    """Insert static data."""
    with databaseSession() as session:

        # insert file types
        fileTypeList = [
            (1, 'appropriations', 'appropriations file',1),
            (2, 'program_activity','program activity and object class file',2),
            (3, 'award_financial', 'award_financial file',3),
            (4, 'award', 'award file',4),
            (5, 'award_procurement', 'award procurement file', 5)
            ]
        for f in fileTypeList:
            fileType = FileTypeValidation(file_id=f[0], name=f[1], description=f[2], file_order = f[3])
            session.merge(fileType)

        # insert field types
        fieldTypeList = [
            (1, 'INT', 'integer type'),
            (2, 'DECIMAL', 'decimal type '),
            (3, 'BOOLEAN', 'yes/no'),
            (4, 'STRING', 'string type'),
            (5, 'LONG', 'long integer')
            ]
        for f in fieldTypeList:
            fieldType = FieldType(field_type_id=f[0], name=f[1], description=f[2])
            session.merge(fieldType)

        # insert rule severity
        severityList = [
            (1, 'warning', 'warning'),
            (2, 'fatal', 'fatal error')
        ]
        for s in severityList:
            ruleSeverity = RuleSeverity(rule_severity_id=s[0], name=s[1], description=s[2])
            session.merge(ruleSeverity)

        session.commit()

if __name__ == '__main__':
    setupValidationDB()
