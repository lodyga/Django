from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class NamingConvention:
    inputs_list: str
    operations_list: str
    arguments_list: str
    expected_list: str


@dataclass(frozen=True)
class BinaryTreeConfig:
    utils_file: str
    build: str
    serialize: str


@dataclass(frozen=True)
class LinkedListConfig:
    utils_file: str
    build: str
    serialize: str


@dataclass(frozen=True)
class ClassDesignConfig:
    utils_file: str


@dataclass(frozen=True)
class SolutionConfig:
    instance_code: str
    instance_pattern: str


@dataclass(frozen=True)
class LanguageConfig:
    print: str
    serialize: str

    solution: SolutionConfig
    binary_tree: BinaryTreeConfig
    linked_list: LinkedListConfig
    class_design: ClassDesignConfig

    naming: NamingConvention

    run_tests_function: str
    in_place_utils_file: str
    heap_utils_file: str = ""


def get_language_name(language):
    language_name = language.name if hasattr(language, "name") else language

    if language_name == "C++":
        language_name = "Cpp"

    return language_name


class LanguageAdapter(ABC):
    config: LanguageConfig

    @property
    def solution(self) -> SolutionConfig:
        return self.config.solution

    @property
    def binary_tree(self) -> BinaryTreeConfig:
        return self.config.binary_tree

    @property
    def linked_list(self) -> LinkedListConfig:
        return self.config.linked_list

    @property
    def class_design(self) -> ClassDesignConfig:
        return self.config.class_design

    @property
    def naming(self) -> NamingConvention:
        return self.config.naming

    @property
    def run_tests_function(self) -> str:
        return self.config.run_tests_function

    @property
    def in_place_utils_file(self) -> str:
        return self.config.in_place_utils_file

    @property
    def heap_utils_file(self) -> str:
        return self.config.heap_utils_file

    def print_call(self, expression: str) -> str:
        return f"{self.config.print}({expression})"

    def serialize_call(self, expression: str) -> str:
        return f"{self.config.serialize}({expression})"


class PythonAdapter(LanguageAdapter):
    config = LanguageConfig(
        print="print",
        serialize="json.dumps",
        solution=SolutionConfig(
            instance_code="\nsolution = Solution()\n",
            instance_pattern=r"solution\s*=\s*Solution\(\)\s*",
        ),
        binary_tree=BinaryTreeConfig(
            utils_file="binary_tree_utils.py",
            build="build_binary_tree",
            serialize="serialize_binary_tree",
        ),
        linked_list=LinkedListConfig(
            utils_file="linked_list_utils.py",
            build="build_linked_list",
            serialize="serialize_linked_list",
        ),
        class_design=ClassDesignConfig(
            utils_file="class_design_utils.py",
        ),
        naming=NamingConvention(
            inputs_list="inputs_list",
            operations_list="operations_list",
            arguments_list="arguments_list",
            expected_list="expected_list",
        ),
        run_tests_function="run_tests",
        in_place_utils_file="in_place_utils.py",
    )


class JavaScriptAdapter(LanguageAdapter):
    config = LanguageConfig(
        print="console.log",
        serialize="JSON.stringify",
        solution=SolutionConfig(
            instance_code="\nconst solution = new Solution();\n",
            instance_pattern=r"const\s+solution\s*=\s*new\s+Solution\(\)\s*;?",
        ),
        binary_tree=BinaryTreeConfig(
            utils_file="binary-tree-utils.js",
            build="buildBinaryTree",
            serialize="serializeBinaryTree",
        ),
        linked_list=LinkedListConfig(
            utils_file="linked-list-utils.js",
            build="buildLinkedList",
            serialize="serializeLinkedList",
        ),
        class_design=ClassDesignConfig(
            utils_file="class-design-utils.js",
        ),
        naming=NamingConvention(
            inputs_list="inputsList",
            operations_list="operationsList",
            arguments_list="argumentsList",
            expected_list="expectedList",
        ),
        run_tests_function="runTests",
        in_place_utils_file="in-place-utils.js",
        heap_utils_file="heap-utils.js",
    )


class CppAdapter(LanguageAdapter):
    config = LanguageConfig(
        print="print",  # print sericalized
        serialize="",
        solution=SolutionConfig(
            instance_code="\nSolution solution;\n",
            instance_pattern=r"Solution\s*solution\s*",
        ),
        binary_tree=BinaryTreeConfig(
            utils_file="binary_tree_utils.cpp",
            build="build_binary_tree",
            serialize="serialize_binary_tree",
        ),
        linked_list=LinkedListConfig(
            utils_file="linked_list_utils.cpp",
            build="build_linked_list",
            serialize="serialize_linked_list",
        ),
        class_design=ClassDesignConfig(
            utils_file="class_design_utils.cpp",
        ),
        naming=NamingConvention(
            inputs_list="inputs_list",
            operations_list="operations_list",
            arguments_list="arguments_list",
            expected_list="expected_list",
        ),
        run_tests_function="run_tests",
        in_place_utils_file="in_place_utils.cpp",
    )


class JavaAdapter(LanguageAdapter):
    config = LanguageConfig(
        print="System.out.println",
        serialize="Arrays.toString",
        solution=SolutionConfig(
            instance_code="\nSolution solution = new Solution();\n",
            instance_pattern=r"Solution\s*solution\s*=\s*new\s*Solution\(\)\s*",
        ),
        binary_tree=BinaryTreeConfig(
            utils_file="binary_tree_utils.cpp",
            build="build_binary_tree",
            serialize="serialize_binary_tree",
        ),
        linked_list=LinkedListConfig(
            utils_file="linked_list_utils.cpp",
            build="build_linked_list",
            serialize="serialize_linked_list",
        ),
        class_design=ClassDesignConfig(
            utils_file="class_design_utils.cpp",
        ),
        naming=NamingConvention(
            inputs_list="inputs_list",
            operations_list="operations_list",
            arguments_list="arguments_list",
            expected_list="expected_list",
        ),
        run_tests_function="runTests",
        in_place_utils_file="in_place_utils.cpp",
    )

class TypeScriptAdapter(LanguageAdapter):
    config = LanguageConfig(
        print="console.log",
        serialize="JSON.stringify",
        solution=SolutionConfig(
            instance_code="\nconst solution = new Solution();\n",
            instance_pattern=r"const\s+solution\s*=\s*new\s+Solution\(\)\s*;?",
        ),
        binary_tree=BinaryTreeConfig(
            utils_file="binary-tree-utils.js",
            build="buildBinaryTree",
            serialize="serializeBinaryTree",
        ),
        linked_list=LinkedListConfig(
            utils_file="linked-list-utils.js",
            build="buildLinkedList",
            serialize="serializeLinkedList",
        ),
        class_design=ClassDesignConfig(
            utils_file="class-design-utils.js",
        ),
        naming=NamingConvention(
            inputs_list="inputsList",
            operations_list="operationsList",
            arguments_list="argumentsList",
            expected_list="expectedList",
        ),
        run_tests_function="runTests",
        in_place_utils_file="in-place-utils.js",
        heap_utils_file="heap-utils.js",
    )


LANGUAGE_ADAPTERS = {
    "Python": PythonAdapter(),
    "JavaScript": JavaScriptAdapter(),
    "Cpp": CppAdapter(),
    "Java": JavaAdapter(),
}
