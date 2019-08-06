# -*- coding: utf-8 -*-

from odoo import fields, models, _
from odoo.exceptions import UserError


class ReserveScanner(models.TransientModel):
    _name = 'stock_scanner.reserve_scanner'

    scanner_hardware_id = fields.Many2one(
        'scanner.hardware',
        string='Barcode scanner',
    )
    action = fields.Selection([
        ('login', 'Login'),
        ('logout', 'Logout'),
    ], string="Action", required=True, default='login')
    stock_picking_id = fields.Many2one(
        'stock.picking',
        "Transfer",
    )

    def button_do_action(self):
        self.ensure_one()
        if not self.scanner_hardware_id:
            raise UserError(_("Barcode scanner is not set!"))
        if self.action == 'login':
            self._scanner_login(self.scanner_hardware_id)
        elif self.action == 'logout':
            self._scanner_logout(self.scanner_hardware_id)
            
        if self._context.get('set_scenario'):
            name, step_vals = self._get_scenario_vals()
            if name:
                self._scanner_set_scenario(self.scanner_hardware_id, name, step_vals)
    
    def _scanner_login(self, scanner, user=False):
        user = user or self.env.user
        if scanner.user_id:
            if user == scanner.user_id:
                return
            raise UserError(
                _("You can not reserve scanner %s, because it was reserved by user %s.")
                % (scanner.code, scanner.user_id.name)
            )
        # Login
        scanner.scanner_call(scanner.code, 'Login')
        scanner.scanner_call(scanner.code, user.sudo().login)
    
    def _scanner_logout(self, scanner):
        scanner.empty_scanner_values()
        # Logout
        scanner.scanner_call(scanner.code, 'Logout')
        if self.stock_picking_id:
            self.stock_picking_id.write({'scanner_hardware_id': False})
    
    def _scanner_set_scenario(self, scanner, scenario_name, step_vals=[]):
        # Set scenario and do some steps
        scanner.scanner_call(scanner.code, scenario_name)
        for value in step_vals:
            scanner.scanner_call(scanner.code, value)
    
    def _get_scenario_vals(self):
        self.ensure_one()
        if self.stock_picking_id:
            return 'Receipt', [self.stock_picking_id.name]
        return False, []
