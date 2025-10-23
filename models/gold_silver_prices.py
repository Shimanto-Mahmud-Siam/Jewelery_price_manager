# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import math
import base64
import csv
import io
from odoo.exceptions import UserError

class GoldSilverPrices(models.Model):
    _name = 'gold.silver.prices'
    _description = 'Gold and Silver Prices'

    name = fields.Char(string="Record Title", required=True)
    
    # Gold prices
    gold_22k_price = fields.Float(string="22K Gold Price (per gram)")
    gold_21k_price = fields.Float(string="21K Gold Price (per gram)")
    gold_18k_price = fields.Float(string="18K Gold Price (per gram)")
    gold_traditional_price = fields.Float(string="Traditional Gold Price (per gram)")

    # Silver prices
    silver_22k_price = fields.Float(string="22K Silver Price (per gram)")
    silver_21k_price = fields.Float(string="21K Silver Price (per gram)")
    silver_18k_price = fields.Float(string="18K Silver Price (per gram)")
    silver_traditional_price = fields.Float(string="Traditional Silver Price (per gram)")
    silver_italian_price = fields.Float(string="Italian Silver Price (per gram)")
    
    def manual_update_prices(self):
        """Action to manually update all product prices based on current rates."""
        self.ensure_one()
        # Ensure no negative prices are stored; clamp negatives to zero and warn
        price_fields = [
            'gold_22k_price', 'gold_21k_price', 'gold_18k_price', 'gold_traditional_price',
            'silver_22k_price', 'silver_21k_price', 'silver_18k_price', 'silver_traditional_price', 'silver_italian_price'
        ]
        for field in price_fields:
            val = getattr(self, field, 0.0) or 0.0
            if val < 0:
                setattr(self, field, 0.0)

        self.env['product.template']._update_product_prices_scheduler()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _("Success!"),
                'message': _("All product prices have been successfully updated."),
                'type': 'success',
                'sticky': False,
            }
        }

    @api.constrains(
        'gold_22k_price','gold_21k_price','gold_18k_price','gold_traditional_price',
        'silver_22k_price','silver_21k_price','silver_18k_price','silver_traditional_price','silver_italian_price'
    )
    def _check_non_negative_prices(self):
        for rec in self:
            for field in [
                'gold_22k_price','gold_21k_price','gold_18k_price','gold_traditional_price',
                'silver_22k_price','silver_21k_price','silver_18k_price','silver_traditional_price','silver_italian_price'
            ]:
                val = getattr(rec, field) or 0.0
                if val < 0:
                    raise UserError(_(f"Price field '{field}' cannot be negative."))