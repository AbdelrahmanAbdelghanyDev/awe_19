/** @odoo-module **/
import { X2ManyField, x2ManyField } from "@web/views/fields/x2many/x2many_field";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

export class One2ManySelectable extends X2ManyField {
    static template = "One2ManySelectable";

    setup() {
        super.setup();
        this.orm = useService("orm");
        this.notification = useService("notification");
    }

    get rendererProps() {
        const props = super.rendererProps;
        if (this.props.viewMode === "list") {
            props.allowSelectors = true;
        }
        return props;
    }

    _getSelectedIds() {
        const list = this.list;
        if (!list) return [];
        return list.records
            .filter((record) => record.selected)
            .map((record) => record.resId)
            .filter((id) => id);
    }

    async _actionSelectedLines(methodName) {
        const ids = this._getSelectedIds();
        if (ids.length === 0) {
            this.notification.add(_t("You must choose at least one record."), {
                type: "warning",
            });
            return;
        }
        await this.orm.call(this.list.resModel, methodName, [ids], {
            context: this.list.context,
        });
        // Reload the record to reflect changes
        await this.props.record.load();
        this.props.record.model.notify();
    }

    async onBulkVerify() {
        await this._actionSelectedLines("bulk_verify");
    }

    async onToAccountant() {
        await this._actionSelectedLines("to_accountant");
    }

    async onToExpense() {
        await this._actionSelectedLines("to_expense");
    }
}

const one2manySelectable = {
    ...x2ManyField,
    component: One2ManySelectable,
};

registry.category("fields").add("one2many_selectable", one2manySelectable);