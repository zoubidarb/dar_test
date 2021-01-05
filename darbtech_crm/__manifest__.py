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

{
    'name': 'Darbtech CRM',
    'summary': 'Darbtech CRM customizations',
    'description': ''' It consists :
      * replace referred by many2one
      * be able to concern multiple partners on leads
      * changing default action for crm to lead
      * overwriting default stages for CRM leads
      * many several views adaptations ''',
    'version': '12.0.0.0.1',
    'category': 'Darbtech',
    'author': 'Youssef EL OUAHBY',
    'license': 'AGPL-3',
    'application': True,
    'installable': True,
    'depends': ['crm'],
    'data': [
        #Wizard
        'wizard/darbtech_res_partner_crm_lead_wizard_views.xml',
        #views
        'views/crm_lead_views.xml',
        'views/res_partner_views.xml',
        #templates
        'views/lead_portal_templates.xml',
    ]
}
