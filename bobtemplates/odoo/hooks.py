# -*- coding: utf-8 -*-
# Copyright © 2016 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import ast
import os
import re

from mrbob.bobexceptions import ValidationError
from mrbob.hooks import show_message
from pkg_resources import parse_version


def _dotted_to_camelcased(dotted):
    return "".join([s.capitalize() for s in dotted.split(".")])


def _dotted_to_underscored(dotted):
    return dotted.replace(".", "_")


def _dotted_to_camelwords(dotted):
    return " ".join([s.capitalize() for s in dotted.split(".")])


def _underscored_to_camelcased(underscored):
    return "".join([s.capitalize() for s in underscored.split("_")])


def _underscored_to_camelwords(underscored):
    return " ".join([s.capitalize() for s in underscored.split("_")])


def _delete_file(configurator, path):
    """remove file and remove it's directories if empty"""
    path = os.path.join(configurator.target_directory, path)
    os.remove(path)
    try:
        os.removedirs(os.path.dirname(path))
    except OSError:
        pass


def _open_manifest(configurator, mode="r"):
    manifest_path = os.path.join(configurator.target_directory, "__openerp__.py")
    if not os.path.exists(manifest_path):
        manifest_path = os.path.join(configurator.target_directory, "__manifest__.py")
        if not os.path.exists(manifest_path):
            raise ValidationError("{} not found".format(manifest_path))
    return open(manifest_path, mode)


def _load_manifest(configurator):
    with _open_manifest(configurator) as f:
        return ast.literal_eval(f.read())


def _insert_manifest_item(configurator, key, item):
    """Insert an item in the list of an existing manifest key"""
    with _open_manifest(configurator) as f:
        manifest = f.read()
    if item in ast.literal_eval(manifest).get(key, []):
        return
    pattern = """(["']{}["']:\\s*\\[)""".format(key)
    repl = """\\1\n        '{}',""".format(item)
    manifest = re.sub(pattern, repl, manifest, re.MULTILINE)
    with _open_manifest(configurator, "w") as f:
        f.write(manifest)


def _add_local_import(configurator, package, module):
    init_path = os.path.join(configurator.target_directory, package, "__init__.py")
    import_string = "from . import {}".format(module)
    if os.path.exists(init_path):
        with open(init_path, "U") as f:
            init = f.read()
    else:
        init = ""
    if import_string not in init.split("\n"):
        open(init_path, "a").write(import_string + "\n")


def _rm_suffix(suffix, configurator, path):
    path = os.path.join(configurator.target_directory, path)
    assert path.endswith(suffix)
    os.rename(path, path[: -len(suffix)])


#
# model hooks
#


def _model_has_view(variables):
    return (
        variables["model.view_form"]
        or variables["model.view_tree"]
        or variables["model.view_search"]
        or variables["model.view_menu"]
    )


def pre_render_model(configurator):
    _load_manifest(configurator)  # check manifest is present
    variables = configurator.variables
    variables["odoo.version"] = int(variables["odoo.version"])
    variables["model.name_underscored"] = _dotted_to_underscored(
        variables["model.name_dotted"]
    )
    variables["model.name_camelcased"] = _dotted_to_camelcased(
        variables["model.name_dotted"]
    )
    variables["model.name_camelwords"] = _dotted_to_camelwords(
        variables["model.name_dotted"]
    )
    variables["addon.name"] = os.path.basename(
        os.path.normpath(configurator.target_directory)
    )


