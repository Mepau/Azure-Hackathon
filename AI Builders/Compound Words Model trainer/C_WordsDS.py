import os
from typing import Union, Tuple

from torchtext._internal.module_utils import is_module_available
from torchtext.data.datasets_utils import (
    _wrap_split_argument,
    _create_dataset_directory,
)

if is_module_available("torchdata"):
    from torchdata.datapipes.iter import FileLister, FileOpener, StreamReader


MD5 = {
    "train": "67ae358c5c78b04e1ea93799e2661fcd",
    "test": "1ca41dd85d5d5af3521ebb5c9430c009",
}
DATASET_NAME = "COMPUND_WORDS"

#[docs]@_create_dataset_directory(dataset_name=DATASET_NAME)
@_wrap_split_argument(("train", "test"))
def C_WORDS(root: str, split: Union[Tuple[str], str]):

    if not is_module_available("torchdata"):
        raise ModuleNotFoundError(
            "Package `torchdata` not found. Please install following instructions at `https://github.com/pytorch/data`"
        )

    cache_dp = FileLister(root=root).filter(lambda fname: fname.endswith(split + '.csv'))
    # TODO: read in text mode with utf-8 encoding, see: https://github.com/pytorch/pytorch/issues/72713
    data_dp = FileOpener(cache_dp, mode="b")

    #print(list(data_dp.parse_csv().map(fn=lambda t: (int(t[0]), " ".join(t[1:])))))
    return data_dp.parse_csv().map(fn=lambda t: (int(t[0]), " ".join(t[1:])))