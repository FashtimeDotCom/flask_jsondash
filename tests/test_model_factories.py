import json

from click.testing import CliRunner

from flask_jsondash import model_factories
from flask_jsondash.settings import CHARTS_CONFIG


def test_get_random_group():
    conf_vals = CHARTS_CONFIG.values()
    data = model_factories.get_random_group()
    assert isinstance(data, dict)
    assert 'charts' in data
    assert data in conf_vals


def test_get_random_chart():
    chart = model_factories.get_random_group()
    data = model_factories.get_random_chart(chart)
    assert isinstance(data, tuple)


def test_make_fake_dashboard():
    fdash = model_factories.make_fake_dashboard(name='Foo', max_charts=4)
    assert isinstance(fdash, dict)
    assert fdash.get('name') == 'Foo'


def test_make_fake_chart_data():
    chartdata = model_factories.make_fake_chart_data(name='Foo')
    chartconfig = json.loads(chartdata[1])
    assert isinstance(chartdata, tuple)
    assert isinstance(chartconfig, dict)
    assert chartconfig.get('name') == 'Foo'


def test_insert_dashboards(monkeypatch):
    records = []
    runner = CliRunner()
    args = ['--max-charts', 5, '--records', 5]
    _db = model_factories.adapter
    monkeypatch.setattr(_db, 'create', lambda *a, **kw: records.append(a))
    result = runner.invoke(model_factories.insert_dashboards, args)
    assert result.exit_code == 0
    assert len(records) == 5


def test_delete_all(monkeypatch):
    _db = model_factories.adapter
    monkeypatch.setattr(_db, 'delete_all', lambda *a, **kw: [])
    assert model_factories.delete_all() is None
