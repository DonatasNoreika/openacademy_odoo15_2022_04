# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Session(models.Model):
    _name = "openacademy.session"
    _description = "OpenAcademy Sessions"

    name = fields.Char(string="Name", required=True)
    instructor_id = fields.Many2one('res.partner', string="Instructor", ondelete="set null")
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    course_id = fields.Many2one('openacademy.course', string="Course", ondelete='set null')