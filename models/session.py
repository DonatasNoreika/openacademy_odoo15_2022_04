# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, exceptions
from datetime import timedelta


class Session(models.Model):
    _name = "openacademy.session"
    _description = "OpenAcademy Sessions"

    name = fields.Char(string=_("Name"), required=True)
    instructor_id = fields.Many2one('res.partner', string=_("Instructor"), ondelete="set null", domain=['|', ('instructor', '=', True), ('category_id.name', 'ilike', 'Teacher')])
    start_date = fields.Date(default=fields.Date.today)
    end_date = fields.Date(string=_("End Date"), store=True,
                           compute='_get_end_date', inverse='_set_end_date')
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string=_("Number of seats"))
    course_id = fields.Many2one('openacademy.course', string=_("Course"), ondelete='set null')
    attendee_ids = fields.Many2many('res.partner', string=_("Attendees"))
    attendees_count = fields.Integer(
        string="Attendees count", compute='_get_attendees_count', store=True)
    taken_seats = fields.Float(string="Taken seats (%)", compute='_taken_seats')
    active = fields.Boolean(default=True)
    color = fields.Integer()
    status = fields.Selection([
        ('draft', _("Draft")),
        ('started', _("Started")),
        ('done', _("Done")),
        ('cancelled', _("Cancelled")),
    ], string=_("Progress"), default='draft', translate=True)

    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for r in self:
            r.attendees_count = len(r.attendee_ids)

    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for record in self:
            if not record.seats:
                record.taken_seats == 0.0
            else:
                record.taken_seats = (len(record.attendee_ids) / record.seats) * 100.0

    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': f"Incorrect 'seats' value",
                    'message': f"The number of available seats may not be negative: {self.seats}",
                },
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': "Too many attendees",
                    'message': "Increase seats or remove excess attendees",
                },
            }

    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise exceptions.ValidationError("A session's instructor can't be an attendee")

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue

            # Add duration to start_date, but: Monday + 5 days = Saturday, so
            # subtract one second to get on Friday instead
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = r.start_date + duration

    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                continue

            # Compute the difference between dates, but: Friday - Monday = 4 days,
            # so add one day to get 5 days instead
            r.duration = (r.end_date - r.start_date).days + 1

    # def send_session_report(self):
    #     # Find the e-mail template
    #     template = self.env.ref('openacademy.openacademy_session_mail_template')
    #     # You can also find the e-mail template like this:
    #     # template = self.env['ir.model.data'].get_object('send_mail_template_demo', 'example_email_template')
    #
    #     # Send out the e-mail template to the user
    #     self.env['mail.template'].browse(template.id).send_mail(self.id)