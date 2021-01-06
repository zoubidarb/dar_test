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

""" Darbtech CRM  res_users adaptations """

from odoo import _, api, exceptions, fields, models, modules
from odoo.addons.base.models.res_users import is_selection_groups


class Users(models.Model):
    _name = 'res.users'
    _inherit = ['res.users']
    _description = 'Users'

    @api.model
    def systray_get_leads(self):
        """ get leads to show on systray navbar dashboard """
        query = """SELECT m.id, m.reminder_date,
                    CASE
                        WHEN %(today)s::date - reminder_date::date = 0 Then 'today'
                        WHEN %(today)s::date - reminder_date::date > 0 Then 'overdue'
                        WHEN %(today)s::date - reminder_date::date < 0 Then 'planned'
                    END AS states
                    FROM crm_lead AS m
                    WHERE m.type='lead' and m.reminder_date IS NOT NULL
                    GROUP BY m.id, states;
                    """

        self.env.cr.execute(query, {
            'today': fields.Date.context_today(self),
        })
        lead_data = self.env.cr.dictfetchall()
        leads = {'name': 'CRM Qualifications',
                 'icon': modules.module.get_module_icon(self.env['crm.lead']._original_module),
                 'model': 'crm.lead',
                 'total_count': len(lead_data),
                 'today_count': len([l for l in lead_data if l['states'] == 'today']),
                 'overdue_count': len([l for l in lead_data if l['states'] == 'overdue']),
                 'planned_count': len([l for l in lead_data if l['states'] == 'planned'])
                }
        return leads
