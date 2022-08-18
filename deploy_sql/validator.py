from pandera import DataFrameSchema, Column, Check, Index, MultiIndex
import pandera

schema = DataFrameSchema(
    columns={
        "passenger_count": Column(
            dtype=pandera.engines.numpy_engine.Float64,
            checks=[Check(lambda s: s >= 0),
                       Check(lambda s: s <= 10)],
            nullable=True,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
        ),
        "trip_distance": Column(
            dtype=pandera.engines.numpy_engine.Float64,
            checks=[Check(lambda s: s >= 0)],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
        ),
        "fare_amount": Column(
            dtype=pandera.engines.numpy_engine.Float64,
            checks=None,
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
        ),
        "fare_amount_per_person": Column(
            dtype=pandera.engines.numpy_engine.Float64,
            checks=None,
            nullable=True,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
        ),
    },
    index=Index(
        dtype=pandera.engines.numpy_engine.Int64,
        checks=None,
        nullable=False,
        coerce=False,
        name=None,
    ),
    coerce=False,
    strict="filter",
    name=None,
)
