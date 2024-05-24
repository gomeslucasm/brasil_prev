from conftest import db
import pytest


@pytest.fixture
def delete_entity_on_db(db):
    def fn(instance):
        db.delete(instance)
        db.commit()

    return fn
