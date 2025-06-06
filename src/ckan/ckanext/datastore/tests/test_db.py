# encoding: utf-8

import unittest.mock as mock
import pytest

import ckan.lib.jobs as jobs
import ckan.plugins as p
import ckan.tests.factories as factories
import ckan.tests.helpers as helpers
import ckanext.datastore.backend as backend
import ckanext.datastore.backend.postgres as db


@pytest.mark.ckan_config("ckan.plugins", "datastore")
@pytest.mark.usefixtures("with_plugins")
class TestCreateIndexes(object):
    def test_creates_fts_index_using_gist_by_default(self):
        connection = mock.MagicMock()
        context = {"connection": connection}
        resource_id = "resource_id"
        data_dict = {"resource_id": resource_id}

        db.create_indexes(context, data_dict)

        self._assert_created_index_on(
            "_full_text", connection, resource_id, method="gist"
        )

    @pytest.mark.ckan_config("ckan.datastore.default_fts_index_method", "gin")
    def test_default_fts_index_method_can_be_overwritten_by_config_var(self):
        connection = mock.MagicMock()
        context = {"connection": connection}
        resource_id = "resource_id"
        data_dict = {"resource_id": resource_id}

        db.create_indexes(context, data_dict)

        self._assert_created_index_on(
            "_full_text", connection, resource_id, method="gin"
        )

    @pytest.mark.ckan_config(
        "ckan.datastore.default_fts_index_field_types", "text tsvector")
    @mock.patch("ckanext.datastore.backend.postgres._get_fields")
    def test_creates_fts_index_on_all_fields_except_dates_nested_and_arrays_with_english_as_default(
        self, _get_fields
    ):
        _get_fields.return_value = [
            {"id": "text", "type": "text"},
            {"id": "tsvector", "type": "tsvector"},
            {"id": "nested", "type": "nested"},
            {"id": "date", "type": "date"},
            {"id": "text array", "type": "text[]"},
            {"id": "timestamp", "type": "timestamp"},
        ]
        connection = mock.MagicMock()
        context = {"connection": connection}
        resource_id = "resource_id"
        data_dict = {"resource_id": resource_id}

        db.create_indexes(context, data_dict)

        self._assert_created_index_on(
            "text", connection, resource_id, "english"
        )
        self._assert_created_index_on(
            "tsvector", connection, resource_id,
        )

    @pytest.mark.ckan_config(
        "ckan.datastore.default_fts_index_field_types", "")
    @mock.patch("ckanext.datastore.backend.postgres._get_fields")
    def test_creates_no_fts_indexes_by_default(
        self, _get_fields
    ):
        _get_fields.return_value = [
            {"id": "text", "type": "text"},
            {"id": "tsvector", "type": "tsvector"},
            {"id": "nested", "type": "nested"},
            {"id": "date", "type": "date"},
            {"id": "text array", "type": "text[]"},
            {"id": "timestamp", "type": "timestamp"},
        ]
        connection = mock.MagicMock()
        context = {"connection": connection}
        resource_id = "resource_id"
        data_dict = {"resource_id": resource_id}

        db.create_indexes(context, data_dict)

        self._assert_no_index_created_on(
            "text", connection, resource_id, "english"
        )
        self._assert_no_index_created_on(
            "tsvector", connection, resource_id,
        )

    @pytest.mark.ckan_config(
        "ckan.datastore.default_fts_index_field_types", "text tsvector")
    @pytest.mark.ckan_config("ckan.datastore.default_fts_lang", "simple")
    @mock.patch("ckanext.datastore.backend.postgres._get_fields")
    def test_creates_fts_index_on_textual_fields_can_overwrite_lang_with_config_var(
        self, _get_fields
    ):
        _get_fields.return_value = [{"id": "foo", "type": "text"}]
        connection = mock.MagicMock()
        context = {"connection": connection}
        resource_id = "resource_id"
        data_dict = {"resource_id": resource_id}

        db.create_indexes(context, data_dict)

        self._assert_created_index_on("foo", connection, resource_id, "simple")

    @pytest.mark.ckan_config(
        "ckan.datastore.default_fts_index_field_types", "text tsvector")
    @pytest.mark.ckan_config("ckan.datastore.default_fts_lang", "simple")
    @mock.patch("ckanext.datastore.backend.postgres._get_fields")
    def test_creates_fts_index_on_textual_fields_can_overwrite_lang_using_lang_param(
        self, _get_fields
    ):
        _get_fields.return_value = [{"id": "foo", "type": "text"}]
        connection = mock.MagicMock()
        context = {"connection": connection}
        resource_id = "resource_id"
        data_dict = {"resource_id": resource_id, "language": "french"}

        db.create_indexes(context, data_dict)

        self._assert_created_index_on("foo", connection, resource_id, "french")

    def _assert_created_index_on(
        self,
        field,
        connection,
        resource_id,
        lang=None,
        cast=False,
        method="gist",
    ):
        field = u'"{0}"'.format(field)
        if cast:
            field = u"cast({0} AS text)".format(field)
        if lang is not None:
            sql_str = (
                u'ON "resource_id" '
                u"USING {method}(to_tsvector('{lang}', {field}))"
            )
            sql_str = sql_str.format(method=method, lang=lang, field=field)
        else:
            sql_str = u"USING {method}({field})".format(
                method=method, field=field
            )

        calls = connection.execute.call_args_list

        was_called = any(sql_str in str(call.args[0]) for call in calls)

        assert was_called, (
            "Expected 'connection.execute' to have been "
            "called with a string containing '%s'" % sql_str
        )

    def _assert_no_index_created_on(
        self,
        field,
        connection,
        resource_id,
        lang=None,
        cast=False,
        method="gist",
    ):
        field = u'"{0}"'.format(field)
        if cast:
            field = u"cast({0} AS text)".format(field)
        if lang is not None:
            sql_str = (
                u'ON "resource_id" '
                u"USING {method}(to_tsvector('{lang}', {field}))"
            )
            sql_str = sql_str.format(method=method, lang=lang, field=field)
        else:
            sql_str = u"USING {method}({field})".format(
                method=method, field=field
            )

        calls = connection.execute.call_args_list

        was_called = any(sql_str in str(call.args[0]) for call in calls)

        assert not was_called, (
            "Expected 'connection.execute' to not have been "
            "called with a string containing '%s'" % sql_str
        )


