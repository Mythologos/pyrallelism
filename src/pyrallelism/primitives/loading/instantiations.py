from xml.etree import ElementTree as ETModule
from xml.etree.ElementTree import Element, ElementTree

from .base import BaseParallelismLoader
from ..typing import TokenIdentifiers


class TSVLoader(BaseParallelismLoader):
    @staticmethod
    def _read_file(filepath: str, **kwargs) -> list[TokenIdentifiers]:
        with open(filepath, encoding="utf-8", mode="r") as input_file:
            rows: list[str] = input_file.readlines()
            header_row, *table_rows = rows
            header_items = header_row.strip().split("\t")

            if (len(header_items) - 1) % 2 != 0:
                raise ValueError("The number of ID lines (sans the token) must be divisible by 2, "
                                 "with 2 IDs (for a parallelism and branch) being required per stratum.")

            stratum_count: int = (len(header_items) - 1) % 2 if kwargs["stratum_count"] is None \
                else kwargs["stratum_count"]

            data_rows: list[list[tuple[int, int]]] = []
            for row in table_rows:
                _, *ids = row.strip().split("\t")

                stratum_ids: list[tuple[int, int]] = []
                for index in range(0, len(ids), 2):
                    parallelism_id, branch_id = ids[index:index + 2]
                    current_ids: tuple[int, int] = (int(parallelism_id), int(branch_id))
                    stratum_ids.append(current_ids)

                assert len(stratum_ids) == stratum_count
                data_rows.append(stratum_ids)

        stratum_rows: list[TokenIdentifiers] = list(zip(*data_rows))
        return stratum_rows


class XMLLoader(BaseParallelismLoader):
    @staticmethod
    def _read_file(filepath: str, **kwargs) -> list[TokenIdentifiers]:
        xml_file: ElementTree = ETModule.parse(filepath)
        root: Element = xml_file.getroot()

        words: list[Element] = root.findall(".//word")

        if kwargs["stratum_count"] is not None:
            stratum_count: int = kwargs["stratum_count"]
        elif root.attrib.get("stratum_count", None) is not None:
            stratum_count = int(root.attrib["stratum_count"])
        else:
            raise ValueError(f"No stratum count was provided or found in the given file, <{filepath}>.")

        stratum_rows: list[TokenIdentifiers] = []
        for stratum in range(0, stratum_count):
            stratum_rows.append([])
            for word in words:
                parallelism_id: int = int(word.attrib.get(f"parallelism_id_{stratum + 1}", -1))
                branch_id: int = int(word.attrib.get(f"branch_id_{stratum + 1}", -1))
                stratum_token_ids: tuple[int, int] = (parallelism_id, branch_id)
                stratum_rows[-1].append(stratum_token_ids)

        return stratum_rows
