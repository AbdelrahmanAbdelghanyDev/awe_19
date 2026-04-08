/** @odoo-module **/
// web_domain_field is deprecated in Odoo 19.
// The functionality (using a computed char field as a domain attribute value)
// is now natively supported by Odoo's form field domain evaluation.
// This module is kept as a no-op for backward compatibility with dependents.
console.debug("web_domain_field: This module is deprecated. Dynamic field domains are natively supported in Odoo 19.");