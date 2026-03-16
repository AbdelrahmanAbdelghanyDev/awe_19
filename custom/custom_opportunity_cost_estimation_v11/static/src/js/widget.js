/** @odoo-module */

// Minimal migration: keep existing requires but use modern module header.
const core = require('web.core');
//var form_common = require('web.form_common');
const _t = core._t;
const QWeb = core.qweb;
const Model = require('web.rpc');
const relation_fields = require('web.relational_fields');
// web.field_registry may not be available as in older versions; use it if present
let registry;
try {
	registry = require('web.field_registry');
} catch (e) {
	registry = null;
}
const ListRenderer = require('web.ListRenderer');
const FieldOne2Many = relation_fields.FieldOne2Many


var One2ManySelectable = FieldOne2Many.extend({
		// my custom template for unique char field
		template: 'One2ManySelectable',

		multi_selection: true,
		hasSelectors:true,
		//viewType : 'list',
		//button click
		events: {
			"click .cf_button_to_warehouse": "action_selected_lines",
			"click .cf_button_to_accountant" : "action_selected_lines_2",
			"click .cf_button_to_expense" : "action_selected_expense",
		},
		init: function()
	    {
	    	this._super.apply(this, arguments);
			var self=this;
			var mem = false;
		},
		_render: function () 
		{
			if (!this.view) {
            return this._super();
        }
        if (this.renderer) {
            this.currentColInvisibleFields = this._evalColumnInvisibleFields();
            this.renderer.updateState(this.value, {'columnInvisibleFields': this.currentColInvisibleFields});
            this.pager.updateState({ size: this.value.count });
            return $.when();
        }
        var arch = this.view.arch;
        var viewType;
        if (arch.tag === 'tree') {
            viewType = 'list';
            this.currentColInvisibleFields = this._evalColumnInvisibleFields();
            this.renderer = new ListRenderer(this, this.value, {
                arch: arch,
                editable: this.mode === 'edit' && arch.attrs.editable,
                addCreateLine: !this.isReadonly && this.activeActions.create,
                addTrashIcon: !this.isReadonly && this.activeActions.delete,
                viewType: viewType,
                columnInvisibleFields: this.currentColInvisibleFields,
                hasSelectors : true,
            });
        }
        if (arch.tag === 'kanban') {
            viewType = 'kanban';
            var record_options = {
                editable: false,
                deletable: false,
                read_only_mode: this.isReadonly,
            };
            this.renderer = new KanbanRenderer(this, this.value, {
                arch: arch,
                record_options: record_options,
                viewType: viewType,
            });
        }
        this.$el.addClass('o_field_x2many o_field_x2many_' + viewType);
        var ret =  this.renderer ? this.renderer.appendTo(this.$el) : this._super();
        var  k = 1 ;
        if (this.record.data.estimation_ids)
        {
        	var self = this;
        	 this.$el.find('.o_data_row').each(function(i) {
 			 $( this ).addClass( "val-data-id:"+self.record.data.estimation_ids.data[i].ref );
				})
        	//this.record.data.estimation_ids.data["0"].ref;
        }
        else if (this.record.data.tasks_estimations_ids)
        {
        	var self = this;
        	 this.$el.find('.o_data_row').each(function(i) {
 			 $( this ).addClass( "val-data-id:"+self.record.data.tasks_estimations_ids.data[i].ref );
				})
        	//this.record.data.tasks_estimations_ids.data["0"].ref;
        }
		},
		start: function()
	    {
	    	this._super.apply(this, arguments);
			var self=this;
		   },
		// passing ids to function
		action_selected_expense: function()
		{
			var self=this;
			var selected_ids = self.get_selected_ids_one2many();
			if (selected_ids.length === 0)
			{
				this.do_warn(_t("You must choose at least one record."));
				return false;
			}
			this._rpc({
			 model: this.value.model,
			 method: 'to_expense',
			 args: [selected_ids],
			 context:this.value.context,
			})
		},
		action_selected_lines: function()
		{
			var self=this;
			var selected_ids = self.get_selected_ids_one2many();
			if (selected_ids.length === 0)
			{
				this.do_warn(_t("You must choose at least one record."));
				return false;
			}
			this._rpc({
			 model: this.value.model,
			 method: 'bulk_verify',
			 args: [selected_ids],
			 context:this.value.context,
			})
		},
		action_selected_lines_2: function()
		{
			var self=this;
			var selected_ids = self.get_selected_ids_one2many();
			if (selected_ids.length === 0)
			{
				this.do_warn(_t("You must choose at least one record."));
				return false;
			}
			this._rpc({
			 model: this.value.model,
			 method: 'to_accountant',
			 args: [selected_ids],
			 context:this.value.context,
			})
		},
		//collecting the selected IDS from one2manay list
		get_selected_ids_one2many: function ()
		{
			var self = this;
			var ids =[];
			if(this.record.data.estimation_ids)
			{
			//for (var i = this.record.data.estimation_ids.data.length - 1; i >= 0; i--) {
			// 	ids.push(this.record.data.estimation_ids.data[i].res_id)
			// 	}
			}
			else if (this.record.data.tasks_estimations_ids)
			{
			// 	for (var i = this.record.data.tasks_estimations_ids.data.length - 1; i >= 0; i--) {
			// 	ids.push(this.record.data.tasks_estimations_ids.data[i].res_id)
			// 	}
			}
			this.$el.find('td.o_list_record_selector input:checked')
					.closest('tr').each(function () {
						ids.push(parseInt(this.classList.value.split(':')[1]));
						console.log(ids);
			});

      var a = this.$el.find('td.o_list_record_selector input:checked')
      var b = this.$el.find('td.o_list_record_selector input:checked').length

      this.$el.find('div.o_checkbox input:checked').checked = false
      for (var i=0; i < b ; i++){
              a[i].checked = false;
      }

			return ids;
		},


	});
				// register with modern registry if available, otherwise fallback to legacy field_registry
				try{
					const registry_modern = require('@web/core/registry');
					registry_modern.category('fields').add('one2many_selectable', One2ManySelectable);
				}catch(e){
					if (registry && registry.add){
						registry.add('one2many_selectable', One2ManySelectable);
					}
				}
