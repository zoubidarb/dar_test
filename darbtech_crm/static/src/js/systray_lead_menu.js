odoo.define('dartbetch_crm.leadMenu', function (require) {
"use strict";

var core = require('web.core');
var session = require('web.session');
var SystrayMenu = require('web.SystrayMenu');
var Widget = require('web.Widget');
var QWeb = core.qweb;

/**
 * Menu item appended in the systray part of the navbar, redirects to the next
 * activities of all app
 */
var LeadMenu = Widget.extend({
    name: 'lead_menu',
    template:'dartbetch_crm.leadMenu',
    events: {
        'click .o_mail_lead_action': '_onLeadActionClick',
        'click .o_lead_preview': '_onLeadFilterClick',
        'show.bs.dropdown': '_onLeadMenuShow',
    },
    willStart: function () {
        return $.when(this.call('mail_service', 'isReady'));
    },
    start: function () {
        this._$leadsPreview = this.$('.o_mail_systray_dropdown_items');
        this.call('mail_service', 'getMailBus').on('lead_updated', this, this._updateCounter);
        this._updateCounter();
        this._updateLeadPreview();
        return this._super();
    },
    //--------------------------------------------------
    // Private
    //--------------------------------------------------
    /**
     * Make RPC and get current user's activity details
     * @private
     */
    _getLeadData: function () {
        var self = this;

        return self._rpc({
            model: 'res.users',
            method: 'systray_get_leads',
            args: [],
            kwargs: {context: session.user_context},
        }).then(function (data) {
            self._leads = data;
            self.leadCounter = _.reduce(data, function (total_count, p_data) { return total_count + p_data.total_count; }, 0);
            self.$('.o_notification_counter').text(self.leadCounter);
            self.$el.toggleClass('o_no_notification', !self.leadCounter);
        });
    },
    /**
     * Get particular model view to redirect on click of activity scheduled on that model.
     * @private
     * @param {string} model
     */
    _getLeadModelViewID: function (model) {
        return this._rpc({
            model: model,
            method: 'get_lead_view_id'
        });
    },
    /**
     * Update(render) activity system tray view on activity updation.
     * @private
     */
    _updateLeadPreview: function () {
        var self = this;
        self._getLeadData().then(function (){
            self._$leadsPreview.html(QWeb.render('mail.systray.LeadMenu.Previews', {
                leads : self._leads
            }));
        });
    },
    /**
     * update counter based on activity status(created or Done)
     * @private
     * @param {Object} [data] key, value to decide activity created or deleted
     * @param {String} [data.type] notification type
     * @param {Boolean} [data.activity_deleted] when activity deleted
     * @param {Boolean} [data.activity_created] when activity created
     */
    _updateCounter: function (data) {
        if (data) {
            if (data.lead_created) {
                this.leadCounter ++;
            }
            if (data.lead_deleted && this.leadCounter > 0) {
                this.leadCounter --;
            }
            this.$('.o_notification_counter').text(this.leadCounter);
            this.$el.toggleClass('o_no_notification', !this.leadCounter);
        }
    },

    //------------------------------------------------------------
    // Handlers
    //------------------------------------------------------------

    /**
     * Redirect to specific action given its xml id
     * @private
     * @param {MouseEvent} ev
     */
    _onLeadActionClick: function (ev) {
        ev.stopPropagation();
        var actionXmlid = $(ev.currentTarget).data('action_xmlid');
        this.do_action(actionXmlid);
    },

    /**
     * Redirect to particular model view
     * @private
     * @param {MouseEvent} event
     */
    _onLeadFilterClick: function (event) {
        // fetch the data from the button otherwise fetch the ones from the parent (.o_mail_preview).
        var data = _.extend({}, $(event.currentTarget).data(), $(event.target).data());
        this.do_action({
            type: 'ir.actions.act_window',
            name: data.model_name,
            res_model:  data.res_model,
            views: [[false, 'kanban'], [false, 'form']],
            search_view_id: [false],
            domain: [['activity_user_id', '=', session.uid]],
            //context:context,
        });
    },
    /**
     * @private
     */
    _onLeadMenuShow: function () {
         this._updateLeadPreview();
    },
});

SystrayMenu.Items.push(LeadMenu);

return LeadMenu;

});
