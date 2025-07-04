from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, List, Dict

class Fetcher(ABC):
    @abstractmethod
    def download(self, force: bool = False) -> Path: ...

class Parser(ABC):
    @abstractmethod
    def parse(self, bundle_json: Dict[str, Any]) -> List[Dict[str, Any]]: ...

class Exporter(ABC):
    @abstractmethod
    def export(self, rows: List[Dict[str, Any]], out_path: Path) -> None: ...
