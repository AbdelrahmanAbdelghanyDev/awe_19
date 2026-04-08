odoo.define('portal_expense', function(require) {
    'use strict';
    var core = require('web.core');
    var _t = core._t;
    var utils = require('web.utils');
    var lang = utils.get_cookie('website_lang') || $('html').attr('lang') || 'en_US';
    lang = lang.substring(0,2);

    $(document).ready(function(){
        var datepicker_date_input = $('#datepicker-container-date .input-group.date input');
//        var datepicker_date_to_input = $('#datepicker-container-date-to .input-group.date input');
        $(function () {
          $("#product").select2();
          $("#sale_order").select2();
          if ($('#input_unit_amount').val() != "")
          {
                var total= $('#input_unit_amount').val() * $('#input_quantity').val();
                $('#input_total_amount').val(total);
          }
        });

        $('#datepicker-container-date').each(function(){

            datepicker_date_input.datepicker({
                autoclose: true,
                enableOnReadonly: false,
                todayHighlight: true,
                language: lang,
            });
        });



        $('#input_unit_amount').on('change', function() {
            if ($('#input_quantity').val() == "")
                {$('#input_quantity').val(1);}
            var total= $('#input_unit_amount').val() * $('#input_quantity').val();
            $('#input_total_amount').val(total);
         });
         $('#input_quantity').on('change', function() {
            var total= $('#input_unit_amount').val() * $('#input_quantity').val();
            $('#input_total_amount').val(total);
         });
//        $('#datepicker-container-date-to').each(function(){
//
//            datepicker_date_to_input.datepicker({
//                autoclose: true,
//                enableOnReadonly: false,
//                todayHighlight: true,
//                language: lang,
//            });
//        });
//        datepicker_date_from_input.on("change", function (e) {
//            var date_from = datepicker_date_from_input.datepicker("getDate");
//            var date_to = datepicker_date_to_input.datepicker("getDate");
//            if (date_from > date_to) {
//                datepicker_date_to_input.datepicker("setDate", e.currentTarget.value);
//            }
//            datepicker_date_to_input.datepicker("option", "minDate", date_from);
//        });
//        datepicker_date_to_input.on("change", function (e) {
//            var date_from = datepicker_date_from_input.datepicker("getDate");
//            var date_to = datepicker_date_to_input.datepicker("getDate");
//            if (date_from > date_to) {
//                datepicker_date_from_input.datepicker("setDate", e.currentTarget.value);
//            }
//            datepicker_date_from_input.datepicker("option", "maxDate", date_to);
//        });

        var expenses_headers = $('.o_expenses_management_portal_users thead .o_list_record_selector input');
        var expenses_rows = $('.o_expenses_management_portal_users tbody .o_list_record_selector input');
        expenses_rows .prop('checked', false);
        expenses_headers .prop('checked', false);
        expenses_headers.click(function () {
            if (!$(this).prop('checked')) {
                $('#button_to_remove_expenses').addClass('o_hidden');
            } else {
                $('#button_to_remove_expenses').removeClass('o_hidden');
            }
            expenses_rows.prop('checked', $(this).prop('checked') || false);
        });
        expenses_rows.click(function () {
            if (expenses_headers.prop('checked') && !$(this).prop('checked')) {
                expenses_headers.prop('checked', false);
            }
            var something_checked = false;
            var i;
            for (i=0; i<expenses_rows.length; i++) {
                if (expenses_rows[i].checked) {
                    something_checked = true;
                    break;
                }
            }
            if (something_checked) {
                $('#button_to_remove_expenses').removeClass('o_hidden');
            } else {
                $('#button_to_remove_expenses').addClass('o_hidden');
            }
        });
        $('#delete_form').submit(function () {
            if ( ! confirm(_t('Do you really want to remove these records?'))) {
                event.preventDefault();
            }
        });
        $('#delete_expense_id').click(function () {
            if ( ! confirm(_t('Do you really want to remove these records?'))) {
                event.preventDefault();
            } else {
                document.getElementById('to_delete_checkbox').checked = true;
            }
        });
        $('#to_confirm_checkbox').click(function () {
            document.getElementById('to_delete_checkbox').checked = false;
        });
        $('#to_reset_state').click(function () {
            document.getElementById('to_delete_checkbox').checked = false;
            $('#input_state').val('draft');
        });
        $('.o_expenses_management_portal_users').on('change', "select[name='date_from_half_day']", function (e) {
            var select = $("select[name='date_to_half_day']");
            select.val(e.currentTarget.value);
        });
    });

});
