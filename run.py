import os

os.environ["MINIO_ACCESS_KEY"] = "OOZ67ZZ3IC594HVU39MM"
os.environ["MINIO_SECRET_KEY"] = "IbjiNZdvODrzgzM4J3wBcutgCnBkI2CGt4KFpHxL"
os.environ["MINIO_ENDPOINT"] = "s3.gwdg.de"

import datajoint as dj
dj.config["database.host"] = '134.76.19.44'
dj.config["database.password"] = 'duchess robin strife rename'
dj.config["database.user"] = 'eoffenberg'

from nnfabrik.main import my_nnfabrik
import torch
from nnfabrik.templates import TrainedModelBase, DataInfoBase

dj.config['enable_python_native_blobs'] = True
dj.config['nnfabrik.schema_name'] = "eoffenberg_v4_neuromodulation"
if not "stores" in dj.config:
    dj.config["stores"] = {}
dj.config["stores"]["minio"] = {  # store in s3
        "protocol": "s3",
        "endpoint": os.environ.get("MINIO_ENDPOINT", "DUMMY_ENDPOINT"),
        "bucket": "nnfabrik",
        "location": "dj-store",
        "access_key": os.environ.get("MINIO_ACCESS_KEY", "FAKEKEY"),
        "secret_key": os.environ.get("MINIO_SECRET_KEY", "FAKEKEY"),
    }

main_nnfabrik = my_nnfabrik(
    schema="eoffenberg_v4_neuromodulation",
    use_common_fabrikant=False,
)
Fabrikant, Dataset, Model, Trainer, Seed = map(
    main_nnfabrik.__dict__.get, ["Fabrikant", "Dataset", "Model", "Trainer", "Seed"]
)

schema = main_nnfabrik.schema


@schema
class TrainedModelDJ(TrainedModelBase):
    table_comment = "Trained models"
    storage = "minio"

    model_table = Model
    dataset_table = Dataset
    trainer_table = Trainer
    seed_table = Seed
    user_table = Fabrikant

model_hashes = (Model & 'model_ts > "2023-04-17"' & 'model_ts < "2023-04-19"').fetch("model_hash")
other_rests = { 'dataset_hash': '0d73713f106d71e0920e07ae1b818896',
                'trainer_hash': '11b0d8b378d05b7f33cc41a9e345574a',
                'seed':'5000'}
restrictions = dj.AndList([[dict(model_hash = i) for i in model_hashes], other_rests])

TrainedModelDJ().populate(restrictions, display_progress=True,reserve_jobs=True) 