# -*- coding: utf-8 -*-

from odoo import models


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    def action_reserve_barcode_scanner(self):
        self.ensure_one()
        ScannerHardware = self.env['scanner.hardware']
        scanner = ScannerHardware.search([
            ('user_id', '=', False),
        ], limit=1)
        if scanner:
            # Login
            res = scanner.scanner_call(scanner.code, 'Login')
            res = scanner.scanner_call(scanner.code, 'admin')
            res = scanner.scanner_call(scanner.code, 'admin')
            
            # Set scenario and select receipt
            res = scanner.scanner_call(scanner.code, 'Receipt')
            res = scanner.scanner_call(scanner.code, self.name)
