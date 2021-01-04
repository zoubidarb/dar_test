# -*- coding: utf-8 -*-

#    Copyright 2020 Youssef EL OUAHBY <youssef.elouahby@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" Darbtech Res Partner CRM Lead Wizard """

from odoo import models, fields, api

class DarbtechResPartnerCrmLeadWizard(models.TransientModel):
    """ Darbtech Res Partner CRM Lead Wizard """
    _name = 'darbtech.res.partner.crm.lead.wizard'
    _description = 'Darbtech Res Partner CRM Lead Wizard'

    state = fields.Selection([('init', 'Initial'), ('final', 'Final')],
                             default='init')


    name = fields.Char('Opportunity', required=True, index=True)
    partner_id = fields.Many2one('res.partner', string='Customer', track_visibility='onchange', track_sequence=1, index=True,
        help="Linked partner (optional). Usually created when converting the lead. You can find a partner by its Name, TIN, Email or Internal Reference.")

    team_id = fields.Many2one('crm.team', string='Sales Team', oldname='section_id', default=lambda self: self.env['crm.team'].sudo()._get_default_team_id(user_id=self.env.uid),
        index=True, track_visibility='onchange', help='When sending mails, the default email address is taken from the Sales Team.')
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, track_visibility='onchange', default=lambda self: self.env.user)


    priority = fields.Selection(
        [('0', 'Low'),
         ('1', 'Medium'),
         ('2', 'High'),
         ('3', 'Very High')], string='Priority', index=True, default='0')
    tag_ids = fields.Many2many('crm.lead.tag', 'crm_lead_tag_rel', 'lead_id', 'tag_id', string='Tags', help="Classify and analyze your lead/opportunity categories like: Training, Service")
    reminder_date = fields.Date()


    @api.multi
    def previous(self):
        """ Previous and goes to user and periode choices """
        self.ensure_one()
        self.state = 'init'
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': self._name,
            'res_id': self[0].id,
            'target': 'new'
        }

    @api.multi
    def next(self):
        """ Next and goes to summary """
        self.ensure_one()
        self.state = 'final'
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': self._name,
            'res_id': self[0].id,
            'target': 'new'
        }

    @api.multi
    def create_lead(self):
        """ Next and goes to summary """
        self.ensure_one()
        values = self.get_values()
        values.update({'type': 'lead'})
        self.env['crm.lead'].create(values)

    def get_values(self):
        self.ensure_one()
        return {
            'name': self.name,
            'partner_id': self.partner_id.id,
            'partner_name': self.partner_id.company_name,

            'street': self.partner_id.street,
            'street2': self.partner_id.street2,
            'city': self.partner_id.city,
            'state_id': self.partner_id.state_id.id,
            'zip': self.partner_id.zip,
            'country_id': self.partner_id.country_id.id,
            'website': self.partner_id.website,
            'user_id': self.user_id.id,
            'team_id': self.team_id.id,

            'contact_name': self.partner_id.name,
            'title': self.partner_id.title.id,
            'email_from': self.partner_id.email,
            'phone': self.partner_id.phone,
            'mobile': self.partner_id.mobile,
            'priority': self.priority,
            'tag_ids': self.tag_ids.ids,
            'reminder_date': self.reminder_date

        }
