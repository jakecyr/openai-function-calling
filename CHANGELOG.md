# Release Notes

## 2.0.0

* Upgrade to the latest OpenAI version that changes from function calling to tools.
* Add the `ToolHelpers` class.

## 1.2.0

* Increase compatible Python version range to include 3.9

## 1.1.0

* Adds the ability to automatically infer a function's definition along with it's parameters automatically from a function reference.

## 1.0.1

* Added the to_dict method back to the Function class and marked it as deprecated. It will be removed in future versions.

## 1.0.0

* Renamed to_dict to to_json_schema.
* Added additional validation conditions when creating and converting Parameters and Functions to JSON schema.
* Add ruff.toml file with additional checks and fixed all linting errors.
* Added additional docstrings.
* Added py.typed file for mypy.

## 0.6.0

* Add new parameter to Parameter class array_item_type to specify the type of array items if type is set to array

## 0.5.0

* Remove the openai dependency since it isn't required to use the package. It must now be installed separately.

## 0.4.0

* Fix bugs in the Parameter class related to required_parameters and add unit tests.

## 0.3.0

* Update the examples link in the README to point to GitHub instead of being relative.

## 0.2.0

* Update README to include details about setting the OpenAI API key and link to the examples

## 0.1.0

* Initial release
