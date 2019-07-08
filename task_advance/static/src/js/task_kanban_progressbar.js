odoo.define('task_advance.TaskKanbanProgressBar', function (require) {
'use strict';

    var utils = require('web.utils');
    var KanbanColumnProgressBar = require('web.KanbanColumnProgressBar');

    KanbanColumnProgressBar.include({
        init: function (parent, options, columnState) {
            this._super.apply(this, arguments);
            // this._super(parent, options, columnState);
            console.log('parent............',parent);
            this.progessBarPercentage = 0;
            console.log(this, this.progessBarPercentage);
        },

        _render: function () {
            var self = this;
            if (this.columnState.model === 'project.task' &&
                this.columnState.progressBarValues.sum_field === 'production_time_count'){
                this._super();
                // Display and animate the progress bars
                var machineCapacity = 0;
                var barNumber = 0;
                var barMinWidth = 0; // In %

                _.each(self.columnState.data, function (record) {
                    var recordData = record.data;
                    if (recordData.capacity_machine_id) {
                        self._rpc({
                            model: recordData.capacity_machine_id.model,
                            method: 'search_read',
                            fields: ['capacity'],
                            domain: [['id', '=', recordData.capacity_machine_id.res_id]]
                        }).then(function (values) {
                            machineCapacity = values[0].capacity;
                            _.each(self.colors, function (val, key) {
                                var $bar = self.$bars[val];
                                var count = self.subgroupCounts && self.subgroupCounts[key] || 0;

                                if (!$bar) {
                                return;
                            }

                            // Adapt tooltip
                            $bar.attr('data-original-title', count + ' ' + key);
                            $bar.tooltip({
                                delay: 0,
                                trigger: 'hover',
                            });

                            // Adapt active state
                            $bar.toggleClass('active progress-bar-striped', key === self.activeFilter);

                            // Adapt width
                            $bar.removeClass('o_bar_has_records transition-off');
                            window.getComputedStyle($bar[0]).getPropertyValue('width'); // Force reflow so that animations work
                            if (count > 0) {
                                $bar.addClass('o_bar_has_records');
                                // Make sure every bar that has records has some space
                                // and that everything adds up to 100%
                                var maxWidth = 100 - barMinWidth * barNumber;
                                self.$('.progress-bar.o_bar_has_records').css('max-width', maxWidth + '%');
                                count = self.totalCounterValue;
                                if (machineCapacity > 0){
                                    $bar.css('width', (count * 100 / machineCapacity) + '%');
                                    self.progessBarPercentage = (count * 100 / machineCapacity).toFixed(2);
                                    barNumber++;
                                    $bar.attr('aria-valuemin', 0);
                                    $bar.attr('aria-valuemax', machineCapacity);
                                    $bar.attr('aria-valuenow', count);
                                }
                                else {
                                    $bar.css('width', '');
                                }
                            } else {
                                $bar.css('width', '');
                            }
                        });
                        self.$('.progress-bar.o_bar_has_records').css('min-width', barMinWidth + '%');
                        });
                    }
                });
            }
            else {
                this._super();
            }
        },
    });

});