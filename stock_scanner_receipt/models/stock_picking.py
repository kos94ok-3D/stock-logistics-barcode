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
            res = scanner.scanner_call(scanner.code, self.env.user.sudo().login)
            
            if scanner.user_id:
                # Set scenario and select receipt
                res = scanner.scanner_call(scanner.code, 'Receipt')
                res = scanner.scanner_call(scanner.code, self.name)
    
    def action_unreserve_barcode_scanner(self):
        self.ensure_one()
        ScannerHardware = self.env['scanner.hardware']
        scanner = ScannerHardware.search([
            ('user_id', '=', self.env.uid),
            ('reference_document', '=', self.id),
        ], limit=1)
        if scanner:
            # Logout
            res = scanner.scanner_call(scanner.code, 'Logout')
