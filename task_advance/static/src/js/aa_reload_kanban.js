odoo.define('task_advance.aa_reload_kanban', function (require) {
'use strict';

    var KanbanController = require('web.KanbanController');
    var rpc = require('web.rpc');

    KanbanController.include({
        renderButtons: function ($node) {
            this._super.apply(this, arguments);
            var self = this;
            if(this.modelName === "project.task"
            && this.model.defaultGroupedBy[0] === "aa_capacity_machine_id"){
                this.$buttons.css("width","550px");
                this.$buttons.append($('<button type="button" class="btn btn-primary btn-sm"\
                    style="float: right; margin-left:500px;" id="btn_update">Update</button>'
                ));
                this.$buttons.on('click', 'button#btn_update', function(ev){
                    self._rpc({
                        model: 'project.task',
                        method: 'updateCapacityHtml',
                        args: [[]],
                    }).then(function (){
                        location.reload();
                    });
                });
            }
        },
    });
});