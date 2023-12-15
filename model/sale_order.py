from odoo import models, fields, api
from datetime import timedelta
import datetime

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    has_medical_service = fields.Boolean(string='Has Medical Service', default=False, readonly=True)

    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        has_medical_service = res._check_medical_service()
        res.write({'has_medical_service': has_medical_service})
        if has_medical_service:
            res.create_medical_appointment()
        return res

    def find_available_doctor(self, desired_date, duration_hours=1):
        doctors = self.env['medical.physician'].search([])

        for doctor in doctors:
            appointments = self.env['medical.appointment'].search([
                ('doctor_id', '=', doctor.id),
                ('appointment_date', '>=', desired_date),
                ('appointment_date', '<=', desired_date + timedelta(hours=duration_hours))
            ])

            if not appointments:
                return doctor
        return None

    def _check_medical_service(self):
        return any(line.product_id.is_medical and line.product_id.type == 'service' for line in self.order_line)

    def create_medical_appointment(self):
        if self.has_medical_service:
            desired_date = self.date_order if isinstance(self.date_order, datetime.datetime) else fields.Datetime.from_string(self.date_order)
            available_doctor = self.find_available_doctor(desired_date)

            if available_doctor:
                for line in self.order_line:
                    if line.product_id.is_medical and line.product_id.type == 'service':
                        for _ in range(int(line.product_uom_qty)):
                            appointment_vals = {
                                'patient_id': self.partner_id.id,
                                'doctor_id': available_doctor.id,
                                'appointment_date': desired_date
                                # Otros campos relevantes...
                            }
                            self.env['medical.appointment'].create(appointment_vals)

    def action_view_medical_appointments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Medical Appointments',
            'view_mode': 'tree,form',
            'res_model': 'medical.appointment',
            'domain': [('patient_id', '=', self.partner_id.id)],
            'context': {'default_patient_id': self.partner_id.id},
            'views': [(self.env.ref('basic_hms.medical_appointment_tree_view').id, 'tree'),
                      (False, 'form')]
        }
