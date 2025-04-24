PROJECT_SUCCESSFULLY_CREATED = 'Provided CloudFormation Template has been successfully processed and a new IriusRisk ' \
                               'project has been created with the provided metadata'
PROJECT_SUCCESSFULLY_UPDATED = 'IriusRisk project has been updated with the latest changes from the CloudFormation ' \
                               'Template provided'
UNAUTHORIZED_EXCEPTION = 'Authentication information is missing, invalid or not granted to perform this action'
BAD_REQUEST = 'Bad request'
FORBIDDEN_OPERATION = 'Forbidden operation'
PROJECT_NOT_FOUND = 'Project not found'
UNEXPECTED_API_ERROR = 'Unexpected API error'
INCONSISTENT_IDS = 'Generated OTM file has inconsistent IDs'
OTM_SCHEMA_IS_NOT_VALID = 'OTM schema is not valid'
OTM_FILE_NOT_FOUND = 'Cannot find OTM file'
OTM_SUCCESSFULLY_CREATED = 'Provided source file has been successfully processed and a new OTM file ' \
                               'has been created'
MAPPING_FILE_NOT_FOUND = 'Cannot find mapping file'
MAPPING_FILE_SCHEMA_NOT_VALID = 'Mapping files are not valid'
ERROR_WRITING_THREAT_MODEL = 'Unable to create the threat model'
IAC_FILE_IS_NOT_VALID = 'Provided IaC file is not valid'
DIAGRAM_FILE_IS_NOT_VALID = 'Provided diagram file is not valid'
NOT_PARSEABLE_SOURCE_FILES = 'The source files are not parseable'

CANNOT_RECOGNIZE_GIVEN_DIAGRAM_TYPE = 'Cannot recognize given diagram type'

# CLI
SOURCE_FILE_NAME = 'source-file'
SOURCE_FILES_NAME = 'source-files'

IAC_TYPE_NAME = '--iac-type'
IAC_TYPE_SHORTNAME = '-t'
IAC_TYPE_DESC = 'The IaC file type.'
IAC_TYPE_SUPPORTED = ['CLOUDFORMATION', 'TERRAFORM', 'TFPLAN']

DIAGRAM_TYPE_NAME = '--diagram-type'
DIAGRAM_TYPE_SHORTNAME = '-g'
DIAGRAM_TYPE_DESC = 'The diagram file type.'
DIAGRAM_TYPE_SUPPORTED = ['VISIO', 'LUCID', 'DRAWIO','ABACUS']

ETM_TYPE_NAME = '--etm-type'
ETM_TYPE_SHORTNAME = '-e'
ETM_TYPE_DESC = 'The etm file type.'
ETM_TYPE_SUPPORTED = ['MTMT']
ETM_MAPPING_FILE_NAME = '--etm-mapping-file'
ETM_MAPPING_FILE_DESC = 'External Threat Model mapping file to validate.'

DEFAULT_MAPPING_FILE_NAME = '--default-mapping-file'
DEFAULT_MAPPING_FILE_SHORTNAME = '-d'
DEFAULT_MAPPING_FILE_DESC = 'Default mapping file to parse the diagram file.'

CUSTOM_MAPPING_FILE_NAME = '--custom-mapping-file'
CUSTOM_MAPPING_FILE_SHORTNAME = '-c'
CUSTOM_MAPPING_FILE_DESC = 'Custom mapping file to parse the diagram file.'

OUTPUT_FILE_NAME = '--output-file'
OUTPUT_FILE_SHORTNAME = '-o'
OUTPUT_FILE_DESC = 'OTM output file.'
OUTPUT_FILE = 'threatmodel.otm'
SUMMARY_FILE_DESC = 'Summary output file.'

PROJECT_NAME_NAME = '--project-name'
PROJECT_NAME_SHORTNAME = '-n'
PROJECT_NAME_DESC = 'Project name.'

PROJECT_ID_NAME = '--project-id'
PROJECT_ID_SHORTNAME = '-i'
PROJECT_ID_DESC = 'Project id.'

OTM_INPUT_FILE_NAME = '--otm-file'
OTM_INPUT_FILE_SHORTNAME = '-o'
OTM_INPUT_FILE_DESC = 'OTM input file.'

VALIDATE_MAPPING_FILE_NAME = '--mapping-file'
VALIDATE_MAPPING_FILE_SHORTNAME = '-m'
VALIDATE_MAPPING_FILE_DESC = 'Mapping file to validate.'

VALIDATE_MAPPING_FILE_TYPE_NAME = '--mapping-type'
VALIDATE_MAPPING_FILE_TYPE_SHORTNAME = '-t'
VALIDATE_MAPPING_FILE_TYPE_DESC = 'Mapping file type to validate.'
MAPPING_FILE_TYPE_SUPPORTED = ['CLOUDFORMATION', 'TERRAFORM', 'VISIO', 'MTMT', 'LUCID', 'DRAWIO']

