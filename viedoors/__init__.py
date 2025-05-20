"""
Loader File
Author: Michael Kohlegger
Date: Jan. 2025
"""


from .loader.bst_loader import BSTLoader
from .loader.cad_loader import CADLoader
from .loader.flt_loader import FLTLoader
from .loader.npa_loader import NPALoader
from .loader.hm_loader import HMLoader
from .loader.fm_loader import FMLoader
from .merger.file_merger import FileMerger
from .merger.util import eliminate_duplicates
from .merger.util import count_duplicates
from .merger.util import clean_merge
from .functions import calculate_duplicate_info