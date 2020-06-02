# from marshmallow import Schema, fields, post_load, validate

# from govtext_cli.constants import Task
# from govtext_cli.helper import resolve_path


# def no_op(*args, **kwargs):
#     pass


# class Enum(fields.String):
#     def _deserialize(self, value, attr, data, **kwargs):
#         return value.upper()


# class DatasetSchema(Schema):
#     name = fields.String(required=True, validate=validate.Length(min=1))
#     filepath = fields.String(validate=validate.Length(min=1))

#     @post_load
#     def get_op(self, data, **kwargs):
#         client = self.context["client"]
#         data["filepath"] = resolve_path(data["filepath"])
#         data["op"] = (
#             client.upload_dataset if "filepath" in data else client.get_dataset_by_name
#         )
#         return data


# class ProcessConfigSchema(Schema):
#     task = Enum(required=True, validate=validate.OneOf(Task.list()))
#     dataset = fields.Nested(DatasetSchema)
#     download_location = fields.String(validate=validate.Length(min=1))

#     @post_load
#     def get_op(self, data, **kwargs):
#         client = self.context["client"]
#         data["download_location"] = resolve_path(data["download_location"])
#         data["download_op"] = (
#             client.download_dataset if "download_location" in data else no_op
#         )
#         return data
