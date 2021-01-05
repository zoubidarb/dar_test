odoo.define('display_documentation', function (require) {
    'use strict';

    var rpc = require('web.rpc');
    var SystrayMenu = require('web.SystrayMenu');
    var Widget = require('web.Widget');

    var DisplayDocumentation = Widget.extend({
        template: 'DisplayDocumentation',
        start: function() {
            return this._super();
        }
    });
    SystrayMenu.Items.push(DisplayDocumentation);

});
