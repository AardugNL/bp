odoo.define('description_on_task.description', function (require) {
'use strict';

    var KanbanRecord = require('web.KanbanRecord');

    KanbanRecord.include({
        init: function(parent, options) {
            this.events["mouseover .customerName"] = "_hideRecords";
            this.events["mouseout .customerName"] = "_showRecords";
            this._super.apply(this, arguments);
        },

        _hideRecords: function (event) {
            var self = this;
            self._rpc({
                model: 'project.task',
                method: 'checkTaskDescription',
                args: [[], event.currentTarget.innerHTML],
            }).then(function (tasks){
                var templateTag = document.getElementsByClassName('oe_kanban_content');
                for (var t in templateTag){
                    if (templateTag[t].dataset){
                        for (var task in tasks){
                            if (templateTag[t].dataset.id == tasks[task]){
                                templateTag[t].style.opacity = 0.1
                            }
                        }
                    }
                }
            });
        },

        _showRecords: function (event){
            var templateTag = document.getElementsByClassName('oe_kanban_content')
            for (var t in templateTag){
                if (templateTag[t].dataset){
                    templateTag[t].style.opacity = 1
                }
            }
        },
    });
});