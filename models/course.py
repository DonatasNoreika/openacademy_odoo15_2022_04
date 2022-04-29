# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Course(models.Model):
    _name = "openacademy.course"
    _description = "OpenAcademy Courses"

    name = fields.Char(string=_("Title"), required=True)
    description = fields.Text(string=_("Description"))
    responsible_id = fields.Many2one('res.users', string="Responsible", ondelete='set null')
    sessions_ids = fields.One2many('openacademy.session', 'course_id')
    image = fields.Image("Image", attachment=True)

    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "The title of the course should not be the description"),

        ('name_unique',
         'UNIQUE(name)',
         "The course title must be unique"),
    ]
