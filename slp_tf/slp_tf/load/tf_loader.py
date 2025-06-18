import logging
import os
from io import StringIO
from typing import Callable

import hcl2
from deepmerge import always_merger

from slp_base import LoadingIacFileError
from slp_base import ProviderLoader
from slp_tf.slp_tf.parse.mapping.mappers.tf_base_mapper import generate_resource_identifier

logger = logging.getLogger(__name__)


def hcl2_reader(data):
    return hcl2.load(StringIO(initial_value=hcl2_data_as_str(data), newline=None))


def hcl2_data_as_str(data) -> str:
    return data if isinstance(data, str) else data.decode()


def raise_empty_sources_error():
    msg = "IaC file is empty"
    raise LoadingIacFileError("IaC file is not valid", msg, msg)


class TerraformLoader(ProviderLoader):
    """
    Builder for a Terraform class from the xml data
    """

    def __init__(self, sources, iac_files):
        self.sources: [bytes] = sources
        self.iac_files = iac_files
        self.hcl2_reader: Callable = hcl2_reader
        self.terraform: dict = {}

    def load(self):
        try:
            self.__load_source_files()
        except LoadingIacFileError as ex:
            raise ex
        except Exception:
            msg = "Source files could not be parsed"
            raise LoadingIacFileError("IaC file is not valid", msg, msg)

    def get_terraform(self):
        return self.terraform
    
    def __load_source_files(self):
        if not self.sources:
            raise_empty_sources_error()

        for i, source in enumerate(self.sources):
            tf_model = self.__load_hcl2_data(source)
            iac_file = self.iac_files[i]
            base_path = os.path.dirname(iac_file) if iac_file else None
            tf_model = self._enrich_source_model(tf_model, base_path)
            self.__merge_hcl2_data(tf_model)

        if not self.terraform:
            raise_empty_sources_error()

        self._func_squash_terraform()

    def _func_squash_terraform(self):
        if self.terraform is not None and 'resource' in self.terraform:
            for component_type_obj in self.terraform['resource']:
                if isinstance(component_type_obj, dict):
                    resource_type, resource_key, resource_properties = (None,) * 3
                    for component_type, component_name_obj in component_type_obj.items():
                        resource_type = component_type
                        if isinstance(component_name_obj, dict):
                            component_name, properties = list(component_name_obj.items())[0]
                            resource_key = component_name
                            resource_properties = properties
                    component_type_obj["resource_id"] = generate_resource_identifier(resource_type, resource_key)
                    component_type_obj["resource_type"] = resource_type
                    component_type_obj["resource_name"] = resource_key
                    component_type_obj["resource_properties"] = resource_properties
                    # Deprecated, but included for the seek to maximize compatibility between mappings
                    component_type_obj["Type"] = resource_type
                    component_type_obj["_key"] = resource_key
                    component_type_obj["Properties"] = resource_properties

    def __merge_hcl2_data(self, tf_data):
        self.terraform = always_merger.merge(self.terraform, tf_data)

    def __load_hcl2_data(self, source):
        try:
            logger.debug(f"Loading iac data and reading as string")

            tf_data = self.hcl2_reader(source)

            logger.debug("Source data loaded successfully")

            return tf_data
        except Exception as e:
            detail = e.__class__.__name__
            message = e.__str__()
            raise LoadingIacFileError("IaC file is not valid", detail, message)

    def _enrich_source_model(self, source_model, base_path):
        """
        Enriches the source model by replacing Terraform modules with their associated resources.

        Args:
            source_model (dict): The source model containing provider, module, and resource attributes.

        Returns:
            dict: The enriched source model with modules replaced by their associated resources.
        """
        enriched_model = source_model.copy()

        modules = source_model.get('module', [])
        resources = source_model.get('resource', [])
        enriched_resources = resources.copy()

        for module in modules:
            module_name, module_data = next(iter(module.items()))
            module_source = module_data.get('source')
            module_variables = {k: v for k, v in module_data.items() if k != 'source'}

            # Load module definition from the source directory
            module_resources = self._load_module_resources(module_name, module_source, module_variables, base_path)
            enriched_resources.extend(module_resources)

        enriched_model['resource'] = enriched_resources
        if 'module' in enriched_model:
            del enriched_model['module']  # Remove modules after enrichment

        return enriched_model
            
    def _load_module_resources(self, module_name, module_source, module_variables, base_path):
        """
        Loads resources from a Terraform module and resolves variables.

        Args:
            module_source (str): Path to the module directory.
            module_variables (dict): Variables to resolve in the module.

        Returns:
            list: List of resources defined in the module with unique names/keys.
        """
        # Resolve relative paths for module_source
        if module_source and not (module_source.startswith('/') or module_source.startswith('http')):
            module_source = os.path.abspath(os.path.join(base_path, module_source))

        if not module_source or not os.path.isdir(module_source):
            raise ValueError(f"Invalid module source: {module_source}")

        resources = []

        # # Load variables.tf to resolve module parameters
        # variables_tf_path = os.path.join(module_source, 'variables.tf')
        # variables_definitions = {}
        # if os.path.exists(variables_tf_path):
        #     with open(variables_tf_path, 'r') as f:
        #         variables_definitions = hcl2.load(f)

        # # Resolve variables using module_variables
        # resolved_variables = self._resolve_variables(variables_definitions, module_variables)

        merged_tf_data = {}
        for file_name in os.listdir(module_source):
            if file_name.endswith('.tf'):
                file_path = os.path.join(module_source, file_name)
                with open(file_path, 'r') as f:
                    tf_data = hcl2.load(f)
                    merged_tf_data = always_merger.merge(merged_tf_data, tf_data)

        # Resolve variables using variables.tf and module_variables
        variables_definitions = merged_tf_data.get('variable', [])
        resolved_variables = self._resolve_variables(variables_definitions, module_variables)

        # Load resources from main.tf
        # main_tf_path = os.path.join(module_source, 'main.tf')
        # if os.path.exists(main_tf_path):
        #     with open(main_tf_path, 'r') as f:
        #         tf_data = hcl2.load(f)

        # module_resources = tf_data.get('resource', [])
        # module_nested_modules = tf_data.get('module', [])


        module_resources = merged_tf_data.get('resource', [])
        module_nested_modules = merged_tf_data.get('module', [])
        
        for resource_def in module_resources:
            for resource_type, resource_definitions in resource_def.items():
                for resource_name, resource_properties in resource_definitions.items():
                    resolved_resource = self._resolve_resource(resource_properties, resolved_variables)
                    
                    resource = {
                        resource_type: {resource_name: resolved_resource}
                    }
                    resources.append(resource)
                    
        for nested_module in module_nested_modules:
            for nested_module_name, nested_module_data in nested_module.items():
                nested_module_source = nested_module_data.get('source')
                nested_module_variables = {k: v for k, v in nested_module_data.items() if k != 'source'}

                nested_resources = self._load_module_resources(nested_module_name, nested_module_source, nested_module_variables, module_source)
                resources.extend(nested_resources)

        return resources
    
    def _resolve_variables(self, variable_list, module_variables):
        """
        Resolves variables in a Terraform module.

        Args:
            variables_definitions (dict): Definitions from variables.tf.
            module_variables (dict): Variables passed to the module.

        Returns:
            dict: Resolved variables.
        """
        resolved = {}
        # variable_list = variables_definitions.get('variable', [])

        for var_def in variable_list:
            for var_name, var_details in var_def.items():
                if var_name in module_variables:
                    resolved[var_name] = module_variables[var_name]
                else:
                    resolved[var_name] = var_details.get('default', None)

        return resolved

    def _resolve_resource(self, resource, resolved_variables):
        """
        Resolves variables in a resource definition.

        Args:
            resource (dict): Resource definition.
            resolved_variables (dict): Resolved variables.

        Returns:
            dict: Resource with variables replaced.
        """
        resolved_resource = resource.copy()
        for key, value in resolved_resource.items():
            if isinstance(value, str) and value.startswith('${') and value.endswith('}'):
                var_name = value[2:-1]
                resolved_resource[key] = resolved_variables.get(var_name, value)
        return resolved_resource

