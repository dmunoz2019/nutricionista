# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class res_partner(models.Model):
    _inherit = 'res.partner'

    relationship = fields.Char(string='Relationship')
    relative_partner_id = fields.Many2one('res.partner',string="Relative_id")
    is_patient = fields.Boolean(string='Patient')
    is_person = fields.Boolean(string="Person")
    is_doctor = fields.Boolean(string="Doctor")
    is_insurance_company = fields.Boolean(string='Insurance Company')
    is_pharmacy = fields.Boolean(string="Pharmacy")
    patient_insurance_ids = fields.One2many('medical.insurance','patient_id')
    is_institution = fields.Boolean('Institution')
    company_insurance_ids = fields.One2many('medical.insurance','insurance_compnay_id','Insurance')
    reference = fields.Char('ID Number')
    medical_patient_partner_id = fields.Many2one('medical.patient', string="Medical Patient", compute='_compute_medical_patient', store=True)

    @api.depends('is_patient')
    def _compute_medical_patient(self):
        for partner in self:
            if partner.is_patient:
                # Lógica para encontrar y asignar el registro médico del paciente correspondiente
                patient = self.env['medical.patient'].search([('partner_address_id', '=', partner.id)], limit=1)
                partner.medical_patient_id = patient.id if patient else False


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
