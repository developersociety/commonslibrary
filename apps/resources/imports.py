from collections import namedtuple

# We define a namedtuple to read the CSV data in to.
ResourceCSVRow = namedtuple(
    'Resource', [
        'title',
        'abstract',
        'content',
        'image',
        'tags',
        'organisation',
        'privacy',
        'status',
        'created_by',
    ]
)
