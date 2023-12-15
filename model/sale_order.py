# En tu archivo models/sale_order.py

from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    has_medical_service = fields.Boolean(string='Has Medical Service', default=False, readonly=True)

    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        res.has_medical_service = res._check_medical_service()
        return res

    def _check_medical_service(self):
        return any(line.product_id.is_medical and line.product_id.type == 'service' for line in self.order_line)

    def create_medical_appointment(self):
        # Lógica para crear una cita médica
        if self.has_medical_service:
            for line in self.order_line:
                if line.product_id.is_medical and line.product_id.type == 'service':
                    # Crear registro en medical.appointment aquí
                    self.env['medical.appointment'].create({
                        'patient_id': self.partner_id.id,  # Asumiendo que el cliente es el paciente
                        'appointment_date': fields.Date.today(),
                        # Otros campos relevantes...
                    })
                    break
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
