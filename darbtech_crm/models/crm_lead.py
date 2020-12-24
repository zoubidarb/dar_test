# -*- coding: utf-8 -*-


#    Copyright 2020 Youssef El Ouahby <youssef.elouahby@gmail.com>
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

""" Darbtech CRM adaptations """

import logging
from datetime import datetime, date
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
_LOGGER = logging.getLogger(__name__)


class CrmLead(models.Model):
    """ Darbtech CRM Lead adaptations """
    _inherit = 'crm.lead'

    reminder_date = fields.Date()

    @api.onchange('partner_name')
    def onchange_partner_name(self):
        if self.partner_name:
            parent = self.env['res.partner'].search([('name', '=', self.partner_name)], limit=1)
            if parent:
                client = self.env['res.partner'].search([('parent_id', '=', parent.id)], limit=1)
                if client:
                    values = {'contact_name': client.name,
                              'title': client.title}
                    self.update(values)



        """if partner_id:
            partner = self.env['res.partner'].browse(partner_id)

            partner_name = partner.parent_id.name
            if not partner_name and partner.is_company:
                partner_name = partner.name

            values =  {
                'partner_name': partner_name,
                'contact_name': partner.name if not partner.is_company else False,
                'title': partner.title.id,
                'street': partner.street,
                'street2': partner.street2,
                'city': partner.city,
                'state_id': partner.state_id.id,
                'country_id': partner.country_id.id,
                'email_from': partner.email,
                'phone': partner.phone,
                'mobile': partner.mobile,
                'zip': partner.zip,
                'function': partner.function,
                'website': partner.website,
            }
            values = self._onchange_partner_id_values(self.partner_id.id if self.partner_id else False)
        self.update(values)"""
