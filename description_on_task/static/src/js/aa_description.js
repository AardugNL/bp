odoo.define('description_on_task.aa_description', function (require) {
'use strict';

    var KanbanRecord = require('web.KanbanRecord');
    var KanbanController = require('web.KanbanController');

    KanbanRecord.include({
        init: function(parent, options) {
            this.events["mouseover .aa_customerName"] = "aa_hideRecords";
            this.events["mouseout .aa_customerName"] = "aa_showRecords";
            this.events["mouseover .aa_kanbanTag"] = "aa_decorateRecords";
            this.events["mouseout .aa_kanbanTag"] = "aa_removeDecorationRecords";
            this._super.apply(this, arguments);
        },

        aa_hideRecords: function (event) {
            var aa_self = this;
            aa_self._rpc({
                model: 'project.task',
                method: 'aa_checkTaskDescription',
                args: [[], event.currentTarget.innerHTML],
            }).then(function (aa_tasks){
                var aa_templateTag = document.getElementsByClassName('oe_kanban_content');
                for (var aa_t in aa_templateTag){
                    if (aa_templateTag[aa_t].dataset){
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
        aa_decorateRecords: function (event) {
            var aa_self = this;
            aa_self._rpc({
                model: 'project.task',
                method: 'aa_checkTagDescription',
                args: [[], event.currentTarget.innerHTML],
            }).then(function (aa_tasks){
                var aa_templateTag = document.getElementsByClassName('oe_kanban_content');
                for (var aa_t in aa_templateTag){
                    if (aa_templateTag[aa_t].dataset){
                        for (var aa_task in aa_tasks){
                            if (aa_templateTag[aa_t].dataset.id == aa_tasks[aa_task]){
                                aa_templateTag[aa_t].style.background = '#C0D4C3'
                            }
                        }
                    }
                }
            });
        },
        aa_removeDecorationRecords: function (event){
            var aa_templateTag = document.getElementsByClassName('oe_kanban_content')
            for (var aa_t in aa_templateTag){
                if (aa_templateTag[aa_t].dataset){
                    aa_templateTag[aa_t].style.background = 'white'
                }
            }
        },
    });

    // KanbanController.include({
    //     renderButtons: function ($node) {
    //         this._super.apply(this, arguments);
    //         var self = this;
    //         if(this.modelName === "project.task"
    //         && this.model.defaultGroupedBy[0] === "aa_capacity_machine_id"){
    //             this.$buttons.css("width","550px");
    //             this.$buttons.append($('<input type="text" name="FindTags" id="tag_taxt"\
    //                 style="margin-left:200px; width:300px; float: right;margin-right: 1%;" />\
    //                 <button type="button" class="btn btn-primary btn-sm"\
    //                 style="float: right; margin-left:500px;" id="btm_click_me">Click Me</button>'
    //             ));
    //             this.$buttons.on('click', 'button#btm_click_me', function(ev){
    //                 var aa_taxt = document.getElementById("tag_taxt").value;
    //                 console.log("aa_taxt:",aa_taxt);
    //                 if (aa_taxt){
    //                     self._rpc({
    //                         model: 'project.task',
    //                         method: 'aa_checkTaskTags',
    //                         args: [[], aa_taxt],
    //                     }).then(function (tasks){
    //                         var templateTag = document.getElementsByClassName('oe_kanban_content');
    //                         for (var t in templateTag){
    //                             if (templateTag[t].dataset){
    //                                 for (var task in tasks){
    //                                     if (templateTag[t].dataset.id == tasks[task]){
    //                                         templateTag[t].style.background = '#C0D4C3'
    //                                     }
    //                                 }
    //                             }
    //                         }
    //                     });
    //                 }
    //             });
    //         }
    //     },
    // });
});