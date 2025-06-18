from slp_base.slp_base import MappingLoader, MappingValidator
from slp_base.slp_base import OTMProcessor
from slp_base.slp_base import ProviderValidator
from slp_base.slp_base.provider_loader import ProviderLoader
from slp_base.slp_base.provider_parser import ProviderParser
from slp_tf.slp_tf.load.tf_loader import TerraformLoader
from slp_tf.slp_tf.load.tf_mapping_file_loader import TerraformMappingFileLoader
from slp_tf.slp_tf.parse.tf_parser import TerraformParser
from slp_tf.slp_tf.validate.tf_mapping_file_validator import TerraformMappingFileValidator
from slp_tf.slp_tf.validate.tf_validator import TerraformValidator


class TerraformProcessor(OTMProcessor):
    """
    Terraform implementation of OTMProcessor
    """

    def __init__(self, project_id: str, project_name: str, sources: [bytes], mappings: [bytes], iac_files):
        self.project_id = project_id
        self.project_name = project_name
        self.sources = sources
        self.mappings = mappings
        self.iac_files = iac_files

        self.terraform_loader = None
        self.mapping_loader = None

    def get_provider_validator(self) -> ProviderValidator:
        return TerraformValidator(self.sources)

    def get_provider_loader(self) -> ProviderLoader:
        self.terraform_loader = TerraformLoader(self.sources, self.iac_files)
        return self.terraform_loader

    def get_mapping_validator(self) -> MappingValidator:
        return TerraformMappingFileValidator(self.mappings)

    def get_mapping_loader(self) -> MappingLoader:
        self.mapping_loader = TerraformMappingFileLoader(self.mappings)
        return self.mapping_loader

    def get_provider_parser(self) -> ProviderParser:
        return TerraformParser(
                self.project_id,
                self.project_name,
                self.terraform_loader.get_terraform(),
                self.mapping_loader.get_mappings())
