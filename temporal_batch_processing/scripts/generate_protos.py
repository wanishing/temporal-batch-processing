import os
import shutil
import subprocess
from typing import List

from grpc_tools import protoc

PROTO_DIR = "protos"
PROTO_FILE = "order.proto"
DESTINATION_DIR = "temporal_batch_processing/src/generated_protos"


def _clean_directory(directory: str) -> None:
    """Remove directory if it exists."""
    if os.path.exists(directory):
        print(f"\n=== Cleaning directory: {directory} ===")
        shutil.rmtree(directory)
        print("Directory cleaned successfully")


def _ensure_directory(base_dir: str) -> None:
    """Create directory and any necessary parent directories."""
    print(f"\n=== Creating directory: {base_dir} ===")
    os.makedirs(f"{base_dir}", exist_ok=False)
    print("Directory created successfully")


def _fix_imports(target_dir: str, schemas_dir: str, target_files: List[str]) -> None:
    print("\n=== Fixing relative imports ===")
    print(f"Target directory: {target_dir}")
    subprocess.run([
        'protol',
        '--create-package',
        '--in-place',
        '--exclude-google-imports',
        f'--python-out',
        target_dir,
        'protoc',
        f'--proto-path={schemas_dir}',
        *target_files
    ], check=True)
    print("Finished fixing relative imports")


def generate_protos():
    print("\n=== Running protoc compiler ===")
    print(f"Destination: {DESTINATION_DIR}")
    _clean_directory(DESTINATION_DIR)
    _ensure_directory(DESTINATION_DIR)
    _compile_protos()
    _fix_imports(DESTINATION_DIR, PROTO_DIR, [f"{PROTO_DIR}/{PROTO_FILE}"])


def _compile_protos():
    protoc_args = [
        'grpc_tools.protoc',
        f'--proto_path={PROTO_DIR}',
        f'--python_out={DESTINATION_DIR}',
        f'--mypy_out={DESTINATION_DIR}',
        f'--grpc_python_out={DESTINATION_DIR}',
        f'{PROTO_DIR}/{PROTO_FILE}'
    ]
    print("Executing protoc with arguments:\n" + " \\\n".join(protoc_args))
    print()
    try:
        result = protoc.main(protoc_args)
        if result != 0:
            raise Exception(f"protoc failed with exit code {result}")
        print()
        print("Successfully generated Python files")
    except Exception as e:
        raise Exception(f"Failed to generate Python files: {str(e)}")
