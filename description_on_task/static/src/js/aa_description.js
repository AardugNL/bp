odoo.define('description_on_task.description', function (require) {
'use strict';

    var aa_KanbanRecord = require('web.KanbanRecord');

    KanbanRecord.include({
        init: function(parent, options) {
            this.events["mouseover .aa_customerName"] = "aa_hideRecords";
            this.events["mouseout .aa_customerName"] = "aa_showRecords";
            this._super.apply(this, arguments);
        },

        aa_hideRecords: function (event) {
            var aa_self = this;
            aa_self._rpc({
                model: 'project.task',
                method: 'aa_checkTaskDescription',
                args: [[], event.currentTarget.innerHTML],
            }).then(function (tasks){
                var aa_templateTag = document.getElementsByClassName('oe_kanban_content');
                for (var aa_t in aa_templateTag){
                    if (aa_templateTag[t].dataset){
                        for (var aa_task in aa_tasks){
                            if (aa_templateTag[aa_t].dataset.id == aa_tasks[aa_task]){
                                aa_templateTag[aa_t].style.opacity = 0.1
                            }
                        }
                    }
                }
            });
        },

        aa_showRecords: function (event){
            var aa_templateTag = document.getElementsByClassName('oe_kanban_content')
            for (var aa_t in aa_templateTag){
                if (aa_templateTag[aa_t].dataset){
                    aa_templateTag[aa_t].style.opacity = 1
                }
            }
        },
    });
});