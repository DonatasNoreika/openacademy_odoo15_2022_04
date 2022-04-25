# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Session(models.Model):
    _name = "openacademy.session"
    _description = "OpenAcademy Sessions"

    name = fields.Char(string="Name", required=True)
    instructor_id = fields.Many2one('res.partner', string="Instructor", ondelete="set null", domain=['|', ('instructor', '=', True), ('category_id.name', 'ilike', 'Teacher')])
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    course_id = fields.Many2one('openacademy.course', string="Course", ondelete='set null')
    attendee_ids = fields.Many2many('res.partner', string="Attendees")
    taken_seats = fields.Float(string="Taken seats (%)", compute='_taken_seats')
    active = fields.Boolean(default=True)

    def _taken_seats(self):
        for record in self:
            if not record.seats:
                record.taken_seats == 0.0
            else:
                record.taken_seats = (len(record.attendee_ids) / record.seats) * 100.0