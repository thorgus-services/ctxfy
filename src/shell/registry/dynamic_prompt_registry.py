import inspect
from typing import Any, Callable, Dict

from fastmcp import Context, FastMCP

from src.core.models.specification_result import SaveDirectoryPath
from src.core.models.specification_workflow import BusinessRequirements
from src.shell.adapters.prompt_loaders.yaml_prompt_loader import YAMLPromptLoader


class DynamicPromptRegistry:
    def __init__(self) -> None:
        self._prompts: Dict[str, Any] = {}
        self._yaml_loader = YAMLPromptLoader()
        self._registered_functions: Dict[str, Callable[..., Any]] = {}

    def load_and_register_all_prompts(self, mcp: FastMCP) -> None:
        all_prompts_data = self._yaml_loader.all_prompts_data
        if all_prompts_data is None:
            self._yaml_loader.load_prompt_template("specification_save_instruction")
            all_prompts_data = self._yaml_loader.all_prompts_data

        if not all_prompts_data:
            return

        for prompt_name, prompt_config in all_prompts_data.items():
            self._create_and_register_prompt(mcp, prompt_name, prompt_config)

    def _create_and_register_prompt(self, mcp: FastMCP, prompt_name: str, prompt_config: Dict[str, Any]) -> None:
        parameters: list[dict[str, Any]] = prompt_config.get('parameters', [])

        func = self._create_dynamic_function(prompt_name, prompt_config, parameters)

        func.__name__ = prompt_name.replace('-', '_').replace(' ', '_')
        func.__doc__ = prompt_config.get('description', f'Prompt for: {prompt_name}')

        self._registered_functions[prompt_name] = func

        mcp.prompt(
            name=prompt_name,
            description=prompt_config.get('description', f'Prompt for: {prompt_name}'),
        )(func)

    def _create_dynamic_function(self, prompt_name: str, prompt_config: Dict[str, Any], parameters: list[dict[str, Any]]) -> Callable[..., Any]:
        template = prompt_config.get('template', '')

        dynamic_prompt_impl = self._create_prompt_implementation(prompt_name, template, parameters)

        sig = self._build_signature(parameters)
        dynamic_prompt_impl.__signature__ = sig  # type: ignore[attr-defined]

        annotations = self._build_annotations(parameters)
        dynamic_prompt_impl.__annotations__ = annotations

        return dynamic_prompt_impl

    def _create_prompt_implementation(self, prompt_name: str, template: str, parameters: list[dict[str, Any]]) -> Callable[..., Any]:
        async def dynamic_prompt_impl(ctx: Context, *args: Any, **kwargs: Any) -> str:
            param_values: Dict[str, Any] = {}

            for i, param in enumerate(parameters):
                param_name = param.get('name', '')
                if i < len(args):
                    param_values[param_name] = args[i]
                elif param_name in kwargs:
                    param_values[param_name] = kwargs[param_name]
                else:
                    default_val = param.get('default')
                    if default_val is not None:
                        param_values[param_name] = default_val
                    else:
                        raise ValueError(f"Missing required parameter '{param_name}' for prompt {prompt_name}") from None

            try:
                result: str = template.format(**param_values)
                return result
            except KeyError as e:
                raise ValueError(f"Missing required parameter {e} for prompt {prompt_name}") from e

        return dynamic_prompt_impl

    def _build_signature(self, parameters: list[dict[str, Any]]) -> inspect.Signature:
        sig_params = []

        ctx_param = inspect.Parameter(
            name='ctx',
            kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
            annotation=Context
        )
        sig_params.append(ctx_param)

        for param in parameters:
            param_name = param.get('name', '')
            param_type_name = param.get('type', 'str')

            if param_type_name == 'SaveDirectoryPath':
                param_type_annotation: type = SaveDirectoryPath
            elif param_type_name == 'BusinessRequirements':
                param_type_annotation = BusinessRequirements
            elif param_type_name == 'int':
                param_type_annotation = int
            elif param_type_name == 'float':
                param_type_annotation = float
            elif param_type_name == 'bool':
                param_type_annotation = bool
            else:
                param_type_annotation = str

            default_val = param.get('default', inspect.Parameter.empty)
            if default_val == inspect.Parameter.empty:
                default: Any = inspect.Parameter.empty
            else:
                try:
                    if param_type_annotation is int:
                        default = int(default_val)
                    elif param_type_annotation is float:
                        default = float(default_val)
                    elif param_type_annotation is bool:
                        default = bool(default_val) if isinstance(default_val, bool) else str(default_val).lower() in ('true', '1', 'yes', 'on')
                    else:
                        default = default_val
                except (ValueError, TypeError):
                    default = default_val

            param_spec = inspect.Parameter(
                name=param_name,
                kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                annotation=param_type_annotation,
                default=default
            )
            sig_params.append(param_spec)

        return inspect.Signature(sig_params)

    def _build_annotations(self, parameters: list[dict[str, Any]]) -> dict[str, Any]:
        annotations = {'ctx': Context, 'return': str}
        for param in parameters:
            param_name = param.get('name', '')
            param_type_name = param.get('type', 'str')

            if param_type_name == 'SaveDirectoryPath':
                param_type_for_annotation: type = SaveDirectoryPath
            elif param_type_name == 'BusinessRequirements':
                param_type_for_annotation = BusinessRequirements
            elif param_type_name == 'int':
                param_type_for_annotation = int
            elif param_type_name == 'float':
                param_type_for_annotation = float
            elif param_type_name == 'bool':
                param_type_for_annotation = bool
            else:
                param_type_for_annotation = str

            annotations[param_name] = param_type_for_annotation

        return annotations


dynamic_prompt_registry: DynamicPromptRegistry = DynamicPromptRegistry()