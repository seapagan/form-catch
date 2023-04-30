"""This file contains Custom Metadata for your API Project.

Be aware, this will be re-generated any time you run the
'api-admin custom metadata' command!
"""
from config.helpers import MetadataBase

custom_metadata = MetadataBase(
    title="Form Catcher",
    description="Capture Form data from your static websites",
    repository="https://github.com/seapagan/form-catch",
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    contact={
        "name": "Grant Ramsay (seapagan)",
        "url": "https://www.gnramsay.com",
    },
    email="seapagan@gmail.com",
    year="2023",
)
