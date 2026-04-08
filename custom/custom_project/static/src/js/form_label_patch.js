/** @odoo-module **/
import { FormController } from "@web/views/form/form_controller";
import { FormLabel } from "@web/views/form/form_label";
import { ProjectProjectFormController } from "@project/views/project_form/project_project_form_controller";

// In Odoo 19, the form compiler generates FormLabel references in controller-level
// slots, but FormController.components does not include FormLabel by default.
// OWL resolves slot components from the definer's scope (the controller), so
// FormLabel must be present in the controller's components dict.

// Patch the base FormController for any future subclasses.
FormController.components = {
    ...FormController.components,
    FormLabel,
};

// ProjectProjectFormController already copied FormController.components at class
// definition time (via spread), before this module loaded. Patch it directly.
ProjectProjectFormController.components = {
    ...ProjectProjectFormController.components,
    FormLabel,
};