class TestGetAllResourcesIdsInDatastore(object):
    @pytest.mark.ckan_config(u"ckan.plugins", u"datastore")
    @pytest.mark.usefixtures(u"with_plugins", u"clean_db")
    def test_get_all_resources_ids_in_datastore(self):
        resource_in_datastore = factories.Resource()
        resource_not_in_datastore = factories.Resource()
        data = {"resource_id": resource_in_datastore["id"], "force": True}
        helpers.call_action("datastore_create", **data)

        resource_ids = backend.get_all_resources_ids_in_datastore()

        assert resource_in_datastore["id"] in resource_ids
        assert resource_not_in_datastore["id"] not in resource_ids


def datastore_job(res_id, value):
    """
    A background job that uses the Datastore.
    """
    app = helpers._get_test_app()
    if not p.plugin_loaded(u"datastore"):
        p.load("datastore")
    data = {
        "resource_id": res_id,
        "method": "insert",
        "records": [{"value": value}],
    }

    with app.flask_app.test_request_context():
        helpers.call_action("datastore_upsert", **data)


class TestBackgroundJobs(helpers.RQTestBase):
    """
    Test correct interaction with the background jobs system.
    """
    @pytest.mark.ckan_config(u"ckan.plugins", u"datastore")
    @pytest.mark.usefixtures(u"with_plugins", u"clean_db")
    def test_worker_datastore_access(self, app):
        """
        Test DataStore access from within a worker.
        """
        pkg = factories.Dataset()
        data = {
            "resource": {"package_id": pkg["id"]},
            "fields": [{"id": "value", "type": "int"}],
        }

        table = helpers.call_action("datastore_create", **data)
        res_id = table["resource_id"]
        for i in range(3):
            self.enqueue(datastore_job, args=[res_id, i])
        jobs.Worker().work(burst=True)
        # Aside from ensuring that the job succeeded, this also checks
        # that accessing the Datastore still works in the main process.
        result = helpers.call_action("datastore_search", resource_id=res_id)
        assert [0, 1, 2] == [r["value"] for r in result["records"]]
