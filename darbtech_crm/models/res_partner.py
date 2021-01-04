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

""" Darbtech CRM partner adaptations """


import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
_LOGGER = logging.getLogger(__name__)

class ResPartner(models.Model):
    """ Darbtech CRM partner adaptations """
    _inherit = 'res.partner'

    lead_ids = fields.One2many('crm.lead', 'partner_id')
