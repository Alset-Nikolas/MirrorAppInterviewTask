from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship


def AssociationColumn(foreign_key_column_name, ondelete='CASCADE', primary_key=False, **kwargs):  # noqa
    return Column(
        ForeignKey(foreign_key_column_name, ondelete=ondelete),
        nullable=kwargs.pop('nullable', False),
        primary_key=primary_key,
        **kwargs,
    )


def association_relationship(
    mapper_class_name,
    back_populates,
    foreign_keys=None,
    lazy='noload',
    **kwargs,
):
    return relationship(
        mapper_class_name,
        foreign_keys=foreign_keys,
        back_populates=back_populates,
        lazy=lazy,
        **kwargs,
    )
