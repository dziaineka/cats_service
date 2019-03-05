import data
import pytest


@pytest.fixture(scope='module')
def cats_data():
    yield data.Data()


@pytest.mark.parametrize(
    'parameters',
    [
        None,
        {
            'attribute': 'name',
            'order': 'asc',
            'offset': '5',
            'limit': '6',
        },
        {
            'attribute': 'name',
            'order_invalid': 'asc',
            'offset': '5',
            'limit': '6',
        },

    ]
    )
def test_get_cats(parameters, cats_data):
    assert isinstance(cats_data.get_cats(parameters), str)


@pytest.mark.parametrize(
    'parameters',
    [
        dict(),

        b"{\"name\": \"Tihon\", \"color\": \"red & white\", " +
        b"\"tail_length\": 15, \"whiskers_length\": 45}",

        {
            'attribute': 'name',
            'order': 'asc',
            'offset': '5',
            'limit': '6',
        },
        {
            'name': 'Tihon',
            'color': 'red & white',
            'tail_length': '15',
            'whiskers_length': '12',
        }
    ]
    )
def test_add_cat(parameters, cats_data):
    assert isinstance(cats_data.add_cat(parameters), str)