def post_render_model(configurator):
    variables = configurator.variables
    # make sure the models package is imported from the addon root
    _add_local_import(configurator, "", "models")
    # add new model import in __init__.py
    _add_local_import(configurator, "models", variables["model.name_underscored"])
    # views
    view_path = "views/{}.xml".format(variables["model.name_underscored"])
    if _model_has_view(variables):
        _insert_manifest_item(configurator, "data", view_path)
    else:
        _delete_file(configurator, view_path)
    # ACL
    acl_path = "security/{}.xml".format(variables["model.name_underscored"])
    if variables["model.acl"]:
        _insert_manifest_item(configurator, "data", acl_path)
    else:
        _delete_file(configurator, acl_path)
    # demo data
    demo_path = "demo/{}.xml".format(variables["model.name_underscored"])
    if variables["model.demo_data"]:
        _insert_manifest_item(configurator, "demo", demo_path)
    else:
        _delete_file(configurator, demo_path)
    # show message if any
    show_message(configurator)


#
# addon hooks
#


def pre_render_addon(configurator):
    variables = configurator.variables
    variables["odoo.version"] = int(variables["addon.version"].split(".")[0])
    variables["addon.name_camelwords"] = _underscored_to_camelwords(
        variables["addon.name"]
    )


def post_render_addon(configurator):
    variables = configurator.variables
    if variables["addon.oca"]:
        _rm_suffix(".oca", configurator, variables["addon.name"] + "/README.rst.oca")
        _rm_suffix(
            ".oca",
            configurator,
            variables["addon.name"] + "/static/description/icon.png.oca",
        )
    else:
        _delete_file(configurator, variables["addon.name"] + "/README.rst.oca")
        _delete_file(
            configurator, variables["addon.name"] + "/static/description/icon.png.oca"
        )
    version = variables["addon.version"]
    if parse_version(version) >= parse_version("10.0"):
        manifest_file = os.path.join(
            configurator.target_directory, variables["addon.name"] + "/__openerp__.py"
        )
        manifest_new_file = os.path.join(
            configurator.target_directory, variables["addon.name"] + "/__manifest__.py"
        )
        os.rename(manifest_file, manifest_new_file)
    # show message if any
    show_message(configurator)


#
# test hooks
#


def pre_render_test(configurator):
    _load_manifest(configurator)  # check manifest is present
    variables = configurator.variables
    variables["odoo.version"] = int(variables["odoo.version"])
    variables["test.name_camelcased"] = _underscored_to_camelcased(
        variables["test.name_underscored"]
    )
    variables["test.is_class_method"] = variables["test.common_class"] in (
        "SavepointCase",
        "SingleTransactionCase",
    )


def post_render_test(configurator):
    # add new test import in __init__.py
    _add_local_import(
        configurator, "tests", configurator.variables["test.name_underscored"]
    )
    # show message if any
    show_message(configurator)


#
# wizard hooks
#


def _wizard_has_view(variables):
    return (
        variables["wizard.view_form"]
        or variables["wizard.view_action"]
        or variables["wizard.action_multi"]
        or variables["wizard.view_menu"]
    )


def pre_render_wizard(configurator):
    _load_manifest(configurator)  # check manifest is present
    variables = configurator.variables
    variables["odoo.version"] = int(variables["odoo.version"])
    variables["wizard.name_underscored"] = _dotted_to_underscored(
        variables["wizard.name_dotted"]
    )
    variables["wizard.name_camelcased"] = _dotted_to_camelcased(
        variables["wizard.name_dotted"]
    )
    variables["wizard.name_camelwords"] = _dotted_to_camelwords(
        variables["wizard.name_dotted"]
    )
    variables["addon.name"] = os.path.basename(
        os.path.normpath(configurator.target_directory)
    )


def post_render_wizard(configurator):
    variables = configurator.variables
    # make sure the wizards package is imported from the addon root
    _add_local_import(configurator, "", "wizards")
    # add new wizard import in __init__.py
    _add_local_import(configurator, "wizards", variables["wizard.name_underscored"])
    # views
    view_path = "wizards/{}.xml".format(variables["wizard.name_underscored"])
    if _wizard_has_view(variables):
        _insert_manifest_item(configurator, "data", view_path)
    else:
        _delete_file(configurator, view_path)
    # show message if any
    show_message(configurator)
