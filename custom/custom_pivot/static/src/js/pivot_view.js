/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { PivotModel } from "@web/views/pivot/pivot_model";

patch(PivotModel.prototype, {

    _getMeasures() {
        const measures = super._getMeasures(...arguments);

        delete measures.opportunity_total_cost;
        delete measures.contribution_profit;

        measures.budget_total_x = {
            string: "Total Budget",
            type: "float",
            group_operator: "sum",
        };

        measures.margin_after_travel = {
            string: "CP After Travel",
            type: "float",
            group_operator: "sum",
        };

        return measures;
    },

});