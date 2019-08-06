# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.tools.safe_eval import safe_eval


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    scanner_hardware_id = fields.Many2one(
        'scanner.hardware',
        string='Barcode scanner',
    )
    
    def action_reserve_barcode_scanner(self):
        self.ensure_one()
        ReserveScanner = self.env['stock_scanner.reserve_scanner']
        wizard = ReserveScanner.create({
            'action': 'login',
            'stock_picking_id': self.id,
        })
        action = self.env.ref('stock_scanner.reserve_scanner_action_window').read()[0]
        action['res_id'] = wizard.id
        action['context'] = dict(safe_eval(action['context']), set_scenario=True)
        return action
    
    def action_unreserve_barcode_scanner(self):
        self.ensure_one()
        ReserveScanner = self.env['stock_scanner.reserve_scanner']
        wizard = ReserveScanner.create({
            'scanner_hardware_id': self.scanner_hardware_id.id,
            'action': 'logout',
            'stock_picking_id': self.id,
        })
        wizard.button_do_action()
