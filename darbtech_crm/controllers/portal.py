# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import OrderedDict
from operator import itemgetter

from odoo import http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.tools import groupby as groupbyelem

from odoo.osv.expression import OR


class CustomerPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        values['lead_count'] = request.env['crm.lead'].search_count([('type', '=', 'lead')])
        return values

    # ------------------------------------------------------------
    # My Project
    # ------------------------------------------------------------
    def _lead_get_page_view_values(self, lead, access_token, **kwargs):
        values = {
            'page_name': 'lead',
            'lead': lead,
        }
        return self._get_page_view_values(lead, access_token, values, 'my_leads_history', False, **kwargs)

    @http.route(['/my/leads', '/my/leads/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_leads(self, page=1, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        Lead = request.env['crm.lead']
        domain = [('type', '=', 'lead')]

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
        }
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups('crm.lead', domain)
        #if date_begin and date_end:
        #    domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # projects count
        lead_count = Lead.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/leads",
            url_args={'sortby': sortby},
            total=lead_count,
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        leads = Lead.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_leads_history'] = leads.ids[:100]

        values.update({

            'leads': leads,
            'page_name': 'lead',
            'archive_groups': archive_groups,
            'default_url': '/my/leads',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby
        })
        return request.render("darbtech_crm.portal_my_leads", values)
