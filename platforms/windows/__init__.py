from core.fetcher import GenericFetcher
from core.parser   import GenericParser
from core.exporter_csv import GenericCSVExporter
from core.registry import register

register('windows', GenericFetcher, GenericParser, GenericCSVExporter)
